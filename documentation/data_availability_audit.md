# Data availability audit

Audit date: 2026-10-04

## Decision

No public source identified in this audit supports a validated PMS severity or PMS prevalence estimate for reproductive-aged women in each of California's 58 counties. The study is therefore blocked at the dependent-variable stage.

This is a substantive missing-data problem, not an invitation to manufacture a county outcome. The project does not use menstrual irregularity, depression, frequent mental distress, pelvic pain, PMDD-related search behavior, or general reproductive-health indicators as substitutes for PMS.

## Outcome sources reviewed

### California Health Interview Survey (CHIS)

CHIS is California's largest state health survey and provides questionnaires, public-use files, and restricted-access options. Its public survey-topic and questionnaire materials were reviewed as a plausible state-specific source. The audit did not identify a repeated validated PMS instrument or a public all-county PMS estimate. If UCLA confirms an appropriate restricted variable exists, county identifiers and sample sufficiency would still need formal review.

Source: https://healthpolicy.ucla.edu/our-work/california-health-interview-survey-chis

### CDC PLACES and BRFSS-derived county estimates

PLACES provides county-level small-area estimates for health outcomes, behaviors, access, and social needs. Its 2025 release contains 40 measures, including short sleep, physical inactivity, food insecurity, and health insurance. PMS is not a PLACES measure.

Sources:

- https://www.cdc.gov/places/about/
- https://www.cdc.gov/places/measure-definitions/index.html
- https://data.cdc.gov/d/swc5-untb

### Validated PMS instruments

The Premenstrual Symptoms Screening Tool (PSST) is a validated screening instrument that measures symptom severity and functional impairment. The Daily Record of Severity of Problems (DRSP) prospectively records symptoms across cycles and is useful for more rigorous case identification. Validation publications establish instruments; they do not supply California county estimates.

Sources:

- Steiner et al. PSST: https://pubmed.ncbi.nlm.nih.gov/12920618/
- PSST compared with DRSP: https://pubmed.ncbi.nlm.nih.gov/29132173/

## Available explanatory data

### American Community Survey

The 2024 ACS 5-year detailed tables cover all counties and support income, poverty, and education measures with margins of error. The acquisition script uses B19013, B17001, and B15003.

Source: https://api.census.gov/data/2024/acs/acs5.html

### CDC PLACES

The 2025 county release supports age-adjusted adult prevalence estimates for food insecurity, short sleep duration, physical inactivity, and lack of health insurance. These are model-based ecological estimates and are not restricted to reproductive-aged women.

Source: https://data.cdc.gov/d/swc5-untb

## What would unblock the project

A qualifying dataset must:

1. use a documented validated PMS measure such as PSST or DRSP;
2. represent reproductive-aged women under a clearly stated age and eligibility definition;
3. identify California county of residence using five-digit FIPS codes;
4. cover all 58 counties or provide a defensible, prespecified missing-county strategy;
5. include denominators, survey years, weights/design information where applicable, and uncertainty estimates; and
6. permit county-level analysis under its data-use agreement.

If no existing dataset qualifies, the appropriate next step is primary data collection with adequate county sampling—not modeled or fabricated PMS values.
