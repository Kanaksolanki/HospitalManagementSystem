"""
Disease Risk Predictor
Input:  patient_data (dict) - e.g. {"age": 45, "bp": 130, "sugar": 110, "weight": 70, ...}
Output: {"disease": str, "risk_percent": float, "risk_level": str}

Model trained on age, blood_pressure, glucose (from patient_data's "age", "bp",
"sugar") via train_risk_model.py, using the Pima Indians Diabetes dataset.
"""

import joblib
import os
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "disease_risk_model.pkl")

_model = None


def _load_model():
    global _model
    if _model is None and os.path.exists(MODEL_PATH):
        _model = joblib.load(MODEL_PATH)
    return _model


def _risk_level(risk_percent: float) -> str:
    if risk_percent < 30:
        return "low"
    elif risk_percent < 60:
        return "medium"
    return "high"


def predict_disease_risk(patient_data: dict) -> dict:
    model = _load_model()
    if model is None:
        return {"disease": "diabetes", "risk_percent": 0.0, "risk_level": "unknown"}

    age = patient_data.get("age", 0)
    bp = patient_data.get("bp", 0)
    sugar = patient_data.get("sugar", 0)

    features = pd.DataFrame([[age, bp, sugar]], columns=["age", "blood_pressure", "glucose"])
    probability = model.predict_proba(features)[0][1]  # probability of class 1 (has diabetes)
    risk_percent = round(float(probability) * 100, 1)

    return {
        "disease": "diabetes",
        "risk_percent": risk_percent,
        "risk_level": _risk_level(risk_percent),
    }


if __name__ == "__main__":
    sample = {"age": 45, "bp": 130, "sugar": 110, "weight": 70}
    print(predict_disease_risk(sample))
    