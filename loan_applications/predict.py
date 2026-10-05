"""
Loan Repayment Predictor
Predict whether an applicant will repay a loan based on financial features:
- income
- years_employed
- credit_score
- debt_ratio
- loan_amount
Plus engineered financial ratios:
- loan_to_income (leverage)
- debt_burden (monthly EMI stress)
- credit_to_debt (credit quality relative to debt)
- disposable_income (net annual cash flow)
"""

import argparse
import json
import os
import warnings
import joblib
import pandas as pd

# Suppress serialization/version warnings across differing environments
warnings.filterwarnings("ignore")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "loan_repayment_model.joblib")
METADATA_PATH = os.path.join(BASE_DIR, "model_metadata.json")

# Calibrated optimal decision threshold (maximizes accuracy & F1)
DEFAULT_THRESHOLD = 0.45

RAW_FEATURE_COLUMNS = [
    "income",
    "years_employed",
    "credit_score",
    "debt_ratio",
    "loan_amount",
]

ENGINEERED_FEATURE_COLUMNS = [
    "loan_to_income",
    "debt_burden",
    "credit_to_debt",
    "disposable_income",
]

ALL_FEATURE_COLUMNS = RAW_FEATURE_COLUMNS + ENGINEERED_FEATURE_COLUMNS
FEATURE_COLUMNS = ALL_FEATURE_COLUMNS

_model = None
_metadata = None


def load_model():
    """Load model pipeline and metadata from disk."""
    global _model, _metadata
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model file not found at {MODEL_PATH}. "
                "Please run train_model.py first."
            )
        _model = joblib.load(MODEL_PATH)

    if _metadata is None and os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "r") as f:
            _metadata = json.load(f)

    return _model, _metadata


def compute_features_dict(
    income: float,
    years_employed: float,
    credit_score: float,
    debt_ratio: float,
    loan_amount: float,
) -> dict:
    """Compute base and engineered financial ratios for an applicant."""
    loan_to_income = float(loan_amount) / (float(income) + 1.0)
    debt_burden = (float(loan_amount) / 36.0) / (
        (float(income) / 12.0) + 1e-5
    )
    credit_to_debt = float(credit_score) / (float(debt_ratio) + 0.05)
    disposable_income = float(income) * (1.0 - float(debt_ratio))

    return {
        "income": float(income),
        "years_employed": float(years_employed),
        "credit_score": float(credit_score),
        "debt_ratio": float(debt_ratio),
        "loan_amount": float(loan_amount),
        "loan_to_income": loan_to_income,
        "debt_burden": debt_burden,
        "credit_to_debt": credit_to_debt,
        "disposable_income": disposable_income,
    }


def predict_loan_repayment(
    income: float,
    years_employed: float,
    credit_score: float,
    debt_ratio: float,
    loan_amount: float,
    threshold: float = None,
) -> dict:
    """Predict loan repayment likelihood for a single applicant."""
    model, metadata = load_model()

    if threshold is None:
        if metadata and "optimal_threshold" in metadata:
            threshold = float(metadata["optimal_threshold"])
        else:
            threshold = DEFAULT_THRESHOLD

    # Normalize debt_ratio if entered as percentage > 1 (e.g. 25 -> 0.25)
    if debt_ratio > 1.0:
        debt_ratio = debt_ratio / 100.0

    all_inputs = compute_features_dict(
        income=income,
        years_employed=years_employed,
        credit_score=credit_score,
        debt_ratio=debt_ratio,
        loan_amount=loan_amount,
    )

    input_df = pd.DataFrame([all_inputs])[ALL_FEATURE_COLUMNS]

    probabilities = model.predict_proba(input_df)[0]
    prob_default = float(probabilities[0])
    prob_repaid = float(probabilities[1])

    is_repaid = int(prob_repaid >= threshold)
    if is_repaid == 1:
        decision = "Will Repay (Approved)"
    else:
        decision = "Will Not Repay (High Risk / Default)"

    # Risk level categorization based on repayment probability
    if prob_repaid >= 0.65:
        risk_level = "Low Risk"
        recommendation = (
            "Strong Approval - Applicant demonstrates high creditworthiness "
            "with above-average repayment probability."
        )
    elif prob_repaid >= 0.48:
        risk_level = "Moderate Risk"
        recommendation = (
            "Standard Approval - Applicant profile exceeds baseline "
            "repayment likelihood; standard loan terms recommended."
        )
    elif prob_repaid >= 0.35:
        risk_level = "Elevated Risk"
        recommendation = (
            "Conditional / Manual Review - Marginally below threshold; "
            "consider reducing loan amount or requiring collateral."
        )
    else:
        risk_level = "High Risk"
        recommendation = (
            "Decline - High probability of default based on income, "
            "debt ratio, and credit history."
        )

    # Analyze feature impacts vs dataset averages
    contributions = []
    if metadata and "feature_stats" in metadata:
        stats = metadata["feature_stats"]
        for feat in ALL_FEATURE_COLUMNS:
            if feat in stats:
                val = float(input_df[feat].iloc[0])
                mean_val = stats[feat]["mean"]
                coef = stats[feat]["coefficient"]
                direction = (val - mean_val) * coef
                if direction > 0:
                    impact = "Positive (Improves Repayment Chance)"
                else:
                    impact = "Negative (Increases Default Risk)"
                contributions.append(
                    {
                        "feature": feat,
                        "value": val,
                        "average": round(mean_val, 2),
                        "impact": impact,
                    }
                )

    return {
        "prediction": decision,
        "repaid_label": is_repaid,
        "probability_repaid": round(prob_repaid, 4),
        "probability_default": round(prob_default, 4),
        "repaid_percentage": f"{prob_repaid * 100:.1f}%",
        "default_percentage": f"{prob_default * 100:.1f}%",
        "risk_level": risk_level,
        "recommendation": recommendation,
        "threshold_used": threshold,
        "inputs": {
            "income": float(income),
            "years_employed": float(years_employed),
            "credit_score": float(credit_score),
            "debt_ratio": float(debt_ratio),
            "loan_amount": float(loan_amount),
            "loan_to_income": all_inputs["loan_to_income"],
            "debt_burden": all_inputs["debt_burden"],
            "credit_to_debt": all_inputs["credit_to_debt"],
            "disposable_income": all_inputs["disposable_income"],
        },
        "feature_contributions": contributions,
    }


