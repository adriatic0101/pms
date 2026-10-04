# California PMS, Social Determinants, and Lifestyle Study

## Research question

> To what extent are social determinants of health and lifestyle factors associated with PMS symptom severity among reproductive-aged women across California's 58 counties?

## Current status: outcome data unavailable

This repository is a reproducible, county-level ecological analysis project. It is **not currently possible to answer the research question** with the public data sources identified in the source audit.

Authoritative sources provide county-level measures for income, poverty, education, food insecurity, sleep, physical inactivity, and healthcare access. However, the audit did **not** identify a public dataset that provides a validated PMS severity or prevalence measure for reproductive-aged women in all 58 California counties.

No PMS values are estimated, simulated, imputed, or replaced with menstrual irregularity, PMDD proxies, general mental health, or another outcome. The analysis pipeline stops unless a real outcome file passes strict validation.

## Required dependent variable

The preferred outcome is one of the following, measured in a defined population of reproductive-aged women and available for all 58 counties:

- a continuous score from a validated PMS instrument, such as the Premenstrual Symptoms Screening Tool (PSST);
- PMS prevalence based on validated PSST criteria; or
- prospectively assessed symptom severity or prevalence using the Daily Record of Severity of Problems (DRSP).

A screening result must not be described as a clinical diagnosis. A county estimate must include its source, survey period, eligible denominator, population definition, and uncertainty measure.

## Candidate independent variables

| Domain | County measure | Planned source |
|---|---|---|
| Economic resources | Median household income | 2024 ACS 5-year, B19013 |
| Economic hardship | Poverty rate | 2024 ACS 5-year, B17001 |
| Education | Bachelor's degree or higher among adults 25+ | 2024 ACS 5-year, B15003 |
| Food access | Adult food insecurity prevalence | CDC PLACES 2025 |
| Sleep | Adult short sleep duration prevalence | CDC PLACES 2025 |
| Physical activity | Adult leisure-time physical inactivity prevalence | CDC PLACES 2025 |
| Healthcare access | Lack of health insurance among adults 18–64 | CDC PLACES 2025 |

These covariates describe county populations and do not necessarily match the age/sex population of a future PMS outcome. That mismatch must be treated as a limitation.

## Repository structure

```text
raw_data/          Source files exactly as downloaded or received
processed_data/    County-level analytic file, created only after validation
analysis_scripts/  Download, validation, merge, and analysis programs
website/           Static project-status and methods page
figures_maps/      Generated plots and maps
documentation/     Data audit, analysis plan, sources, and data dictionary
```

## Reproducible workflow

1. Install Python 3.11+ and dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

2. Download public covariates. The Census API currently requires a key:

   ```bash
   export CENSUS_API_KEY="your-key"
   python analysis_scripts/00_download_covariates.py
   ```

3. Place an authorized, non-synthetic PMS outcome file at `raw_data/pms_outcome.csv`. Its required fields are documented in `documentation/data_dictionary.md`.

4. Validate the outcome before any merge or analysis:

   ```bash
   python analysis_scripts/01_validate_pms_outcome.py
   ```

5. Build and analyze only after validation succeeds:

   ```bash
   python analysis_scripts/02_build_analysis_dataset.py
   python analysis_scripts/03_analyze.py
   ```

Without a valid PMS file, steps 4–5 intentionally fail with a clear explanation.

## Intended analysis

- Describe geographic coverage, missingness, denominators, and estimate precision.
- Map the validated PMS outcome and each exposure without ranking counties.
- Estimate bivariate Spearman correlations.
- Fit prespecified ecological linear models using standardized predictors and HC3 robust standard errors.
- Diagnose multicollinearity and report uncertainty, sensitivity checks, and multiple-testing context.
- Interpret all results as county-level associations, not individual-level or causal effects.

See [documentation/analysis_plan.md](documentation/analysis_plan.md) for the full plan and [documentation/data_availability_audit.md](documentation/data_availability_audit.md) for the source audit.

## Important legacy notice

The existing `dashboard/` git-linked artifact predates this research design and used explicitly synthetic PMS values. It is **excluded from this study** and must not be used as evidence, input, or output for this project.
