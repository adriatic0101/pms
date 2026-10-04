#!/usr/bin/env python3
"""Download public county covariates. This script never creates PMS outcomes."""

import csv
import io
import json
import os
import sys
import urllib.parse
import urllib.request

from config import COUNTIES, RAW_DIR

PLACES_URL = (
    "https://data.cdc.gov/resource/swc5-untb.csv?"
    "%24where=stateabbr%3D%27CA%27&%24limit=5000"
)
ACS_BASE = "https://api.census.gov/data/2024/acs/acs5"
ACS_VARIABLES = [
    "NAME",
    "B19013_001E", "B19013_001M",
    "B17001_001E", "B17001_001M", "B17001_002E", "B17001_002M",
    "B15003_001E", "B15003_001M",
    "B15003_022E", "B15003_022M", "B15003_023E", "B15003_023M",
    "B15003_024E", "B15003_024M", "B15003_025E", "B15003_025M",
]


def get_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "ca-pms-sdh-study/1.0"})
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.read().decode("utf-8-sig")


def download_places() -> None:
    text = get_text(PLACES_URL)
    rows = list(csv.DictReader(io.StringIO(text)))
    fips = {row["locationid"] for row in rows}
    if fips != set(COUNTIES):
        raise RuntimeError(
            f"CDC PLACES county coverage mismatch: expected 58, received {len(fips)}"
        )
    target = RAW_DIR / "cdc_places_2025_ca.csv"
    target.write_text(text, encoding="utf-8")
    print(f"Saved {len(rows):,} CDC PLACES rows to {target.relative_to(RAW_DIR.parent)}")


def download_acs(api_key: str) -> None:
    query = urllib.parse.urlencode(
        {
            "get": ",".join(ACS_VARIABLES),
            "for": "county:*",
            "in": "state:06",
            "key": api_key,
        }
    )
    payload = json.loads(get_text(f"{ACS_BASE}?{query}"))
    header, records = payload[0], payload[1:]
    fips = {row[header.index("state")] + row[header.index("county")] for row in records}
    if fips != set(COUNTIES):
        raise RuntimeError(
            f"ACS county coverage mismatch: expected 58, received {len(fips)}"
        )
    target = RAW_DIR / "acs_2024_ca_counties.json"
    target.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Saved 58 ACS county rows to {target.relative_to(RAW_DIR.parent)}")


def main() -> int:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    download_places()
    api_key = os.getenv("CENSUS_API_KEY", "").strip()
    if not api_key:
        print(
            "ACS download skipped: set CENSUS_API_KEY and rerun. "
            "The CDC file was still downloaded.",
            file=sys.stderr,
        )
        return 2
    download_acs(api_key)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

