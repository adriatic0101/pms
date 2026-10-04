# Data dictionary

## Required PMS outcome file

Path: `raw_data/pms_outcome.csv`

One row per California county; exactly 58 rows.

| Field | Type | Requirement |
|---|---|---|
| `county_fips` | string | Five digits; California state prefix `06` |
| `county_name` | string | Official county name without the word “County” |
| `outcome_name` | string | PMS severity or PMS prevalence |
| `instrument` | string | Validated measure, e.g. `PSST` or `DRSP` |
| `estimate_type` | string | `mean_score` or `prevalence_pct` |
| `estimate` | number | Observed survey estimate; never synthetic or imputed |
| `standard_error` | number | Design-appropriate standard error |
| `ci_lower` | number | Lower confidence limit |
| `ci_upper` | number | Upper confidence limit |
| `n_eligible` | integer | Eligible respondents contributing to county estimate |
| `survey_year_start` | integer | First survey year represented |
| `survey_year_end` | integer | Last survey year represented |
| `population_definition` | string | Age range, menstruation/eligibility criteria, exclusions |
| `source_citation` | string | Full dataset or study citation |
| `source_url` | string | Persistent source or catalog URL |

The validator rejects missing counties, duplicate FIPS codes, unsupported instruments, nonnumeric estimates, absent provenance, impossible confidence intervals, and text indicating synthetic or fabricated data.

## Processed analytic fields

The merge script adds:

- `median_household_income_usd` and ACS margin of error;
- `poverty_rate_pct`;
- `bachelors_or_higher_pct` among adults age 25+;
- `food_insecurity_pct`;
- `short_sleep_pct`;
- `physical_inactivity_pct`; and
- `uninsured_18_64_pct`.

CDC PLACES fields are age-adjusted model-based prevalence estimates. ACS derived percentages retain numerator and denominator margins of error in the raw response but the first-pass pipeline does not propagate ratio margins of error.
