# Week 5 - Linear Model Pipeline (script version of the notebook)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso, RidgeCV, LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline, make_pipeline

pd.set_option('display.width', 140)
RANDOM_STATE = 42

df = pd.read_csv('california_housing.csv')
print('shape:', df.shape)
df.head()

print(df.head().to_string())
print()
print(df.dtypes.to_string())
print()
print('missing values per column:')
print(df.isna().sum().to_string())
print('total missing:', df.isna().sum().sum())
print('duplicate rows:', df.duplicated().sum())

print(df.describe().T.round(3).to_string())

fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(df['MedHouseVal'], bins=40, edgecolor='white')
ax.set_title('Distribution of the target: median house value')
ax.set_xlabel('MedHouseVal (units of $100,000)')
ax.set_ylabel('number of districts')
plt.tight_layout()
plt.close()
print('target skew:', round(df['MedHouseVal'].skew(), 3))
print('rows capped at the max value of', df['MedHouseVal'].max(), ':', int((df['MedHouseVal'] == df['MedHouseVal'].max()).sum()))

X = df.drop(columns='MedHouseVal')
y = df['MedHouseVal']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE
)
print('X_train:', X_train.shape, '| X_test:', X_test.shape)
print('y_train:', y_train.shape, '| y_test:', y_test.shape)

baseline = DummyRegressor(strategy='mean')
base_scores = cross_val_score(baseline, X_train, y_train, cv=5)
print('baseline fold R2:', base_scores.round(4))
print('baseline CV R2  :', base_scores.mean().round(3))

lr = LinearRegression()
lr.fit(X_train, y_train)
plain_scores = cross_val_score(lr, X_train, y_train, cv=5)
print('plain LR CV R2:', plain_scores.mean().round(3))
print('baseline CV R2:', base_scores.mean().round(3))
print()
print('coef range:', lr.coef_.min().round(4), 'to', lr.coef_.max().round(4))
print()
print('RAW (unscaled) coefficients vs feature scale:')
raw = pd.DataFrame({'raw_coef': lr.coef_, 'feature_std': X_train.std().values}, index=X.columns)
raw['abs_coef'] = raw['raw_coef'].abs()
print(raw.round(5).to_string())

scaled_plain = make_pipeline(StandardScaler(), LinearRegression())
scaled_ridge = make_pipeline(StandardScaler(), Ridge())   # default alpha = 1.0
scaled_lasso = make_pipeline(StandardScaler(), Lasso())   # default alpha = 1.0

plain_cv = cross_val_score(scaled_plain, X_train, y_train, cv=5).mean()
ridge_cv = cross_val_score(scaled_ridge, X_train, y_train, cv=5).mean()
lasso_cv_default = cross_val_score(scaled_lasso, X_train, y_train, cv=5).mean()

print('Baseline CV     :', base_scores.mean().round(3))
print('Plain (scaled)  :', plain_cv.round(3))
print('Ridge  CV       :', ridge_cv.round(3))
print('Lasso  CV       :', lasso_cv_default.round(3))

scaled_ridge.fit(X_train, y_train)
scaled_lasso.fit(X_train, y_train)
scaled_plain.fit(X_train, y_train)

coef_table = pd.DataFrame({
    'Plain (scaled)': scaled_plain[-1].coef_,
    'Ridge (alpha=1)': scaled_ridge[-1].coef_,
    'Lasso (alpha=1)': scaled_lasso[-1].coef_,
}, index=X.columns)
print(coef_table.round(4).to_string())
print()
print('exact zeros -> Ridge:', int((scaled_ridge[-1].coef_ == 0).sum()),
      '| Lasso:', int((scaled_lasso[-1].coef_ == 0).sum()))

alphas = [0.0001, 0.001, 0.01, 0.1, 1, 10]

lasso_cv = make_pipeline(StandardScaler(), LassoCV(alphas=alphas, cv=5))
lasso_cv.fit(X_train, y_train)          # training part only

best_alpha = lasso_cv.named_steps['lassocv'].alpha_
lasso_coefs = lasso_cv.named_steps['lassocv'].coef_
print('Lasso best alpha :', best_alpha)
print('Lasso best CV R2 :', cross_val_score(lasso_cv, X_train, y_train, cv=5).mean().round(3))
print('zeroed coefficients:', int((lasso_coefs == 0).sum()), 'of', len(lasso_coefs))
print(pd.Series(lasso_coefs, index=X.columns).round(4).to_string())

