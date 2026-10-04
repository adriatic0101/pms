#!/usr/bin/env python3
"""Strictly validate a real PMS county outcome before analysis."""

import csv
import json
import math
import re
import sys
from pathlib import Path

from config import (
    COUNTIES,
    PMS_ALLOWED_ESTIMATE_TYPES,
    PMS_ALLOWED_INSTRUMENTS,
    PMS_REQUIRED_FIELDS,
    RAW_DIR,
)

OUTCOME_PATH = RAW_DIR / "pms_outcome.csv"
RECEIPT_PATH = RAW_DIR / "pms_outcome.validation.json"
FORBIDDEN_PROVENANCE = re.compile(r"\b(synthetic|simulated|fabricated|dummy|mock)\b", re.I)


class ValidationError(RuntimeError):
    pass


def number(row: dict[str, str], field: str, line: int) -> float:
    try:
        value = float(row[field])
    except (TypeError, ValueError):
        raise ValidationError(f"Row {line}: {field} must be numeric") from None
    if not math.isfinite(value):
        raise ValidationError(f"Row {line}: {field} must be finite")
    return value


def validate(path: Path = OUTCOME_PATH) -> list[dict[str, str]]:
    if not path.exists():
        raise ValidationError(
            "No PMS outcome file exists. Add a real validated dataset at "
            "raw_data/pms_outcome.csv; synthetic substitutes are prohibited."
        )

    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        missing_fields = PMS_REQUIRED_FIELDS - fields
        if missing_fields:
            raise ValidationError(f"Missing required columns: {sorted(missing_fields)}")
        rows = list(reader)

    if len(rows) != 58:
        raise ValidationError(f"Expected exactly 58 county rows; found {len(rows)}")

    seen: set[str] = set()
    instruments: set[str] = set()
    estimate_types: set[str] = set()
    for line, row in enumerate(rows, start=2):
        joined = " ".join(str(value) for value in row.values())
        if FORBIDDEN_PROVENANCE.search(joined):
            raise ValidationError(f"Row {line}: prohibited synthetic/fabricated provenance")

        fips = row["county_fips"].strip().zfill(5)
        if fips not in COUNTIES:
            raise ValidationError(f"Row {line}: unknown California county FIPS {fips}")
        if fips in seen:
            raise ValidationError(f"Row {line}: duplicate county FIPS {fips}")
        seen.add(fips)
        if row["county_name"].strip() != COUNTIES[fips]:
            raise ValidationError(
                f"Row {line}: county name does not match {fips} ({COUNTIES[fips]})"
            )

        instrument = row["instrument"].strip().upper()
        if instrument not in PMS_ALLOWED_INSTRUMENTS:
            raise ValidationError(
                f"Row {line}: instrument must be one of {sorted(PMS_ALLOWED_INSTRUMENTS)}. "
                "Review and update the protocol before allowing another validated instrument."
            )
        instruments.add(instrument)
        estimate_type = row["estimate_type"].strip()
        if estimate_type not in PMS_ALLOWED_ESTIMATE_TYPES:
            raise ValidationError(f"Row {line}: unsupported estimate_type {estimate_type!r}")
        estimate_types.add(estimate_type)

        estimate = number(row, "estimate", line)
        standard_error = number(row, "standard_error", line)
        ci_lower = number(row, "ci_lower", line)
        ci_upper = number(row, "ci_upper", line)
        n_eligible = number(row, "n_eligible", line)
        year_start = number(row, "survey_year_start", line)
        year_end = number(row, "survey_year_end", line)
        if standard_error <= 0 or n_eligible <= 0:
            raise ValidationError(f"Row {line}: standard_error and n_eligible must be positive")
        if not ci_lower <= estimate <= ci_upper:
            raise ValidationError(f"Row {line}: estimate must fall within its confidence interval")
        if estimate_type == "prevalence_pct" and not (0 <= ci_lower <= ci_upper <= 100):
            raise ValidationError(f"Row {line}: prevalence confidence limits must be 0–100")
        if year_start > year_end:
            raise ValidationError(f"Row {line}: survey year range is reversed")
        for field in ("outcome_name", "population_definition", "source_citation", "source_url"):
            if not row[field].strip():
                raise ValidationError(f"Row {line}: {field} cannot be blank")
        if not row["source_url"].strip().startswith(("https://", "http://")):
            raise ValidationError(f"Row {line}: source_url must be an HTTP(S) URL")

    missing_counties = set(COUNTIES) - seen
    if missing_counties:
        raise ValidationError(f"Missing county FIPS: {sorted(missing_counties)}")
    if len(instruments) != 1 or len(estimate_types) != 1:
        raise ValidationError("All counties must use one common instrument and estimate type")
    return rows


def main() -> int:
    try:
        rows = validate()
    except ValidationError as exc:
        print(f"PMS OUTCOME VALIDATION FAILED: {exc}", file=sys.stderr)
        return 1

    receipt = {
        "status": "passed",
        "county_count": len(rows),
        "instrument": rows[0]["instrument"],
        "estimate_type": rows[0]["estimate_type"],
        "source_citation": rows[0]["source_citation"],
    }
    RECEIPT_PATH.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print("PMS outcome validation passed for all 58 California counties.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
