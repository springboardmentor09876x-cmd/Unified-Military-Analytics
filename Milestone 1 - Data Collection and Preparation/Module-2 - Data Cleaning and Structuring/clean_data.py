"""
clean_data.py
--------------
Module 2 deliverable: Data Cleaning and Structuring.

Takes military_raw_data.csv (messy scraped output — currency symbols,
commas, embedded tabs/newlines, unit suffixes like "km" or "bbl") and
produces a fully numeric, structured military_cleaned.csv.

Usage:
    python clean_data.py
"""

import re
import pandas as pd

SOURCE_FILE = "military_raw_data.csv"
OUTPUT_FILE = "military_cleaned.csv"

# Columns that are text/categorical, not numeric — left as-is (just stripped).
TEXT_COLUMNS = ["Country", "Continent", "Region", "Alliance"]

# Rename raw column headers to the consistent snake_case scheme used
# throughout the rest of the project.
RENAME_MAP = {
    "Country": "country",
    "Power Index": "power_index_score",
    "Continent": "continent",
    "Region": "region",
    "GDP": "gdp_usd",
    "Alliance": "alliance",
}


def clean_numeric(value):
    """Strips $, commas, unit suffixes (km, bbl, cum, mt, etc.), and stray
    whitespace/tabs/newlines, returning a clean float. Returns None if no
    number can be found."""
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).replace(",", "")
    match = re.search(r"-?\d+\.?\d*", text)
    if match:
        return float(match.group())
    return None


def main():
    df = pd.read_csv(SOURCE_FILE)

    for col in TEXT_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    numeric_cols = [c for c in df.columns if c not in TEXT_COLUMNS]
    for col in numeric_cols:
        df[col] = df[col].apply(clean_numeric)

    df = df.rename(columns=RENAME_MAP)

    total_cells = df.shape[0] * df.shape[1]
    missing_cells = df.isna().sum().sum()
    missing_pct = (missing_cells / total_cells) * 100
    print(f"Shape: {df.shape}")
    print(f"Missing values after cleaning: {missing_cells} of {total_cells} cells ({missing_pct:.2f}%)")

    missing_by_col = df.isna().sum()
    worst_cols = missing_by_col[missing_by_col > 0].sort_values(ascending=False)
    if len(worst_cols):
        print("Columns with missing values:")
        print(worst_cols.to_string())

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
