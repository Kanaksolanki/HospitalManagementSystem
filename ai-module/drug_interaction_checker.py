"""
Drug Interaction Checker
Input:  medicine_list (list[str])
Output: {"interaction_found": bool, "details": str}

Start rule-based: a CSV lookup of known dangerous combinations in data/.
"""

import csv
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "drug_interactions.csv")


def _load_interaction_pairs():
    pairs = set()
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pairs.add(frozenset([row["drug_a"].lower(), row["drug_b"].lower()]))
    return pairs


def check_drug_interaction(medicine_list: list) -> dict:
    pairs = _load_interaction_pairs()
    meds = [m.lower() for m in medicine_list]
    for i in range(len(meds)):
        for j in range(i + 1, len(meds)):
            if frozenset([meds[i], meds[j]]) in pairs:
                return {
                    "interaction_found": True,
                    "details": f"Interaction detected between {meds[i]} and {meds[j]}",
                }
    return {"interaction_found": False, "details": ""}


if __name__ == "__main__":
    print(check_drug_interaction(["aspirin", "warfarin"]))
