# Raw data

This directory is reserved for unmodified source files.

Expected files after running the acquisition script:

- `acs_2024_ca_counties.json` — U.S. Census Bureau ACS 2024 5-year county response.
- `cdc_places_2025_ca.csv` — CDC PLACES 2025 California county rows.
- `pms_outcome.csv` — **not provided**. This must be a real, authorized dataset using a validated PMS measure and meeting the schema in `documentation/data_dictionary.md`.

Raw data are ignored by Git to avoid accidentally committing restricted participant or licensed data. Never place person-level identifiers in this repository.
