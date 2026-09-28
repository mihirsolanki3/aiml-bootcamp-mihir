# Ames Housing EDA Capstone

This project is an end-to-end exploratory data analysis of Ames, Iowa residential sale prices, aimed at identifying which property characteristics are most strongly associated with sale price.

## Question and headline finding

**Question:** What property characteristics are most strongly associated with residential sale prices in Ames, and what unusual observations or data-quality issues should be considered when interpreting those relationships?

**Headline finding:** Overall property quality is the single strongest driver of sale price in this dataset (Spearman ρ = 0.79, p < .0001), followed by above-ground living area (r = 0.60). Neighborhood also matters a great deal, with median prices ranging from about $167,000 to $373,000 across neighborhoods (Kruskal-Wallis H = 1142.99, ε² = 0.78). Living area only translates into higher price at the rate a property's quality allows — two of the largest homes in the dataset sold well below the market's typical price because they were only medium quality, not because size stopped mattering.

## Dataset

**Source:** Ames, Iowa residential sales data (derived from Ames city assessor records; widely used for teaching, e.g. via Kaggle's "Ames Housing" datasets). This project uses an 11-column extract of 1,460 property sales: `Id`, `Neighborhood`, `OverallQual`, `GrLivArea`, `YearBuilt`, `Bedrooms`, `FullBath`, `GarageCars`, `LotArea`, `SalePrice`, and `LotFrontage`.

**Condition on arrival:** 248 `LotFrontage` values (17.0%) were missing; no duplicate rows, no duplicate `Id` values, and no impossible values (negative counts, non-positive areas/prices, out-of-range quality scores) were found.

## Main cleaning decisions

- **`LotFrontage` missing values (17.0%):** filled with neighborhood-median imputation (overall-median fallback, not needed here) rather than dropping rows or using one overall median, because missingness is concentrated unevenly by neighborhood and this approach keeps all 1,460 rows while changing the variable's spread only modestly (std 19.98 vs. an observed 21.90).
- **Duplicates:** none found; no rows removed.
- **Outliers:** two very large homes (Id 1016, Id 858; over 4,500 sq ft) were investigated individually rather than deleted — both pass domain-validity checks and turn out to explain a genuine pattern (size only pays off at the rate a property's quality allows) rather than being data errors.
- **`Id`:** retained only as an identifier, excluded from correlation/statistical analysis.

## Repository contents

- `notebooks/Ames_Housing_EDA_Capstone.ipynb` — the full, executed analysis notebook.
- `report/Ames_Housing_Capstone_Report.pdf` — the two-page written report.
- `figures/` — ten exported, captioned visualizations.
- `data/ames_housing.csv` — the raw dataset.

## How to run

```bash
pip install -r requirements.txt
jupyter notebook notebooks/Ames_Housing_EDA_Capstone.ipynb
```

Run all cells top to bottom from a fresh kernel. The dataset must be present at `data/ames_housing.csv` (already included here). Figures are regenerated into `figures/` when the notebook is run.
