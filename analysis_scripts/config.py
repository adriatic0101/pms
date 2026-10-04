"""Shared constants for the California county PMS study."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "raw_data"
PROCESSED_DIR = ROOT / "processed_data"
FIGURES_DIR = ROOT / "figures_maps"

COUNTIES = {
    "06001": "Alameda", "06003": "Alpine", "06005": "Amador",
    "06007": "Butte", "06009": "Calaveras", "06011": "Colusa",
    "06013": "Contra Costa", "06015": "Del Norte", "06017": "El Dorado",
    "06019": "Fresno", "06021": "Glenn", "06023": "Humboldt",
    "06025": "Imperial", "06027": "Inyo", "06029": "Kern",
    "06031": "Kings", "06033": "Lake", "06035": "Lassen",
    "06037": "Los Angeles", "06039": "Madera", "06041": "Marin",
    "06043": "Mariposa", "06045": "Mendocino", "06047": "Merced",
    "06049": "Modoc", "06051": "Mono", "06053": "Monterey",
    "06055": "Napa", "06057": "Nevada", "06059": "Orange",
    "06061": "Placer", "06063": "Plumas", "06065": "Riverside",
    "06067": "Sacramento", "06069": "San Benito", "06071": "San Bernardino",
    "06073": "San Diego", "06075": "San Francisco", "06077": "San Joaquin",
    "06079": "San Luis Obispo", "06081": "San Mateo", "06083": "Santa Barbara",
    "06085": "Santa Clara", "06087": "Santa Cruz", "06089": "Shasta",
    "06091": "Sierra", "06093": "Siskiyou", "06095": "Solano",
    "06097": "Sonoma", "06099": "Stanislaus", "06101": "Sutter",
    "06103": "Tehama", "06105": "Trinity", "06107": "Tulare",
    "06109": "Tuolumne", "06111": "Ventura", "06113": "Yolo",
    "06115": "Yuba",
}

PMS_REQUIRED_FIELDS = {
    "county_fips", "county_name", "outcome_name", "instrument",
    "estimate_type", "estimate", "standard_error", "ci_lower", "ci_upper",
    "n_eligible", "survey_year_start", "survey_year_end",
    "population_definition", "source_citation", "source_url",
}

PMS_ALLOWED_INSTRUMENTS = {"PSST", "DRSP"}
PMS_ALLOWED_ESTIMATE_TYPES = {"mean_score", "prevalence_pct"}

PLACES_MEASURES = {
    "Food Insecurity": "food_insecurity_pct",
    "Short Sleep Duration": "short_sleep_pct",
    "Physical Inactivity": "physical_inactivity_pct",
    "Health Insurance": "uninsured_18_64_pct",
}

