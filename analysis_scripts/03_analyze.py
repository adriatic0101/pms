#!/usr/bin/env python3
"""Run the prespecified county-level analysis after the PMS data gate passes."""

import importlib.util
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from scipy.stats import spearmanr
from statsmodels.stats.outliers_influence import variance_inflation_factor

from config import FIGURES_DIR, PROCESSED_DIR

OUTCOME = "estimate"
PRIMARY = ["median_household_income_usd", "poverty_rate_pct", "bachelors_or_higher_pct"]
SECONDARY = ["food_insecurity_pct", "short_sleep_pct", "physical_inactivity_pct", "uninsured_18_64_pct"]
ANALYTIC_PATH = PROCESSED_DIR / "ca_county_pms_analysis.csv"


def load_validator():
    path = Path(__file__).with_name("01_validate_pms_outcome.py")
    spec = importlib.util.spec_from_file_location("pms_validator", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def fit_model(df: pd.DataFrame, predictors: list[str], name: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    standardized = df[predictors].apply(lambda column: (column - column.mean()) / column.std(ddof=1))
    design = sm.add_constant(standardized)
    fit = sm.OLS(df[OUTCOME], design).fit(cov_type="HC3")
    intervals = fit.conf_int()
    coefficients = pd.DataFrame(
        {
            "model": name,
            "term": fit.params.index,
            "estimate": fit.params.values,
            "std_error_hc3": fit.bse.values,
            "ci_lower": intervals[0].values,
            "ci_upper": intervals[1].values,
            "p_value": fit.pvalues.values,
            "r_squared": fit.rsquared,
            "n_counties": int(fit.nobs),
        }
    )
    vif = pd.DataFrame(
        {
            "model": name,
            "term": predictors,
            "vif": [variance_inflation_factor(standardized.values, i) for i in range(len(predictors))],
        }
    )
    return coefficients, vif


def main() -> int:
    validator = load_validator()
    try:
        validator.validate()
    except validator.ValidationError as exc:
        print(f"ANALYSIS BLOCKED: {exc}", file=sys.stderr)
        return 1
    if not ANALYTIC_PATH.exists():
        print("ANALYSIS BLOCKED: run 02_build_analysis_dataset.py first", file=sys.stderr)
        return 1

    df = pd.read_csv(ANALYTIC_PATH, dtype={"county_fips": str})
    predictors = PRIMARY + SECONDARY
    required = [OUTCOME, "county_name", "n_eligible"] + predictors
    if df[required].isna().any().any() or len(df) != 58:
        print("ANALYSIS BLOCKED: analytic data must have 58 complete county rows", file=sys.stderr)
        return 1

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    df[[OUTCOME] + predictors].describe().T.to_csv(PROCESSED_DIR / "descriptive_summary.csv")

    correlations = []
    for predictor in predictors:
        result = spearmanr(df[predictor], df[OUTCOME])
        correlations.append(
            {"predictor": predictor, "spearman_rho": result.statistic, "p_value": result.pvalue, "n_counties": len(df)}
        )
    pd.DataFrame(correlations).to_csv(PROCESSED_DIR / "spearman_correlations.csv", index=False)

    coefficient_tables, vif_tables = [], []
    for name, terms in (("A_social_determinants", PRIMARY), ("B_lifestyle_access", SECONDARY), ("C_exploratory_all", predictors)):
        coefficients, vif = fit_model(df, terms, name)
        coefficient_tables.append(coefficients)
        vif_tables.append(vif)
    pd.concat(coefficient_tables).to_csv(PROCESSED_DIR / "model_coefficients.csv", index=False)
    pd.concat(vif_tables).to_csv(PROCESSED_DIR / "model_vif.csv", index=False)

    sns.set_theme(style="whitegrid")
    figure, axes = plt.subplots(3, 3, figsize=(15, 14))
    for axis, predictor in zip(axes.flat, predictors):
        sns.regplot(data=df, x=predictor, y=OUTCOME, ax=axis, ci=None, scatter_kws={"alpha": 0.75})
        axis.set_title(predictor.replace("_", " ").title())
    for axis in axes.flat[len(predictors):]:
        axis.remove()
    figure.suptitle("County-level associations with validated PMS outcome", fontsize=16)
    figure.tight_layout()
    figure.savefig(FIGURES_DIR / "bivariate_associations.png", dpi=200, bbox_inches="tight")
    plt.close(figure)
    print("Analysis complete. Interpret results as ecological associations, not causal effects.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
