import os
import sys
import pickle
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import requests
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# ── Translation support ─────────────────────────────────────────────────────
try:
    from deep_translator import GoogleTranslator
    TRANSLATION_AVAILABLE = True
except ImportError:
    TRANSLATION_AVAILABLE = False

app = FastAPI(title="HealthCare AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Paths ────────────────────────────────────────────────────────────────────
# This file lives at api/index.py so the project root is one level up
API_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(API_DIR)
MODEL_PATH = os.path.join(ROOT_DIR, "healthcare-chatbot", "models.pkl")
DATA_PATH  = os.path.join(ROOT_DIR, "healthcare-chatbot", "Data", "Training.csv")

# ── Load pickled data ────────────────────────────────────────────────────────
with open(MODEL_PATH, "rb") as f:
    _data = pickle.load(f)
    _le               = _data[2]
    _cols             = _data[3]
    _description_list = _data[5]
    _precautionDict   = _data[6]

symptoms_list = list(_cols)

# ── Medical knowledge base ───────────────────────────────────────────────────
# Import from same api/ directory
sys.path.insert(0, API_DIR)
from medical_data import DISEASE_REMEDIES, DISEASE_PRECAUTIONS, SEARCH_NAME_MAP


# ── Models ───────────────────────────────────────────────────────────────────
class DiagnosisRequest(BaseModel):
    symptoms: List[str]
    lang: Optional[str] = "en"


# ── Prediction ───────────────────────────────────────────────────────────────
def get_prediction(symptoms_exp: List[str]) -> str:
    df = pd.read_csv(DATA_PATH)
    X  = df.iloc[:, :-1]
    y  = df["prognosis"]
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.3, random_state=20)
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)

    sym_index = {s: i for i, s in enumerate(X.columns)}
    vec = np.zeros(len(sym_index))
    for s in symptoms_exp:
        if s in sym_index:
            vec[sym_index[s]] = 1
        elif s.replace(" ", "_") in sym_index:
            vec[sym_index[s.replace(" ", "_")]] = 1

    return clf.predict([vec])[0]


# ── Translation helpers ───────────────────────────────────────────────────────
def _translate(text: str, lang: str) -> str:
    if not TRANSLATION_AVAILABLE or lang == "en" or not text:
        return text
    try:
        return GoogleTranslator(source="en", target=lang).translate(text)
    except Exception:
        return text


def _translate_list(items: List[str], lang: str) -> List[str]:
    if not TRANSLATION_AVAILABLE or lang == "en" or not items:
        return items
    try:
        combined   = " || ".join(items)
        translated = GoogleTranslator(source="en", target=lang).translate(combined)
        return [i.strip() for i in translated.split(" || ")]
    except Exception:
        return items


# ── Routes ───────────────────────────────────────────────────────────────────
@app.get("/api/symptoms")
def get_symptoms():
    return {"symptoms": symptoms_list}


@app.post("/api/predict")
def predict(request: DiagnosisRequest):
    if not request.symptoms:
        raise HTTPException(status_code=400, detail="No symptoms provided")

    try:
        disease = get_prediction(request.symptoms)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

    precautions = (
        DISEASE_PRECAUTIONS.get(disease)
        or [p for p in _precautionDict.get(disease, []) if p and p.strip()]
    )
    remedies    = DISEASE_REMEDIES.get(disease, [])
    description = _description_list.get(disease, "")

    lang = request.lang or "en"

    return {
        "disease":     _translate(disease, lang),
        "description": _translate(description, lang),
        "precautions": _translate_list(precautions, lang),
        "remedies":    _translate_list(remedies, lang),
        "original_disease": disease,
    }


@app.get("/api/health")
def health():
    return {"status": "ok", "translation": TRANSLATION_AVAILABLE}