# Mean CV R2 for every alpha in the grid (this is what LassoCV compares)
lcv = lasso_cv.named_steps['lassocv']
cv_curve = pd.DataFrame({'alpha': lcv.alphas_, 'mean_CV_MSE': lcv.mse_path_.mean(axis=1)}).sort_values('alpha')
print(cv_curve.to_string(index=False))

# Same honest tuning for Ridge so the comparison is fair
ridge_alphas = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
ridge_tuned = make_pipeline(StandardScaler(), RidgeCV(alphas=ridge_alphas, cv=5))
ridge_tuned.fit(X_train, y_train)
print('Ridge best alpha :', ridge_tuned.named_steps['ridgecv'].alpha_)
print('Ridge best CV R2 :', cross_val_score(ridge_tuned, X_train, y_train, cv=5).mean().round(3))

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LassoCV(alphas=alphas, cv=5)),
])
pipeline.fit(X_train, y_train)

pipeline_cv = cross_val_score(pipeline, X_train, y_train, cv=5)
print('Pipeline CV R2   :', pipeline_cv.mean().round(3))
print('Earlier Lasso CV :', cross_val_score(lasso_cv, X_train, y_train, cv=5).mean().round(3))
print('chosen alpha     :', pipeline.named_steps['model'].alpha_)
print(pipeline)

coefs = pipeline.named_steps['model'].coef_
coef_series = pd.Series(coefs, index=X.columns).sort_values(key=np.abs, ascending=False)
print(coef_series.round(4).to_string())

fig, ax = plt.subplots(figsize=(8, 6))
colors = ['tab:green' if c > 0 else 'tab:red' for c in coefs]
ax.bar(X.columns, coefs, color=colors)
ax.axhline(0, color='black', linewidth=0.8)
ax.set_title('Effect of each feature on median house value (tuned Lasso)')
ax.set_ylabel('coefficient (standardised)')
ax.set_xlabel('feature  (green = raises price, red = lowers price)')
ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
fig.savefig('coefficients.png', dpi=150, bbox_inches='tight')
plt.close()

# The ONLY time the test set is used: one evaluation of the chosen Pipeline.
final_test_score = pipeline.score(X_test, y_test)
print('FINAL test R2:', round(final_test_score, 3))

ridge_tuned_cv = cross_val_score(ridge_tuned, X_train, y_train, cv=5).mean()
lasso_tuned_cv = cross_val_score(pipeline, X_train, y_train, cv=5).mean()

comparison = pd.DataFrame({
    'Model': [
        'Baseline (DummyRegressor, mean)',
        'Plain LinearRegression',
        'Ridge (scaled, alpha=1)',
        'Lasso (scaled, alpha=1)',
        'Ridge tuned (RidgeCV)',
        'Lasso tuned (LassoCV)  <- final Pipeline',
    ],
    'Alpha': ['-', '-', 1, 1, ridge_tuned.named_steps['ridgecv'].alpha_, pipeline.named_steps['model'].alpha_],
    'CV R2 (train, 5-fold)': [base_scores.mean(), plain_scores.mean(), ridge_cv, lasso_cv_default, ridge_tuned_cv, lasso_tuned_cv],
    'Test R2 (final, once)': ['-', '-', '-', '-', '-', final_test_score],
})
comparison['CV R2 (train, 5-fold)'] = comparison['CV R2 (train, 5-fold)'].round(3)
comparison['Test R2 (final, once)'] = comparison['Test R2 (final, once)'].apply(lambda v: round(v, 3) if v != '-' else v)
print(comparison.to_string(index=False))
comparison.to_csv('comparison_table.csv', index=False)

cv_est = lasso_tuned_cv
gap = final_test_score - cv_est
print(f'CV estimate: {cv_est:.3f} | Test score: {final_test_score:.3f} | gap (test - CV): {gap:+.3f}')

from sklearn.metrics import mean_absolute_error, root_mean_squared_error
pred = pipeline.predict(X_test)
print('Test RMSE (x $100k):', round(root_mean_squared_error(y_test, pred), 3), '| MAE:', round(mean_absolute_error(y_test, pred), 3))

