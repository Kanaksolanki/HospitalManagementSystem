"""
Quick demo runner for the disease risk predictor.

Loads data/sample_risk_cases.json (low/medium/high risk examples) and runs
each through predict_disease_risk(), so you can show the model working
end-to-end without needing a live Django endpoint.

Usage:
    cd ai-module
    python demo_risk_cases.py

Requires the trained model to exist first:
    python train_risk_model.py
"""

import json
import os

from risk_predictor import predict_disease_risk

CASES_PATH = os.path.join(os.path.dirname(__file__), "data", "sample_risk_cases.json")


def main():
    with open(CASES_PATH) as f:
        cases = json.load(f)

    print(f"{'Case':45} {'Disease':10} {'Risk %':8} {'Level':8}")
    print("-" * 75)
    for case in cases:
        result = predict_disease_risk(case["patient_data"])
        print(
            f"{case['label']:45} {result['disease']:10} "
            f"{result['risk_percent']:<8} {result['risk_level']:8}"
        )


if __name__ == "__main__":
    main()
