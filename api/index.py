import os
import sys
import traceback
import pickle
import json
import re
import csv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# ── Translation (optional — graceful fallback if not available) ──────────────
try:
    from deep_translator import GoogleTranslator
    HAS_TRANSLATOR = True
except ImportError:
    HAS_TRANSLATOR = False

# ── Resolve paths ────────────────────────────────────────────────────────────
# On Vercel: __file__ = /var/task/api/index.py  → ROOT = /var/task
# Locally:   __file__ = .../health/api/index.py → ROOT = .../health
API_DIR  = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(API_DIR)

MODEL_PATH = os.path.join(ROOT_DIR, "healthcare-chatbot", "models.pkl")
DATA_PATH  = os.path.join(ROOT_DIR, "healthcare-chatbot", "Data", "Training.csv")

# ── Inline medical data (no import needed — avoids module resolution issues) ─
# We load it directly from the file to avoid import problems on Vercel
_medical_data_path = os.path.join(API_DIR, "medical_data.py")
DISEASE_REMEDIES = {}
DISEASE_PRECAUTIONS = {}
SEARCH_NAME_MAP = {}
MODEL_COLUMNS = []
MODEL_SYMPTOM_ALIAS = {}
MODEL_COL_INDEX = {}
TRAIN_X = None
TRAIN_Y = None

SYMPTOM_SYNONYMS = {
    "runny_nose": "runny_nose",
    "runny nose": "runny_nose",
    "nasal_discharge": "runny_nose",
    "burning_pee": "burning_micturition",
    "burning pee": "burning_micturition",
    "pain_while_urinating": "burning_micturition",
    "pain while urinating": "burning_micturition",
    "painful_urination": "burning_micturition",
    "shortness_of_breath": "breathlessness",
    "shortness of breath": "breathlessness",
    "breathing_difficulty": "breathlessness",
    "high_temperature": "high_fever",
    "sore_throat": "throat_irritation",
}

RED_FLAG_RULES = [
    {
        "id": "possible_heart_emergency",
        "required": {"chest_pain", "breathlessness"},
        "any_of": {"sweating", "nausea", "pain_behind_the_eyes"},
        "message": (
            "Possible emergency: chest pain with breathing difficulty can indicate a serious heart or lung problem. "
            "Seek urgent in-person care immediately."
        ),
    },
    {
        "id": "possible_severe_infection",
        "required": {"high_fever", "breathlessness"},
        "any_of": {"chest_pain", "cough"},
        "message": (
            "Possible severe respiratory infection: high fever with breathing difficulty needs urgent medical evaluation."
        ),
    },
]

SAFE_SELF_CARE_REMEDIES = [
    "Rest, stay hydrated, and monitor temperature and symptom progression.",
    "Use only doctor-approved over-the-counter symptom relief (for example, acetaminophen when appropriate).",
    "Avoid antibiotics, steroids, and unverified herbal treatments without clinician advice.",
    "Get in-person evaluation if symptoms persist, worsen, or feel severe.",
]

LOW_CONFIDENCE_PRECAUTIONS = [
    "This result has low confidence. Treat it as a preliminary suggestion only.",
    "Keep a symptom timeline (onset, severity, fever pattern) to share with your doctor.",
    "Do not self-medicate with prescription drugs without medical advice.",
    "Seek urgent care immediately for chest pain, breathing trouble, confusion, or persistent high fever.",
]

# Execute medical_data.py to get the dictionaries
if os.path.exists(_medical_data_path):
    _ns = {}
    with open(_medical_data_path, "r", encoding="utf-8") as f:
        exec(f.read(), _ns)
    DISEASE_REMEDIES = _ns.get("DISEASE_REMEDIES", {})
    DISEASE_PRECAUTIONS = _ns.get("DISEASE_PRECAUTIONS", {})
    SEARCH_NAME_MAP = _ns.get("SEARCH_NAME_MAP", {})

# ── Load model data ──────────────────────────────────────────────────────────
try:
    with open(MODEL_PATH, "rb") as f:
        _pkl = pickle.load(f)
    _cols           = _pkl[3]
    _descriptions   = _pkl[5]
    _precaution_pkl = _pkl[6]
    SYMPTOMS_LIST   = list(_cols)
