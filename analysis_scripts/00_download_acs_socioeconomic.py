#!/usr/bin/env python3
"""Create raw and cleaned 2024 ACS 5-year California county data.

By default, download detailed-table estimates from the Census API.  Pass
``--bulk-dir`` to read the same estimates from Census table-based summary
files named ``acsdt5y2024-<table>.dat``.
"""

import argparse
import csv
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

from config import COUNTIES, PROCESSED_DIR, RAW_DIR

YEAR = 2024
API_BASE = f"https://api.census.gov/data/{YEAR}/acs/acs5"
RAW_PATH = RAW_DIR / "acs_2024_5yr_ca_county_socioeconomic_raw.csv"
CLEAN_PATH = PROCESSED_DIR / "ca_county_socioeconomic_acs_2024.csv"

UNINSURED_VARIABLES = [
    f"B27001_{number:03d}E"
    for number in (5, 8, 11, 14, 17, 20, 23, 26, 29,
                   33, 36, 39, 42, 45, 48, 51, 54, 57)
]
VARIABLES = [
    "B19013_001E",
    "B17001_001E", "B17001_002E",
    "B15003_001E", "B15003_022E", "B15003_023E",
    "B15003_024E", "B15003_025E",
    "B23025_003E", "B23025_005E",
    "B27001_001E", *UNINSURED_VARIABLES,
]
TABLES = ("B19013", "B17001", "B15003", "B23025", "B27001")

# Some national summary-file records exceed Python's conservative CSV default.
csv.field_size_limit(10_000_000)


def fetch_api(api_key: str) -> list[dict[str, str]]:
    query = urllib.parse.urlencode(
        {
            "get": ",".join(["NAME", *VARIABLES]),
            "for": "county:*",
            "in": "state:06",
            "key": api_key,
        }
    )
    request = urllib.request.Request(
        f"{API_BASE}?{query}", headers={"User-Agent": "ca-pms-sdh-study/1.0"}
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        payload = json.loads(response.read().decode("utf-8"))
    header = payload[0]
    return [dict(zip(header, values)) for values in payload[1:]]


def bulk_column(api_variable: str) -> str:
    table, suffix = api_variable.split("_")
    return f"{table}_{suffix[-1]}{suffix[:-1]}"


def read_bulk(bulk_dir: Path) -> list[dict[str, str]]:
    by_fips: dict[str, dict[str, str]] = {}
    for table in TABLES:
        path = bulk_dir / f"acsdt5y{YEAR}-{table.lower()}.dat"
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.reader(handle, delimiter="|", quoting=csv.QUOTE_NONE)
            header = next(reader)
            for values in reader:
                row = dict(zip(header, values))
                geo_id = row["GEO_ID"]
                if not geo_id.startswith("0500000US06"):
                    continue
                fips = geo_id.removeprefix("0500000US")
                output = by_fips.setdefault(
                    fips,
                    {"NAME": f"{COUNTIES[fips]} County, California",
                     "state": "06", "county": fips[2:]},
                )
                for variable in VARIABLES:
                    if variable.startswith(table):
                        output[variable] = row[bulk_column(variable)]
    return list(by_fips.values())


def validate(rows: list[dict[str, str]]) -> None:
    fips = {row["state"] + row["county"] for row in rows}
    if len(rows) != 58 or fips != set(COUNTIES):
        raise RuntimeError(
            f"Expected all 58 California counties; received {len(rows)} rows "
            f"and {len(fips)} unique county FIPS codes"
        )
    for row in rows:
        for variable in VARIABLES:
            value = row.get(variable, "")
            if value in {"", "null", None}:
                raise RuntimeError(
                    f"Missing Census estimate {variable} for {row['NAME']}"
                )
            if int(value) < 0:
                raise RuntimeError(
                    f"Census special value {value} for {variable} in {row['NAME']}"
                )


def write_raw(rows: list[dict[str, str]]) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    fields = ["NAME", *VARIABLES, "state", "county"]
    with RAW_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda row: row["county"]))


def rate(numerator: int, denominator: int) -> str:
    if denominator <= 0:
        return ""
    return f"{100 * numerator / denominator:.1f}"


def write_clean(rows: list[dict[str, str]]) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    fields = [
        "county", "county_fips", "median_household_income", "poverty_rate",
        "bachelors_or_higher", "unemployment_rate", "uninsured_rate", "year",
    ]
    with CLEAN_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in sorted(rows, key=lambda item: item["county"]):
            poverty = rate(int(row["B17001_002E"]), int(row["B17001_001E"]))
            bachelors = rate(
                sum(int(row[f"B15003_{number:03d}E"]) for number in range(22, 26)),
                int(row["B15003_001E"]),
            )
            unemployment = rate(int(row["B23025_005E"]), int(row["B23025_003E"]))
            uninsured = rate(
                sum(int(row[variable]) for variable in UNINSURED_VARIABLES),
                int(row["B27001_001E"]),
            )
            writer.writerow(
                {
                    "county": COUNTIES[row["state"] + row["county"]],
                    "county_fips": row["state"] + row["county"],
                    "median_household_income": row["B19013_001E"],
                    "poverty_rate": poverty,
                    "bachelors_or_higher": bachelors,
                    "unemployment_rate": unemployment,
                    "uninsured_rate": uninsured,
                    "year": YEAR,
                }
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bulk-dir",
        type=Path,
        help="Directory containing official Census table-based .dat files",
    )
    args = parser.parse_args()
    if args.bulk_dir:
        rows = read_bulk(args.bulk_dir)
    else:
        api_key = os.getenv("CENSUS_API_KEY", "").strip()
        if not api_key:
            raise SystemExit("Set CENSUS_API_KEY or provide --bulk-dir")
        rows = fetch_api(api_key)
    validate(rows)
    write_raw(rows)
    write_clean(rows)
    print(f"Wrote {len(rows)} rows to {RAW_PATH.relative_to(RAW_DIR.parent)}")
    print(f"Wrote {len(rows)} rows to {CLEAN_PATH.relative_to(PROCESSED_DIR.parent)}")


if __name__ == "__main__":
    main()
