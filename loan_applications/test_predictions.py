"""
Test script to validate loan repayment predictions
across diverse applicant profiles.
"""

import os
import sys
import pandas as pd

# Ensure current script directory is in sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from predict import predict_loan_repayment  # noqa: E402

TEST_CASES = [
    {
        "name": "High Earner & Low Debt (Prime)",
        "inputs": {
            "income": 105000,
            "years_employed": 9.0,
            "credit_score": 780,
            "debt_ratio": 0.10,
            "loan_amount": 25000,
        },
    },
    {
        "name": "Upper-Middle Income & Balanced Debt",
        "inputs": {
            "income": 75000,
            "years_employed": 6.5,
            "credit_score": 720,
            "debt_ratio": 0.20,
            "loan_amount": 35000,
        },
    },
    {
        "name": "Average Worker & Moderate Loan",
        "inputs": {
            "income": 55000,
            "years_employed": 4.0,
            "credit_score": 670,
            "debt_ratio": 0.28,
            "loan_amount": 50000,
        },
    },
    {
        "name": "High Debt Burden & High Loan",
        "inputs": {
            "income": 40000,
            "years_employed": 2.0,
            "credit_score": 590,
            "debt_ratio": 0.42,
            "loan_amount": 75000,
        },
    },
    {
        "name": "Subprime & Severe Risk",
        "inputs": {
            "income": 22000,
            "years_employed": 0.5,
            "credit_score": 510,
            "debt_ratio": 0.55,
            "loan_amount": 85000,
        },
    },
]


def run_tests():
    results = []
    for case in TEST_CASES:
        res = predict_loan_repayment(**case["inputs"])
        results.append(
            {
                "Profile": case["name"],
                "Income": f"${case['inputs']['income']:,}",
                "Years Emp": case["inputs"]["years_employed"],
                "Credit": case["inputs"]["credit_score"],
                "Debt Ratio": f"{case['inputs']['debt_ratio']:.1%}",
                "Loan Req": f"${case['inputs']['loan_amount']:,}",
                "Repay Prob": res["repaid_percentage"],
                "Risk Tier": res["risk_level"],
                "Decision": res["prediction"],
            }
        )

    df_results = pd.DataFrame(results)

    title = "LOAN APPLICANT EVALUATION RESULTS TABLE"
    print("\n" + "=" * 95)
    print(f"{title:^95}")
    print("=" * 95)
    print(df_results.to_string(index=False))
    print("=" * 95 + "\n")
    return df_results


if __name__ == "__main__":
    run_tests()