def parse_clean_float(
    prompt_text: str, min_val: float = None, max_val: float = None
) -> float:
    """Prompt user for a numeric value with validation."""
    while True:
        raw = input(prompt_text).strip()
        cleaned = raw.replace("$", "").replace(",", "").replace("%", "")
        try:
            val = float(cleaned)
            if min_val is not None and val < min_val:
                print(f"  [!] Value must be at least {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"  [!] Value must be at most {max_val}.")
                continue
            return val
        except ValueError:
            print("  [!] Please enter a valid numerical value.")


def display_result(result: dict):
    """Print clean terminal summary of prediction outcome."""
    print("\n" + "=" * 65)
    print("             LOAN REPAYMENT PREDICTION RESULT             ")
    print("=" * 65)
    can_repay = result["repaid_label"] == 1
    if can_repay:
        status_line = "YES - USER CAN REPAY LOAN (Approved)"
    else:
        status_line = "NO - USER CANNOT REPAY (High Risk / Default)"

    print(f" >>> CAN USER REPAY? : {status_line}")
    print(f" >>> Repayment Chance: {result['repaid_percentage']}")
    print(f" >>> Default Risk    : {result['default_percentage']}")
    print(f" >>> Risk Level      : {result['risk_level']}")
    print(f" >>> Decision Cutoff : {result['threshold_used']:.2f}")
    print(f" >>> Recommendation  : {result['recommendation']}")
    print("-" * 65)
    print(" Applicant Details Entered:")
    print(f"   * Income           : ${result['inputs']['income']:,.2f}")
    print(
        f"   * Years Employed   : "
        f"{result['inputs']['years_employed']} years"
    )
    print(f"   * Credit Score     : {result['inputs']['credit_score']}")
    print(f"   * Debt Ratio       : {result['inputs']['debt_ratio']:.2%}")
    print(f"   * Loan Amount      : ${result['inputs']['loan_amount']:,.2f}")
    print(
        f"   * Loan-to-Income   : {result['inputs']['loan_to_income']:.2f}x"
    )
    print(
        f"   * Disposable Income: "
        f"${result['inputs']['disposable_income']:,.2f}/yr"
    )
    print("-" * 65)
    if result["feature_contributions"]:
        print(" Key Feature Drivers:")
        for item in result["feature_contributions"]:
            feat_title = item["feature"].replace("_", " ").title()
            print(f"   * {feat_title:18s}: {item['impact']}")
    print("=" * 65 + "\n")


def interactive_mode():
    """Run an interactive CLI session."""
    print("=" * 65)
    print("   AI LOAN REPAYMENT PREDICTOR - ENTER YOUR APPLICANT DATA   ")
    print("=" * 65)
    print("Please type the applicant details below:\n")

    while True:
        income = parse_clean_float(
            "1. Annual Income ($) [e.g. 70000]: ", min_val=0
        )
        years_employed = parse_clean_float(
            "2. Years Employed [e.g. 5.5]: ", min_val=0, max_val=60
        )
        credit_score = parse_clean_float(
            "3. Credit Score (300 - 850) [e.g. 720]: ",
            min_val=300,
            max_val=850,
        )
        debt_ratio = parse_clean_float(
            "4. Debt-to-Income Ratio [e.g. 0.25 or 25%]: ", min_val=0
        )
        loan_amount = parse_clean_float(
            "5. Loan Amount Requested ($) [e.g. 30000]: ", min_val=500
        )

        result = predict_loan_repayment(
            income=income,
            years_employed=years_employed,
            credit_score=credit_score,
            debt_ratio=debt_ratio,
            loan_amount=loan_amount,
        )

        display_result(result)

        cont = input("Evaluate another applicant? (y/n): ").strip().lower()
        if cont not in ("y", "yes"):
            print("Exiting predictor. Have a great day!")
            break
        print("\n" + "-" * 65 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Predict loan repayment status from applicant features."
    )
    parser.add_argument("--income", type=float, help="Annual income ($)")
    parser.add_argument("--years", type=float, help="Years employed")
    parser.add_argument("--credit", type=float, help="Credit score (300-850)")
    parser.add_argument(
        "--debt", type=float, help="Debt ratio (e.g. 0.25 or 25)"
    )
    parser.add_argument(
        "--loan", type=float, help="Loan amount requested ($)"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=None,
        help="Classification threshold (default: optimal from model)",
    )

    args = parser.parse_args()

    # Check if arguments provided
    if (
        args.income is not None
        and args.years is not None
        and args.credit is not None
        and args.debt is not None
        and args.loan is not None
    ):
        result = predict_loan_repayment(
            income=args.income,
            years_employed=args.years,
            credit_score=args.credit,
            debt_ratio=args.debt,
            loan_amount=args.loan,
            threshold=args.threshold,
        )
        display_result(result)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
