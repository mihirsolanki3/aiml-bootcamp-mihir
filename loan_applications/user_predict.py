"""
Loan Repayment Predictor - User Input Interactive Script
Run this script to enter custom applicant values and predict whether
the applicant can repay the loan or not.
"""

from predict import predict_loan_repayment


def main():
    print("=" * 65)
    print("      AI LOAN REPAYMENT PREDICTOR - ENTER CUSTOM INPUTS      ")
    print("=" * 65)
    print("Please enter the applicant's details below:\n")

    # 1. Income
    while True:
        try:
            raw_income = input("1. Enter Annual Income ($) [e.g. 75000]: ")
            clean_str = raw_income.replace("$", "").replace(",", "").strip()
            income = float(clean_str)
            if income < 0:
                print("   [!] Income cannot be negative.")
                continue
            break
        except ValueError:
            print("   [!] Please enter a valid number for income.")

    # 2. Years Employed
    while True:
        try:
            raw_years = input("2. Enter Years Employed [e.g. 5.5]: ")
            years_employed = float(raw_years.strip())
            if years_employed < 0:
                print("   [!] Years employed cannot be negative.")
                continue
            break
        except ValueError:
            print("   [!] Please enter a valid number for years employed.")

    # 3. Credit Score
    while True:
        try:
            prompt = "3. Enter Credit Score (300 - 850) [e.g. 720]: "
            credit_score = float(input(prompt).strip())
            if credit_score < 300 or credit_score > 850:
                print("   [!] Credit score must be between 300 and 850.")
                continue
            break
        except ValueError:
            print("   [!] Please enter a valid number for credit score.")

    # 4. Debt Ratio
    while True:
        try:
            prompt = "4. Enter Debt-to-Income Ratio [e.g. 0.25 or 25%]: "
            debt_ratio = float(input(prompt).replace("%", "").strip())
            if debt_ratio < 0:
                print("   [!] Debt ratio cannot be negative.")
                continue
            if debt_ratio > 1.0:
                debt_ratio = debt_ratio / 100.0
            break
        except ValueError:
            print("   [!] Please enter a valid number for debt ratio.")

    # 5. Loan Amount
    while True:
        try:
            prompt = "5. Enter Loan Amount Requested ($) [e.g. 30000]: "
            clean_str = input(prompt).replace("$", "").replace(",", "").strip()
            loan_amount = float(clean_str)
            if loan_amount <= 0:
                print("   [!] Loan amount must be greater than 0.")
                continue
            break
        except ValueError:
            print("   [!] Please enter a valid number for loan amount.")

    # Run Prediction
    result = predict_loan_repayment(
        income=income,
        years_employed=years_employed,
        credit_score=credit_score,
        debt_ratio=debt_ratio,
        loan_amount=loan_amount,
    )

    can_repay = result["repaid_label"] == 1

    print("\n" + "=" * 65)
    print("                    PREDICTION OUTCOME                    ")
    print("=" * 65)
    if can_repay:
        print(" >>> RESULT: YES! THE USER CAN REPAY THE LOAN (APPROVED)")
    else:
        print(" >>> RESULT: NO! THE USER CANNOT REPAY (DEFAULT RISK)")
    print("-" * 65)
    print(f" * Repayment Probability : {result['repaid_percentage']}")
    print(f" * Default Risk          : {result['default_percentage']}")
    print(f" * Risk Tier             : {result['risk_level']}")
    print(f" * Recommendation        : {result['recommendation']}")
    print("-" * 65)
    print(" Inputs & Financial Ratios Evaluated:")
    print(f"   - Annual Income        : ${income:,.2f}")
    print(f"   - Years Employed       : {years_employed} years")
    print(f"   - Credit Score         : {credit_score}")
    print(f"   - Debt Ratio           : {debt_ratio:.1%}")
    print(f"   - Loan Amount          : ${loan_amount:,.2f}")
    print(
        f"   - Loan-to-Income (LTI) : "
        f"{result['inputs']['loan_to_income']:.2f}x"
    )
    print(
        f"   - Disposable Income    : "
        f"${result['inputs']['disposable_income']:,.2f}/yr"
    )
    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
