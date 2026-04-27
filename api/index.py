import os
import sys
import traceback
import pickle
import json
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

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
def _predict(symptoms_input: List[str]) -> str:
    df = pd.read_csv(DATA_PATH)
    X = df.iloc[:, :-1]
    y = df["prognosis"]
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.3, random_state=20)
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)

    col_map = {c: i for i, c in enumerate(X.columns)}
    vec = np.zeros(len(col_map))
    for s in symptoms_input:
        key = s if s in col_map else s.replace(" ", "_")
        if key in col_map:
            vec[col_map[key]] = 1

    return clf.predict([vec])[0]


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
        disease = _predict(req.symptoms)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(500, f"Prediction error: {e}")

    precs = DISEASE_PRECAUTIONS.get(disease) or [
        p for p in _precaution_pkl.get(disease, []) if p and p.strip()
    ]
    rems = DISEASE_REMEDIES.get(disease, [])
    desc = _descriptions.get(disease, "")

    lang = req.lang or "en"
    return {
        "disease":     _tr(disease, lang),
        "description": _tr(desc, lang),
        "precautions": _tr_list(precs, lang),
        "remedies":    _tr_list(rems, lang),
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "model_loaded": len(SYMPTOMS_LIST) > 0,
        "symptoms_count": len(SYMPTOMS_LIST),
        "translation": HAS_TRANSLATOR,
    }