except Exception as e:
    print(f"[STARTUP ERROR] Failed to load model: {e}")
    traceback.print_exc()
    SYMPTOMS_LIST   = []
    _cols           = []
    _descriptions   = {}
    _precaution_pkl = {}


def _normalize_symptom_name(symptom: str) -> str:
    clean = symptom.strip().lower().replace("-", " ").replace("_", " ")
    clean = re.sub(r"\s+", " ", clean)
    return clean.replace(" ", "_")


def _resolve_symptom_alias(symptom: str) -> str:
    normalized = _normalize_symptom_name(symptom)
    return _normalize_symptom_name(SYMPTOM_SYNONYMS.get(normalized, normalized))


def _load_runtime_model():
    global MODEL_COLUMNS, MODEL_SYMPTOM_ALIAS, MODEL_COL_INDEX, TRAIN_X, TRAIN_Y
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames or []
            if "prognosis" not in fieldnames:
                raise RuntimeError("Training data missing prognosis column")

            MODEL_COLUMNS = [c for c in fieldnames if c != "prognosis"]
            rows = list(reader)

        if not rows:
            raise RuntimeError("Training data is empty")

        MODEL_SYMPTOM_ALIAS = {_normalize_symptom_name(col): col for col in MODEL_COLUMNS}
        MODEL_COL_INDEX = {col: idx for idx, col in enumerate(MODEL_COLUMNS)}
        TRAIN_X = []
        TRAIN_Y = []
        for row in rows:
            TRAIN_X.append([1 if str(row.get(col, "0")).strip() == "1" else 0 for col in MODEL_COLUMNS])
            TRAIN_Y.append(str(row.get("prognosis", "")).strip())
    except Exception as e:
        print(f"[STARTUP ERROR] Failed to train runtime model: {e}")
        traceback.print_exc()
        MODEL_COLUMNS = []
        MODEL_SYMPTOM_ALIAS = {}
        MODEL_COL_INDEX = {}
        TRAIN_X = None
        TRAIN_Y = None


_load_runtime_model()


