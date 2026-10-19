# Model Selection Memo: Titanic Survival Prediction

**To:** Team Lead  
**From:** Data Science Intern  
**Subject:** Recommendation for the production baseline

## 1. Recommendation

I recommend **XGBoost** as the candidate for the next stage of evaluation.

**Strongest reason:** XGBoost achieved a test ROC-AUC of 0.8737, compared with 0.8352 for Random Forest, a measured advantage of 0.0385.

The measured test ROC-AUC margin is 0.0385. This comparison uses one held-out test split, so the margin should be confirmed on additional data before production deployment.

## 2. Evaluation Results

Both models were evaluated on the same held-out test set. The train–test gap is calculated as training ROC-AUC minus test ROC-AUC.

| Metric | Random Forest | XGBoost |
|---|---:|---:|
| Training ROC-AUC | 1.0000 | 0.8778 |
| Test ROC-AUC | 0.8352 | 0.8737 |
| Train–test gap | 0.1648 | 0.0041 |

A larger positive gap suggests a greater difference between fitting performance and held-out performance. A small gap alone does not prove that a model generalizes well; the test score also matters.

## 3. Recommended Model Hyperparameters

- `n_estimators` (maximum rounds): 1000
- `learning_rate`: 0.1
- `max_depth`: 3
- `eval_metric`: logloss
- `early_stopping_rounds`: 30
- `random_state`: 42

**Tree-count decision:** 43 trees used: best iteration was 42 (zero-based). The model was allowed up to 1000 boosting rounds, with early stopping after 30 rounds without improvement on validation log loss.

## 4. Main Predictive Features

- **Random Forest top three:** sex_male, fare, pclass
- **XGBoost top three:** sex_male, fare, pclass

The models agree on the same top-three features, although their ranking order may differ.

These features were identified using permutation importance with ROC-AUC scoring and 20 repeats. Importance indicates predictive reliance, not that a feature causes survival.

## 5. Main Risk

The recommendation is based on a single train/test split, and the test ROC-AUC was used to choose between the two candidates. This can make the apparent winning margin optimistic. The selected model may perform differently on new passengers or data collected under different conditions.

## 6. Next Test

I would evaluate both models using repeated stratified cross-validation, comparing mean ROC-AUC and its variability. I would then validate the selected model on a separate, untouched dataset and assess calibration and the consequences of false predictions before production deployment.

## 7. Final Decision

XGBoost is the current candidate based on the measured test ROC-AUC comparison. This is a recommendation for further validation, not a claim that production readiness has already been established.
