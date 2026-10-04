#!/usr/bin/env python3
"""Merge validated PMS outcomes with ACS and CDC PLACES covariates."""

import csv
import importlib.util
import json
import sys
from pathlib import Path

from config import COUNTIES, PLACES_MEASURES, PROCESSED_DIR, RAW_DIR


def load_validator():
    path = Path(__file__).with_name("01_validate_pms_outcome.py")
    spec = importlib.util.spec_from_file_location("pms_validator", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def require(path: Path) -> None:
    if not path.exists():
        raise RuntimeError(f"Required source is missing: {path.relative_to(RAW_DIR.parent)}")


def load_acs(path: Path) -> dict[str, dict[str, float | str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    header = payload[0]
    records = [dict(zip(header, row)) for row in payload[1:]]
    output = {}
    for row in records:
        fips = row["state"] + row["county"]
        education_total = float(row["B15003_001E"])
        bachelor_plus = sum(float(row[f"B15003_0{code}E"]) for code in range(22, 26))
        poverty_total = float(row["B17001_001E"])
        output[fips] = {
            "median_household_income_usd": float(row["B19013_001E"]),
            "median_household_income_moe": float(row["B19013_001M"]),
            "poverty_rate_pct": 100 * float(row["B17001_002E"]) / poverty_total,
            "bachelors_or_higher_pct": 100 * bachelor_plus / education_total,
        }
    if set(output) != set(COUNTIES):
        raise RuntimeError("ACS source does not contain exactly the 58 California counties")
    return output


def load_places(path: Path) -> dict[str, dict[str, float]]:
    output: dict[str, dict[str, float]] = {fips: {} for fips in COUNTIES}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            label = row["short_question_text"]
            if (
                label in PLACES_MEASURES
                and row["data_value_type"] == "Age-adjusted prevalence"
                and row["locationid"] in output
                and row["data_value"].strip()
            ):
                output[row["locationid"]][PLACES_MEASURES[label]] = float(row["data_value"])
    expected = set(PLACES_MEASURES.values())
    incomplete = {fips: sorted(expected - set(values)) for fips, values in output.items() if set(values) != expected}
    if incomplete:
        raise RuntimeError(f"CDC PLACES measures are incomplete: {incomplete}")
    return output


def main() -> int:
    validator = load_validator()
    try:
        pms_rows = validator.validate()
        acs_path = RAW_DIR / "acs_2024_ca_counties.json"
        places_path = RAW_DIR / "cdc_places_2025_ca.csv"
        require(acs_path)
        require(places_path)
        acs = load_acs(acs_path)
        places = load_places(places_path)
    except (RuntimeError, validator.ValidationError) as exc:
        print(f"ANALYTIC FILE NOT CREATED: {exc}", file=sys.stderr)
        return 1

    rows = []
    for pms in pms_rows:
        fips = pms["county_fips"].zfill(5)
        rows.append({**pms, **acs[fips], **places[fips]})

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    target = PROCESSED_DIR / "ca_county_pms_analysis.csv"
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Created {target.relative_to(PROCESSED_DIR.parent)} with 58 validated county rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

