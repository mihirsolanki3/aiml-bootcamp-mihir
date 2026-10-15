# Day27 — Model Recommendation Memo

## 1. Objective

The objective was to predict Titanic passenger survival (`survived`: 0 = did not survive, 1 = survived) using 1,000 passenger records and six features: passenger class, sex, age, siblings/spouses aboard, parents/children aboard, and fare. Missing age and fare values were handled using median-based imputation.

## 2. Model choice

Random Forest is a suitable baseline because it combines multiple decision trees, captures nonlinear patterns and feature interactions, and does not require feature scaling. It also supports out-of-bag (OOB) evaluation and feature-importance analysis. However, it should be compared with simpler models before selecting a final approach.

## 3. Evaluation

- **Final test accuracy:** 0.7300 (73.0%)
- **Final test ROC-AUC:** 0.8315
- **OOB score:** approximately 0.7088 (70.88%)
- **Stability:** Across 25 bootstrap repeats, the Random Forest achieved a mean test ROC-AUC of 0.8240 with a standard deviation of 0.0187.

The ROC-AUC indicates useful ranking ability, but test accuracy and OOB score show that performance is not perfect. The stability result comes from bootstrap repeats, not a dedicated repeated-random-seed experiment.

## 4. Key findings

Permutation importance identified `sex_male` as the most influential feature, with a mean ROC-AUC decrease of 0.22256 when shuffled. `fare` ranked third, with a mean decrease of 0.02477. The PDP for `sex_male` shows a lower average predicted survival probability for males than females, while the fare PDP illustrates how the model’s predictions change as fare varies. These are learned associations, not evidence that either feature causes survival outcomes.

## 5. Risks and limitations

The dataset is historical and relatively small, so findings may not generalize to other populations. Median imputation can conceal uncertainty, and correlated features such as fare and passenger class can complicate interpretation. Impurity-based importance also gave random noise a relatively high rank (3rd of 7), despite its near-zero permutation importance (0.00263; 4th of 7). Finally, test metrics have sampling uncertainty, and the model raises fairness concerns if used for real-world decisions.

## 6. Recommendation

Keep Random Forest as a **baseline**, not a deployment-ready system. Next, run stratified cross-validation and compare ROC-AUC and probability calibration against logistic regression and gradient boosting before choosing a final model.