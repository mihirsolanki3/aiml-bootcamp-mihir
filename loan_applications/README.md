# AI Loan Repayment Prediction System

This project predicts whether a loan applicant will **repay their loan** (`repaid = 1`) or **default** (`repaid = 0`) based on 5 financial features extracted from [`loan_applications.csv`](loan_applications.csv):

1. **`income`**: Annual gross income ($)
2. **`years_employed`**: Total years employed
3. **`credit_score`**: Credit score (300 – 850)
4. **`debt_ratio`**: Debt-to-income ratio (e.g., `0.25` or `25%`)
5. **`loan_amount`**: Requested loan amount ($)

---

## 🚀 Quick Start Guide

### 1. Predict From Your Own Inputs (Interactive Terminal)
Run the dedicated script to type your own values into the terminal:

```powershell
python user_predict.py
```
*(Or run `python predict.py`)*

You will be asked to enter:
1. **Annual Income ($)**
2. **Years Employed**
3. **Credit Score (300-850)**
4. **Debt-to-Income Ratio (e.g. 0.25 or 25%)**
5. **Loan Amount ($)**

Example session:
```text
1. Annual Income ($) [e.g. 65000]: 85000
2. Years Employed [e.g. 5.5]: 8
3. Credit Score (300 - 850) [e.g. 720]: 750
4. Debt-to-Income Ratio (0.0 to 1.0 or %) [e.g. 0.25]: 0.15
5. Loan Amount Requested ($) [e.g. 35000]: 25000

==============================================================
           LOAN REPAYMENT PREDICTION RESULT           
==============================================================
 Decision         : Will Repay (Approved)
 Risk Level       : Low Risk
 Repayment Chance : 59.7%
 Default Chance   : 40.3%
 Recommendation   : Strong Approval - Above-average repayment probability.
--------------------------------------------------------------
 Key Drivers:
   * Income          : Positive (Improves Repayment Chance)
   * Years Employed  : Positive (Improves Repayment Chance)
   * Credit Score    : Positive (Improves Repayment Chance)
   * Debt Ratio      : Positive (Improves Repayment Chance)
   * Loan Amount     : Positive (Improves Repayment Chance)
==============================================================
```

---

### 2. Direct CLI Arguments
You can also run instant one-liner evaluations:

```powershell
python predict.py --income 90000 --years 7 --credit 740 --debt 0.18 --loan 30000
```

---

### 3. Interactive Web Application
Launch the visual dashboard locally:

```powershell
python app.py
```
Then open [http://localhost:5000](http://localhost:5000) in your web browser. Features include:
- Clean, responsive UI with dark mode
- Quick preset buttons (*Prime*, *Average*, *High-Risk*)
- Real-time probability bar and risk rating
- Feature influence summary (favorable vs unfavorable factors)
- Adjustable decision threshold slider

---

### 4. Python Programmatic Import
You can import the prediction engine directly into any Python script or Jupyter Notebook:

```python
from predict import predict_loan_repayment

result = predict_loan_repayment(
    income=75000,
    years_employed=6.0,
    credit_score=720,
    debt_ratio=0.22,
    loan_amount=35000,
    threshold=0.50
)

print("Decision:", result["prediction"])
print("Repayment Likelihood:", result["repaid_percentage"])
print("Risk Level:", result["risk_level"])
```

---

## 📊 Model Details & Architecture

- **Pipeline**: `StandardScaler()` followed by `LogisticRegression(class_weight={0: 1.0, 1: 1.6}, max_iter=1000)`
- **Evaluation Metrics (Test Set at Optimal 0.45 Threshold)**:
  - Accuracy: `74.58%` (up from 66.08%)
  - Precision: `50.74%` (up from 39.92%)
  - Recall: `44.34%`
  - F1-Score: `0.4732`
  - ROC AUC: `70.25%`
- **Engineered Financial Features**:
  - `loan_to_income`: Loan principal requested relative to annual income (Leverage)
  - `debt_burden`: Monthly EMI burden vs monthly salary (EMI stress)
  - `credit_to_debt`: Credit score resilience relative to existing debt
  - `disposable_income`: Net annual cash flow after servicing current debts
- **Feature Coefficients (Key Drivers)**:
  - `credit_score` (+0.5352): Strongest positive predictor of repayment
  - `years_employed` (+0.3526): Career stability improves repayment
  - `disposable_income` (+0.1957): Positive cash flow boosts repayment capacity
  - `income` (+0.1169): Higher gross salary improves repayment
  - `credit_to_debt` (+0.0477): Favorable credit buffer
  - `debt_ratio` (-0.1031): Higher existing obligations increase default risk
  - `loan_amount` (-0.2529): Larger principal increases repayment burden
  - `loan_to_income` (-0.0317) & `debt_burden` (-0.0317): Excessive leverage stress

---

## 📁 Repository Files

| File | Description |
| :--- | :--- |
| [`loan_applications.csv`](loan_applications.csv) | Source dataset containing 6,000 historical loan applications |
| [`train_model.py`](train_model.py) | Training script that trains the pipeline and exports the model artifact |
| [`predict.py`](predict.py) | Prediction engine supporting CLI wizard, arguments, and module import |
| [`app.py`](app.py) | Zero-dependency local web app server with UI and REST API |
| [`test_predictions.py`](test_predictions.py) | Verification test suite running 5 diverse financial profiles |
| [`loan_repayment_model.joblib`](loan_repayment_model.joblib) | Serialized trained model pipeline |
| [`model_metadata.json`](model_metadata.json) | Saved model metrics, coefficients, and distribution stats |
