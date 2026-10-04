# ACS county socioeconomic dataset

## Release and geography

The dataset uses the **2024 American Community Survey 5-Year Estimates**, the
most recent mutually available ACS 5-year release for all requested measures.
It contains all 58 California counties (state FIPS `06`, county geography).

The reproducible Census API endpoint is:

`https://api.census.gov/data/2024/acs/acs5?get=NAME,B19013_001E,B17001_001E,B17001_002E,B15003_001E,B15003_022E,B15003_023E,B15003_024E,B15003_025E,B23025_003E,B23025_005E,B27001_001E,B27001_005E,B27001_008E,B27001_011E,B27001_014E,B27001_017E,B27001_020E,B27001_023E,B27001_026E,B27001_029E,B27001_033E,B27001_036E,B27001_039E,B27001_042E,B27001_045E,B27001_048E,B27001_051E,B27001_054E,B27001_057E&for=county:*&in=state:06&key=YOUR_KEY`

At collection time the API required a key and none was configured locally.
The saved files were therefore built from the Census Bureau's official 2024
table-based ACS 5-year summary files for B19013, B17001, B15003, B23025, and
B27001. These contain the same detailed-table estimates requested by the API
endpoint above. The exact source files were:

- `https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/acsdt5y2024-b19013.dat`
- `https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/acsdt5y2024-b17001.dat`
- `https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/acsdt5y2024-b15003.dat`
- `https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/acsdt5y2024-b23025.dat`
- `https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/acsdt5y2024-b27001.dat`

## Variables and calculations

| Output | ACS table/variables | Definition and cleaning |
|---|---|---|
| `median_household_income` | `B19013_001E` | Median household income in 2024 inflation-adjusted dollars; direct estimate. |
| `poverty_rate` | `B17001_002E / B17001_001E` | People below the poverty level divided by the population for whom poverty status is determined, times 100. |
| `bachelors_or_higher` | (`B15003_022E` + `B15003_023E` + `B15003_024E` + `B15003_025E`) / `B15003_001E` | Adults age 25+ whose highest attainment is bachelor's, master's, professional, or doctorate, divided by all adults age 25+, times 100. |
| `unemployment_rate` | `B23025_005E / B23025_003E` | Unemployed civilian labor force divided by the civilian labor force, times 100. |
| `uninsured_rate` | uninsured cells in `B27001` / `B27001_001E` | People with no health insurance across all B27001 age/sex groups, divided by the civilian noninstitutionalized population, times 100. Uninsured cells: `005`, `008`, `011`, `014`, `017`, `020`, `023`, `026`, `029`, `033`, `036`, `039`, `042`, `045`, `048`, `051`, `054`, and `057`. |

The raw CSV is a lossless California-county and requested-variable extract of
published Census estimate cells, plus geography fields; no rates are present.
In bulk-file mode, `NAME` is reconstructed from the repository's complete
California county FIPS crosswalk because table-based files contain `GEO_ID`
rather than `NAME`.
The cleaned CSV removes " County, California" from names, combines state and
county codes into a five-character FIPS string, calculates the four percentages,
and rounds percentages to one decimal place. The income estimate remains an
integer. No values are imputed or fabricated. The script stops on missing or
negative Census special values; a zero denominator would produce a blank rate.
Margins of error are not included in this requested point-estimate dataset.

## Reproduction

With a Census API key:

```bash
export CENSUS_API_KEY="your-key"
python3 analysis_scripts/00_download_acs_socioeconomic.py
```

With the five official table files downloaded into `/tmp/acs_bulk`:

```bash
python3 analysis_scripts/00_download_acs_socioeconomic.py --bulk-dir /tmp/acs_bulk
```
