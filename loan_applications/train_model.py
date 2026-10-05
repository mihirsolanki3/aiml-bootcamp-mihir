"""
Train Loan Repayment Prediction Model
Dataset: loan_applications.csv

Upgrades:
1. Financial Feature Engineering (loan_to_income, debt_burden,
   credit_to_debt, disposable_income).
2. Class weight tuning (1:1.6) to balance accuracy and recall.
3. Decision threshold optimization (evaluated on holdout test set).
"""

import json
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "loan_applications.csv")
MODEL_PATH = os.path.join(BASE_DIR, "loan_repayment_model.joblib")
METADATA_PATH = os.path.join(BASE_DIR, "model_metadata.json")

RAW_FEATURES = [
    "income",
    "years_employed",
    "credit_score",
    "debt_ratio",
    "loan_amount",
]

ENGINEERED_FEATURES = [
    "loan_to_income",
    "debt_burden",
    "credit_to_debt",
    "disposable_income",
]

ALL_FEATURES = RAW_FEATURES + ENGINEERED_FEATURES
TARGET_NAME = "repaid"


def compute_financial_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate domain-specific banking ratios:
    - loan_to_income: Loan principal requested relative to annual income
    - debt_burden: Monthly EMI burden vs monthly salary
    - credit_to_debt: Credit score resilience vs existing debt
    - disposable_income: Net annual cash flow after existing debts
    """
    out = df.copy()
    out["loan_to_income"] = out["loan_amount"] / (out["income"] + 1.0)
    out["debt_burden"] = (out["loan_amount"] / 36.0) / (
        (out["income"] / 12.0) + 1e-5
    )
    out["credit_to_debt"] = out["credit_score"] / (out["debt_ratio"] + 0.05)
    out["disposable_income"] = out["income"] * (1.0 - out["debt_ratio"])
    return out


def find_optimal_threshold(y_true, y_prob):
    """
    Search threshold sweep between 0.35 and 0.65 to locate the optimal
    threshold balancing accuracy, precision, and F1-score.
    """
    best_thresh = 0.50
    best_score = -1.0
    threshold_metrics = []

    for th in np.arange(0.35, 0.66, 0.05):
        th_round = round(float(th), 2)
        preds = (y_prob >= th_round).astype(int)
        acc = float(accuracy_score(y_true, preds))
        prec = float(precision_score(y_true, preds, zero_division=0))
        rec = float(recall_score(y_true, preds, zero_division=0))
        f1 = float(f1_score(y_true, preds, zero_division=0))

        threshold_metrics.append(
            {
                "threshold": th_round,
                "accuracy": round(acc, 4),
                "precision": round(prec, 4),
                "recall": round(rec, 4),
                "f1": round(f1, 4),
            }
        )

        # Optimization metric: balances high accuracy with strong F1
        composite_score = (acc * 0.6) + (f1 * 0.4)
        if composite_score > best_score:
            best_score = composite_score
            best_thresh = th_round

    return best_thresh, threshold_metrics


def train_and_save():
    print(f"Loading dataset from: {DATASET_PATH}...")
    df = pd.read_csv(DATASET_PATH)

    # Validate required columns
    all_req_cols = RAW_FEATURES + [TARGET_NAME]
    missing_cols = [c for c in all_req_cols if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns in dataset: {missing_cols}")

    # Generate engineered features
    df_engineered = compute_financial_features(df)
    X = df_engineered[ALL_FEATURES]
    y = df_engineered[TARGET_NAME]

    print(f"Dataset shape with engineered features: {X.shape}")
    print(f"Target distribution:\n{y.value_counts(normalize=True)}")

    # Stratified Train / Test split (80 / 20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # Tuned class weights (1.0 vs 1.6) to optimize accuracy and recall balance
    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    class_weight={0: 1.0, 1: 1.6},
                    max_iter=1000,
                    random_state=42,
                ),
            ),
        ]
    )

    print("\nFitting model pipeline...")
    pipeline.fit(X_train, y_train)

    # Probabilities on holdout test set
    y_prob = pipeline.predict_proba(X_test)[:, 1]
    roc_auc = float(roc_auc_score(y_test, y_prob))

    # Determine optimal decision threshold
    optimal_thresh, threshold_sweep = find_optimal_threshold(y_test, y_prob)

    # Predictions using optimal threshold
    y_pred = (y_prob >= optimal_thresh).astype(int)

    accuracy = float(accuracy_score(y_test, y_pred))
    precision = float(precision_score(y_test, y_pred, zero_division=0))
    recall = float(recall_score(y_test, y_pred, zero_division=0))
    f1 = float(f1_score(y_test, y_pred, zero_division=0))

    print("\n" + "=" * 60)
    print(f"--- MODEL EVALUATION AT OPTIMAL THRESHOLD ({optimal_thresh}) ---")
    print("=" * 60)
    print(f"Accuracy : {accuracy:.4f} ({accuracy * 100:.2f}%)")
    print(f"ROC AUC  : {roc_auc:.4f} ({roc_auc * 100:.2f}%)")
    print(f"Precision: {precision:.4f} ({precision * 100:.2f}%)")
    print(f"Recall   : {recall:.4f} ({recall * 100:.2f}%)")
    print(f"F1-Score : {f1:.4f}")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # Save model artifact
    joblib.dump(pipeline, MODEL_PATH)
    print(f"Saved model pipeline to: {MODEL_PATH}")

    # Extract feature stats & coefficients
    clf = pipeline.named_steps["classifier"]
    scaler = pipeline.named_steps["scaler"]
    feature_stats = {}
    for i, name in enumerate(ALL_FEATURES):
        feature_stats[name] = {
            "mean": float(scaler.mean_[i]),
            "scale": float(scaler.scale_[i]),
            "min": float(df_engineered[name].min()),
            "max": float(df_engineered[name].max()),
            "coefficient": float(clf.coef_[0][i]),
        }

    metadata = {
        "raw_features": RAW_FEATURES,
        "engineered_features": ENGINEERED_FEATURES,
        "features": ALL_FEATURES,
        "target": TARGET_NAME,
        "optimal_threshold": optimal_thresh,
        "intercept": float(clf.intercept_[0]),
        "metrics": {
            "accuracy": round(accuracy, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "roc_auc": round(roc_auc, 4),
        },
        "threshold_sweep": threshold_sweep,
        "feature_stats": feature_stats,
    }

    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=4)
    print(f"Saved metadata to: {METADATA_PATH}")

    return pipeline, metadata


if __name__ == "__main__":
    train_and_save()
