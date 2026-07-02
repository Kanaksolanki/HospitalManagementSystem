"""
Disease Risk Predictor
Input:  patient_data (dict) - e.g. {"age": 45, "bp": 130, "sugar": 110, "weight": 70, ...}
Output: {"disease": str, "risk_percent": float, "risk_level": str}

Train on a public dataset (e.g. Pima Diabetes / UCI Heart Disease) and save the
trained model to ai-module/models/ with joblib. Load it once at import time.
"""

import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "disease_risk_model.pkl")

_model = None


def _load_model():
    global _model
    if _model is None and os.path.exists(MODEL_PATH):
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_disease_risk(patient_data: dict) -> dict:
    # TODO: replace with real feature engineering + model.predict_proba
    return {"disease": "diabetes", "risk_percent": 0.0, "risk_level": "low"}


if __name__ == "__main__":
    sample = {"age": 45, "bp": 130, "sugar": 110, "weight": 70}
    print(predict_disease_risk(sample))
