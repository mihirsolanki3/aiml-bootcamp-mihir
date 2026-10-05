"""
Train Predictions & Evaluation Script
Runs model predictions across dataset samples from loan_applications.csv,
computes financial ratio features, and compares actual vs predicted outcomes.
"""

import os
import sys
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from predict import (  # noqa: E402
    load_model,
    ALL_FEATURE_COLUMNS,
    DEFAULT_THRESHOLD,
)
from train_model import compute_financial_features  # noqa: E402


def run_train_predictions(num_samples: int = 10):
    """
    Load the trained model and run predictions on dataset samples,
    displaying actual vs predicted outcomes.
    """
    model, metadata = load_model()
    thresh = (
        metadata.get("optimal_threshold", DEFAULT_THRESHOLD)
        if metadata
        else DEFAULT_THRESHOLD
    )
    csv_path = os.path.join(SCRIPT_DIR, "loan_applications.csv")

    if not os.path.exists(csv_path):
        print(f"Error: Dataset not found at {csv_path}")
        return

    df = pd.read_csv(csv_path)
    samples = df.head(num_samples).copy()

    # Generate engineered features
    samples_feat = compute_financial_features(samples)

    X = samples_feat[ALL_FEATURE_COLUMNS]
    probs = model.predict_proba(X)[:, 1]
    preds = (probs >= thresh).astype(int)

    samples["repaid_prob"] = (probs * 100).round(1).astype(str) + "%"
    samples["predicted"] = [
        "Repaid (1)" if p == 1 else "Default (0)" for p in preds
    ]
    samples["actual"] = samples["repaid"].map(
        {1: "Repaid (1)", 0: "Default (0)"}
    )
    samples["match"] = samples["repaid"] == preds

    display_cols = [
        "applicant_id",
        "income",
        "years_employed",
        "credit_score",
        "debt_ratio",
        "loan_amount",
        "actual",
        "predicted",
        "repaid_prob",
        "match",
    ]

    title = f"DATASET PREDICTIONS (FIRST {num_samples} APPLICANTS)"
    print("\n" + "=" * 105)
    print(f"{title:^105}")
    print("=" * 105)
    print(samples[display_cols].to_string(index=False))
    print("=" * 105)

    match_rate = samples["match"].mean() * 100
    print(
        f"Decision Cutoff: {thresh:.2f} | "
        f"Batch Match Rate: {match_rate:.1f}%\n"
    )


if __name__ == "__main__":
    run_train_predictions(10)
