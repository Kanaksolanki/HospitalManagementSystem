"""
One-time training script for the disease risk model.
Uses the Pima Indians Diabetes dataset (public, well-known, good for an MVP).

We deliberately train on just 3 features (age, blood pressure, glucose/sugar)
instead of all 8 in the original dataset, because that's all patient_data
gives us per the API_CONTRACT.md shape: {"age", "bp", "sugar", "weight"}.
This is a simplification worth mentioning to your team/mentor -- a real
system would collect more features for better accuracy.
"""

import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

DATA_URL = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
COLUMNS = [
    "pregnancies", "glucose", "blood_pressure", "skin_thickness",
    "insulin", "bmi", "diabetes_pedigree", "age", "outcome",
]

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "disease_risk_model.pkl")


def train():
    df = pd.read_csv(DATA_URL, names=COLUMNS)

    # Use only the 3 features that map cleanly to patient_data's shape
    X = df[["age", "blood_pressure", "glucose"]]
    y = df["outcome"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    print(f"Test accuracy: {accuracy:.2%}")

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    train()