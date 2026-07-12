"""
Module 2: Data Cleaning and Structuring
-----------------------------------------
Reads military_raw_data.csv (produced by scrape_military_metrics.py) and
produces a clean, analysis-ready dataset for Tableau: military_cleaned.csv

Steps:
  1. Load the raw CSV
  2. Strip currency symbols ($), commas, percent signs (%), plus signs (+),
     and trailing unit labels (km, bbl, Cu.M, mt, etc.) that got wrapped onto
     new lines during scraping, then convert everything to real numbers
  3. Drop duplicate columns (the raw file has an early, already-clean subset
     of columns — e.g. Active_Personnel — that duplicate a later, messier
     scraped column — e.g. active_personnel — for every row)
  4. Standardize all column names to lower_snake_case
  5. Handle missing/null values
  6. Save the cleaned dataset
"""

import re
import numpy as np
import pandas as pd

RAW_FILE = "military_raw_data.csv"
CLEAN_FILE = "military_cleaned.csv"

# Columns that should stay as text, not be numeric-cleaned
TEXT_COLUMNS = ["Country", "Continent", "Region", "Alliance"]


def clean_numeric_value(raw_value):
    """Turn a messy scraped value into a plain float (or NaN).

    Handles cases like:
      "40,121,552"                -> 40121552.0
      "$    145,000,000"          -> 145000000.0
      "34,903\\n    km"            -> 34903.0
      "80,200,000\\n    Cu.M"      -> 80200000.0
      ""  / NaN                   -> NaN
    """
    if pd.isna(raw_value):
        return np.nan

    text = str(raw_value)

    # Unit labels (km, bbl, Cu.M, mt, ...) were appended after a line break
    # during scraping -- keep only the part before the first line break.
    text = text.split("\n")[0]

    # Remove currency symbols, thousands separators, percent and plus signs
    text = re.sub(r"[\$,%+]", "", text)
    text = text.strip()

    if text == "" or text.lower() == "nan":
        return np.nan

    try:
        return float(text)
    except ValueError:
        return np.nan


def to_snake_case(column_name):
    """Standardize a column name to lower_snake_case."""
    name = column_name.strip()
    name = re.sub(r"[^0-9a-zA-Z]+", "_", name)   # spaces/punctuation -> _
    name = re.sub(r"_+", "_", name).strip("_")
    return name.lower()


def drop_duplicate_columns(dataframe):
    """Drop columns that are exact duplicates (value-for-value) of a column
    that appears earlier in the dataframe."""
    seen = {}
    columns_to_drop = []
    for column in dataframe.columns:
        fingerprint = tuple(dataframe[column].fillna("NA").astype(str))
        if fingerprint in seen:
            columns_to_drop.append(column)
        else:
            seen[fingerprint] = column
    return dataframe.drop(columns=columns_to_drop), columns_to_drop


def main():
    print("=" * 60)
    print("MODULE 2: Data Cleaning and Structuring")
    print("=" * 60)

    df = pd.read_csv(RAW_FILE)
    print(f"Loaded {RAW_FILE}: {df.shape[0]} rows, {df.shape[1]} columns")

    # ---------------------------------------------------------
    # STEP 1: Clean text -> numeric for every numeric-style column
    # ---------------------------------------------------------
    numeric_columns = [c for c in df.columns if c not in TEXT_COLUMNS]
    for column in numeric_columns:
        df[column] = df[column].apply(clean_numeric_value)
    print(f"Cleaned {len(numeric_columns)} numeric columns "
          f"(removed $, commas, %, +, unit suffixes)")

    # ---------------------------------------------------------
    # STEP 2: Drop exact-duplicate columns
    # ---------------------------------------------------------
    df, dropped_columns = drop_duplicate_columns(df)
    print(f"Dropped {len(dropped_columns)} duplicate columns:")
    for column in dropped_columns:
        print(f"  - {column}")

    # ---------------------------------------------------------
    # STEP 3: Standardize column names
    # ---------------------------------------------------------
    df.columns = [to_snake_case(c) for c in df.columns]
    print("Standardized all column names to lower_snake_case")

    # ---------------------------------------------------------
    # STEP 4: Handle missing / null values
    # ---------------------------------------------------------
    # Alliance: blank means the country is not part of a listed alliance
    if "alliance" in df.columns:
        df["alliance"] = df["alliance"].fillna("Non-aligned")

    # Continent / Region: fill any stray blanks with "Unknown"
    for column in ["continent", "region"]:
        if column in df.columns:
            df[column] = df[column].fillna("Unknown")

    # Remaining numeric columns: missing usually means "not reported" (0),
    # which matches how Global Firepower treats absent capabilities
    # (e.g. a landlocked country with no naval tonnage).
    numeric_cols_final = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols_final] = df[numeric_cols_final].fillna(0)

    missing_pct = df.isnull().mean().mean() * 100
    print(f"Missing values after cleaning: {missing_pct:.2f}%")

    # ---------------------------------------------------------
    # STEP 5: Save clean dataset
    # ---------------------------------------------------------
    df.to_csv(CLEAN_FILE, index=False)
    print("=" * 60)
    print(f"Saved cleaned dataset -> {CLEAN_FILE}")
    print(f"Final shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print("=" * 60)


if __name__ == "__main__":
    main()