# ── FastAPI app ──────────────────────────────────────────────────────────────
app = FastAPI(title="HealthCare AI API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class DiagnosisRequest(BaseModel):
    symptoms: List[str]
    lang: Optional[str] = "en"


# ── Prediction ───────────────────────────────────────────────────────────────
def _predict(symptoms_input: List[str]):
    if TRAIN_X is None or TRAIN_Y is None or not MODEL_COLUMNS:
        raise RuntimeError("Prediction model is unavailable")

    vec = [0] * len(MODEL_COLUMNS)
    known_matches = 0
    normalized_inputs = []
    for symptom in symptoms_input:
        normalized = _resolve_symptom_alias(symptom)
        normalized_inputs.append(normalized)
        actual_col = MODEL_SYMPTOM_ALIAS.get(normalized)
        if actual_col:
            vec[MODEL_COL_INDEX[actual_col]] = 1
            known_matches += 1

    if known_matches == 0:
        raise ValueError("No known symptoms matched the model vocabulary")

    input_count = int(sum(vec))
    row_overlap = [sum(x_val and v_val for x_val, v_val in zip(row, vec)) for row in TRAIN_X]
    if not any(score > 0 for score in row_overlap):
        raise ValueError("Could not match the provided symptoms to known conditions")

    row_symptom_counts = [sum(row) for row in TRAIN_X]
    scores = []
    for overlap, row_count in zip(row_overlap, row_symptom_counts):
        precision = overlap / max(input_count, 1)
        recall = overlap / max(row_count, 1)
        scores.append(0.7 * precision + 0.3 * recall)

    disease_best_score = {}
    for idx, disease in enumerate(TRAIN_Y):
        score = float(scores[idx])
        if score <= 0:
            continue
        if disease not in disease_best_score or score > disease_best_score[disease]:
            disease_best_score[disease] = score

    ranked = sorted(
        [{"disease": d, "confidence": s} for d, s in disease_best_score.items()],
        key=lambda x: x["confidence"],
        reverse=True,
    )[:3]

    # Heuristic correction:
    # Fever + cough/breathlessness fits infections better than isolated asthma.
    respiratory_signal = {"high_fever", "cough", "breathlessness"}
    if (
        "high_fever" in normalized_inputs
        and len(respiratory_signal.intersection(set(normalized_inputs))) >= 2
        and ranked
        and ranked[0]["disease"] == "Bronchial Asthma"
    ):
        infection_priority = False
        for item in ranked:
            if item["disease"] in {"Pneumonia", "Tuberculosis"}:
                item["confidence"] += 0.15
                infection_priority = True
        if infection_priority:
            for item in ranked:
                if item["disease"] == "Bronchial Asthma":
                    item["confidence"] -= 0.05
        ranked = sorted(ranked, key=lambda x: x["confidence"], reverse=True)

    top_disease = ranked[0]["disease"]
    confidence = ranked[0]["confidence"]
    confidence_bucket = "high" if confidence >= 0.75 else ("medium" if confidence >= 0.5 else "low")
    return {
        "top_disease": top_disease,
        "confidence": confidence,
        "confidence_bucket": confidence_bucket,
        "known_matches": known_matches,
        "ranked_predictions": ranked,
        "normalized_inputs": normalized_inputs,
    }


# ── Translation ──────────────────────────────────────────────────────────────
def _tr(text: str, lang: str) -> str:
    if not HAS_TRANSLATOR or lang == "en" or not text:
        return text
    try:
        return GoogleTranslator(source="en", target=lang).translate(text)
    except Exception:
        return text


def _tr_list(items: List[str], lang: str) -> List[str]:
    if not HAS_TRANSLATOR or lang == "en" or not items:
        return items
    try:
        joined = " || ".join(items)
        result = GoogleTranslator(source="en", target=lang).translate(joined)
        return [s.strip() for s in result.split(" || ")]
    except Exception:
        return items


# ── Routes ───────────────────────────────────────────────────────────────────
@app.get("/api/symptoms")
def get_symptoms():
    return {"symptoms": SYMPTOMS_LIST}


@app.post("/api/predict")
def predict(req: DiagnosisRequest):
    if not req.symptoms:
        raise HTTPException(400, "No symptoms provided")

    try:
        pred = _predict(req.symptoms)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(500, f"Prediction error: {e}")

    disease = pred["top_disease"]
    confidence = pred["confidence"]
    confidence_bucket = pred["confidence_bucket"]
    known_matches = pred["known_matches"]
    normalized_inputs = set(pred["normalized_inputs"])
    is_uncertain = confidence_bucket == "low" or known_matches < 2

    precs = DISEASE_PRECAUTIONS.get(disease) or [
        p for p in _precaution_pkl.get(disease, []) if p and p.strip()
    ]
    rems = list(SAFE_SELF_CARE_REMEDIES)
    desc = _descriptions.get(disease, "")
    red_flag_alerts = []

    for rule in RED_FLAG_RULES:
        required_ok = rule["required"].issubset(normalized_inputs)
        any_ok = not rule["any_of"] or bool(rule["any_of"].intersection(normalized_inputs))
        if required_ok and any_ok:
            red_flag_alerts.append(rule["message"])

    if is_uncertain:
        desc = (
            "The symptom match is not strong enough for a reliable disease-specific result. "
            "Please consult a qualified doctor for confirmation."
        )
        precs = list(LOW_CONFIDENCE_PRECAUTIONS)
        # On low confidence we avoid disease-specific remedy-like claims.
        rems = list(SAFE_SELF_CARE_REMEDIES)
    else:
        if not precs:
            precs = [
                "Follow a doctor-approved treatment plan for this condition.",
                "Monitor symptom changes and report worsening signs early.",
            ]

    lang = req.lang or "en"
    localized_red_flags = _tr_list(red_flag_alerts, lang)
    return {
        "disease":     _tr(SEARCH_NAME_MAP.get(disease, disease), lang),
        "description": _tr(desc, lang),
        "precautions": _tr_list(precs, lang),
        "remedies":    _tr_list(rems, lang),
        "confidence": confidence,
        "confidence_bucket": confidence_bucket,
        "matched_symptoms": known_matches,
        "uncertain": is_uncertain,
        "red_flags": localized_red_flags,
        "possible_conditions": [
            {
                "disease": _tr(SEARCH_NAME_MAP.get(p["disease"], p["disease"]), lang),
                "confidence": p["confidence"],
            }
            for p in pred["ranked_predictions"]
        ],
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "model_loaded": len(SYMPTOMS_LIST) > 0,
        "symptoms_count": len(SYMPTOMS_LIST),
        "runtime_model_loaded": TRAIN_X is not None,
        "translation": HAS_TRANSLATOR,
    }
