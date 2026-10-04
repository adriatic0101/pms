# Prespecified analysis plan

## Design

Cross-sectional ecological study of California's 58 counties. The unit of analysis is the county, not the individual.

## Population and outcome

The target population is reproductive-aged women living in California. Analysis will begin only after obtaining a county-level outcome based on a validated PMS instrument. PSST-based screening prevalence and DRSP-based prospective severity are acceptable but should not be pooled as if they are identical constructs.

## Exposures

Primary social determinants:

1. median household income;
2. poverty rate; and
3. bachelor's degree or higher among adults 25+.

Secondary contextual/lifestyle measures:

1. food insecurity;
2. short sleep duration;
3. physical inactivity; and
4. lack of health insurance among adults 18–64.

All exposure directions and transformations will be set before viewing their relationship with PMS.

## Quality checks

- Confirm exactly 58 unique California county FIPS codes.
- Verify instrument, population, survey years, denominator, and provenance.
- Tabulate missingness and suppress estimates failing the source's reliability rules.
- Compare outcome and exposure periods; document temporal mismatch.
- Examine distributions, influential counties, and county sample sizes.
- Do not pool incompatible PMS instruments or change the outcome after seeing associations.

## Statistical analysis

1. Report medians, interquartile ranges, ranges, and maps.
2. Estimate Spearman rank correlations with two-sided confidence intervals or p-values.
3. Standardize continuous exposures to one standard deviation.
4. Fit Model A with the three primary social determinants.
5. Fit Model B with food insecurity, short sleep, physical inactivity, and uninsurance.
6. Fit the seven-predictor Model C as explicitly exploratory because 58 observations provide limited precision.
7. Use HC3 heteroskedasticity-robust standard errors.
8. Report variance inflation factors and influence diagnostics.
9. Run leave-one-county-out and denominator-weighted sensitivity analyses when weights are defensible.
10. Report estimates and confidence intervals; treat multiplicity-adjusted results as supportive rather than binary proof.

If the outcome is a prevalence, a generalized linear or weighted meta-regression sensitivity model may be preferable once denominator and standard-error properties are known.

## Interpretation boundaries

- Associations are ecological and cannot be interpreted as individual risk.
- Cross-sectional results cannot establish causation or temporal order.
- PLACES measures are modeled adult estimates and may not represent reproductive-aged women specifically.
- County borders can conceal within-county inequity.
- A sample of 58 counties limits statistical power and model complexity.
- Results should not be used to rank counties or diagnose individuals.
