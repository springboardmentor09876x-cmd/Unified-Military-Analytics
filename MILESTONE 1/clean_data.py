"""
clean_data.py
Module 2: Data Cleaning and Structuring

Cleans military_data_merged.csv (output of Module 1) and produces a
Tableau-ready dataset: military_cleaned.csv

Steps performed:
    1. Clean text: strip commas, %, +, $, and unit suffixes (km, bbl, Cu.M, mt, etc.)
    2. Convert cleaned metric columns to numeric dtypes
    3. Standardize column names to a consistent snake_case convention
       (e.g. total_military_aircraft -> total_aircraft)
    4. Handle missing / null values
    5. Save the cleaned dataset
"""

import re
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------------------
INPUT_FILE  = "military_data_merged.csv"
OUTPUT_FILE = "military_cleaned.csv"

df = pd.read_csv(INPUT_FILE)

print("Loaded:", df.shape)

# ---------------------------------------------------------------------------
# 2. Text cleaning + numeric conversion
# ---------------------------------------------------------------------------
# Every "dirty" numeric column in this dataset is a string containing some
# combination of: thousands commas, a leading "$", a trailing unit
# ("km", "bbl", "Cu.M", "mt"), a trailing "%", or a leading "+".
# clean_numeric() strips all of that and returns a float.

def clean_numeric(series: pd.Series) -> pd.Series:
    """Strip commas, $, %, +, and trailing unit text, then convert to float."""
    cleaned = (
        series.astype(str)
        .str.replace(",", "", regex=False)      # remove thousands separators
        .str.replace("$", "", regex=False)       # remove currency symbol
        .str.replace("%", "", regex=False)       # remove percent sign
        .str.replace("+", "", regex=False)       # remove leading/trailing plus
        .str.strip()
        # remove a trailing unit word/abbreviation, e.g. "150,000 km" -> "150000"
        .str.replace(r"\s*(km|bbl|cu\.?m|mt|kg|km2|sq\s?km)\s*$", "", regex=True, flags=0)
        .str.strip()
    )
    # anything that is not a clean number (e.g. "nan", "", "N/A", "-") -> NaN
    cleaned = cleaned.replace({"nan": np.nan, "": np.nan, "N/A": np.nan, "-": np.nan})
    return pd.to_numeric(cleaned, errors="coerce")


# Columns that are numeric but stored as text with symbols/units.
# (Columns already numeric, like attack_aircraft, are skipped automatically.)
text_numeric_cols = [
    "total_military_manpower", "fit_for_service", "population_reaching_military_age_annually",
    "active_personnel", "reserve_personnel", "paramilitary",
    "total_military_aircraft", "fighter_aircraft", "trainer_aircraft",
    "total_military_helicopters", "attack_helicopters",
    "tanks", "armored_fighting_vehicles", "self_propelled_artillery",
    "towed_artillery", "rocket_projectors",
    "total_naval_fleet_tonnage_mt",
    "defense_budget_usd", "external_debt_usd", "purchasing_power_parity_usd",
    "foreign_exchange_and_gold_reserves_usd",
    "total_serviceable_airports", "labour_force", "total_merchant_marine_fleet",
    "railway_coverage_km", "roadway_coverage_km",
    "oil_production_bbl", "oil_consumption_bbl", "proven_oil_reserves_bbl",
    "natural_gas_production_cum", "natural_gas_consumption_cum", "proven_natural_gas_reserves_cum",
    "coal_production_cum", "coal_consumption_mt", "proven_coal_reserves_cum",
    "total_land_area_sq_km", "coastline_coverage_km", "border_coverage_km", "waterway_coverage_km",
]

for col in text_numeric_cols:
    if col in df.columns:
        df[col] = clean_numeric(df[col])

print("Converted", len(text_numeric_cols), "columns to numeric.")

# ---------------------------------------------------------------------------
# 3. Standardize column names
# ---------------------------------------------------------------------------
# Convert everything to a consistent lower_snake_case naming convention and
# shorten a few overly-verbose names (e.g. total_military_aircraft -> total_aircraft)

rename_map = {
    "Country": "country",
    "Continent": "continent",
    "Region": "region",
    "GDP_Year": "gdp_year",
    "GDP": "gdp",
    "NATO_Ally": "nato_ally",
    "total_military_manpower": "total_manpower",
    "total_military_aircraft": "total_aircraft",
    "total_military_helicopters": "total_helicopters",
    "total_naval_fleet_tonnage_mt": "total_naval_fleet_tonnage",
    "defense_budget_usd": "defense_budget",
    "external_debt_usd": "external_debt",
    "purchasing_power_parity_usd": "purchasing_power_parity",
    "foreign_exchange_and_gold_reserves_usd": "forex_gold_reserves",
    "oil_production_bbl": "oil_production",
    "oil_consumption_bbl": "oil_consumption",
    "proven_oil_reserves_bbl": "proven_oil_reserves",
    "natural_gas_production_cum": "natural_gas_production",
    "natural_gas_consumption_cum": "natural_gas_consumption",
    "proven_natural_gas_reserves_cum": "proven_natural_gas_reserves",
    "coal_production_cum": "coal_production",
    "coal_consumption_mt": "coal_consumption",
    "proven_coal_reserves_cum": "proven_coal_reserves",
    "total_land_area_sq_km": "total_land_area",
    "coastline_coverage_km": "coastline_coverage",
    "border_coverage_km": "border_coverage",
    "waterway_coverage_km": "waterway_coverage",
    "railway_coverage_km": "railway_coverage",
    "roadway_coverage_km": "roadway_coverage",
}

df = df.rename(columns=rename_map)

# Fallback: standardize any remaining column name to lower_snake_case
df.columns = [re.sub(r"__+", "_", c.strip().lower().replace(" ", "_")) for c in df.columns]

print("Standardized column names.")

# ---------------------------------------------------------------------------
# 4. Handle missing / null values
# ---------------------------------------------------------------------------
# Strategy:
#   - Numeric "count/quantity" columns: missing usually means the country
#     reports none / data not available -> fill with 0
#   - Categorical columns (continent, region): fill with "Unknown"
#   - gdp / gdp_year: keep as NaN (imputing a false GDP would mislead
#     analysis) but flag with a boolean 'gdp_missing' column for transparency
#   - nato_ally: already boolean, no nulls expected

numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
# Keep GDP fields out of the blanket fill so we don't fabricate financial data
protected_cols = ["gdp", "gdp_year"]
fill_zero_cols = [c for c in numeric_cols if c not in protected_cols]

df[fill_zero_cols] = df[fill_zero_cols].fillna(0)

df["gdp_missing"] = df["gdp"].isna()

categorical_cols = ["continent", "region"]
for col in categorical_cols:
    if col in df.columns:
        df[col] = df[col].fillna("Unknown")

# Final null check
remaining_nulls = df.isna().sum()
remaining_nulls = remaining_nulls[remaining_nulls > 0]
print("\nRemaining nulls after cleaning:")
print(remaining_nulls if len(remaining_nulls) else "None")

# ---------------------------------------------------------------------------
# 5. Final checks & save
# ---------------------------------------------------------------------------
# Drop exact duplicate rows, if any
before = len(df)
df = df.drop_duplicates()
print(f"\nDropped {before - len(df)} duplicate rows.")

df.to_csv(OUTPUT_FILE, index=False)
print(f"\nCleaned dataset saved to: {OUTPUT_FILE}")
print(f"Final shape: {df.shape[0]} rows x {df.shape[1]} columns")
print("\nColumn dtypes:")
print(df.dtypes)
