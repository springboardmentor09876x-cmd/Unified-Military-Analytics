"""
generate_kpis.py
-----------------
Unified Military Analytics and Comparison Dashboard
Milestone 2 - Module 3: KPI Feature Engineering

Reads the cleaned dataset, enriches it with Continent, Region, and NATO
Alliance information, merges the latest available GDP figures, computes
the required KPIs, and exports both a wide-format and a long-format
Tableau-ready workbook.

Guarantees:
    - Row count never changes from the original cleaned dataset (145 rows).
    - No duplicate countries are ever introduced during merges.

Run with:
    python3 generate_kpis.py
"""

import os
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------------
# CONFIGURATION - FILE PATHS
# ---------------------------------------------------------------------------

CLEANED_CSV_PATH = os.path.join("data", "military_cleaned.csv")
LOOKUP_XLSX_PATH = os.path.join("..", "lookups", "Military_Dataset_Lookups.xlsx")

FINAL_XLSX_PATH = os.path.join("data", "military_final.xlsx")
LONG_XLSX_PATH = os.path.join("data", "military_long.xlsx")

CONTINENT_REGION_SHEET = "Continent & Region"
GDP_SHEET_1 = "GDP - 1"
GDP_SHEET_2 = "GDP - 2"
NATO_SHEET = "NATO Alliance"


# ---------------------------------------------------------------------------
# MASTER COUNTRY NAME MAPPING
# ---------------------------------------------------------------------------
# Lookup workbooks (World Bank-style naming) often spell countries
# differently from GlobalFirepower's naming used in the cleaned dataset.
# Every KEY below is a variant that might appear in a lookup sheet;
# every VALUE is the canonical name used in military_cleaned.csv.
# This is the SINGLE source of truth for country name standardization --
# every lookup sheet is passed through this before any merge.

COUNTRY_NAME_MAPPING = {
    "Russian Federation": "Russia",
    "Korea, Rep.": "South Korea",
    "Republic of Korea": "South Korea",
    "Korea, Dem. People's Rep.": "North Korea",
    "Korea, Dem. Rep.": "North Korea",
    "Democratic People's Republic of Korea": "North Korea",
    "Taiwan, China": "Taiwan",
    "Chinese Taipei": "Taiwan",
    "Turkey": "Turkiye",
    "Cote d'Ivoire": "Ivory Coast",
    "Côte d'Ivoire": "Ivory Coast",
    "Cote d Ivoire": "Ivory Coast",
    "Congo, Dem. Rep.": "Democratic Republic of the Congo",
    "Democratic Republic of Congo": "Democratic Republic of the Congo",
    "DR Congo": "Democratic Republic of the Congo",
    "Congo, Rep.": "Republic of the Congo",
    "Congo (Brazzaville)": "Republic of the Congo",
    "Czech Republic": "Czechia",
    "Egypt, Arab Rep.": "Egypt",
    "Iran, Islamic Rep.": "Iran",
    "Syrian Arab Republic": "Syria",
    "Venezuela, RB": "Venezuela",
    "Bosnia & Herzegovina": "Bosnia and Herzegovina",
    "Macedonia, FYR": "North Macedonia",
    "North Macedonia, FYR": "North Macedonia",
    "Kyrgyz Republic": "Kyrgyzstan",
    "Lao PDR": "Laos",
    "Laos PDR": "Laos",
    "Slovak Republic": "Slovakia",
    "Yemen, Rep.": "Yemen",
    "Cabo Verde": "Cape Verde",
    "Micronesia, Fed. Sts.": "Micronesia",
    "Federated States of Micronesia": "Micronesia",
    "Brunei Darussalam": "Brunei",
    "Swaziland": "Eswatini",
    "Beliz": "Belize",
    "Bahamas, The": "Bahamas",
    "Gambia, The": "Gambia",
}


def standardize_country_series(series):
    """
    Applies COUNTRY_NAME_MAPPING to a pandas Series of country names,
    after stripping whitespace. Names not found in the mapping are
    left unchanged (they are already assumed to be in canonical form).
    """
    cleaned = series.astype(str).str.strip()
    return cleaned.replace(COUNTRY_NAME_MAPPING)


# ---------------------------------------------------------------------------
# MANUAL OVERRIDES
# ---------------------------------------------------------------------------
# Used ONLY when a country is genuinely absent from the lookup workbook
# (not a naming mismatch). Filled in manually with correct real-world values.

MANUAL_CONTINENT_REGION_OVERRIDES = {
    "North Korea": {
        "Continent": "Asia",
        "Region": "Eastern Asia"
    },

    "Democratic Republic of the Congo": {
        "Continent": "Africa",
        "Region": "Middle Africa"
    },

    "Ivory Coast": {
        "Continent": "Africa",
        "Region": "Western Africa"
    },

    "North Macedonia": {
        "Continent": "Europe",
        "Region": "Southern Europe"
    },

    "Republic of the Congo": {
        "Continent": "Africa",
        "Region": "Middle Africa"
    },

    "Bosnia and Herzegovina": {
        "Continent": "Europe",
        "Region": "Southern Europe"
    },

    "Kosovo": {
        "Continent": "Europe",
        "Region": "Southern Europe"
    }
}


# ---------------------------------------------------------------------------
# STEP 1: LOAD CLEANED MILITARY DATASET
# ---------------------------------------------------------------------------

def load_cleaned_dataset(path):
    """Loads the cleaned military dataset produced by Module 2."""
    df = pd.read_csv(path)
    df["country"] = standardize_country_series(df["country"])
    print(f"Loaded cleaned dataset: {df.shape[0]} rows x {df.shape[1]} columns")
    return df


# ---------------------------------------------------------------------------
# STEP 2: LOAD CONTINENT & REGION LOOKUP
# ---------------------------------------------------------------------------

def load_continent_region(xlsx_path):
    """
    Loads the Continent & Region sheet, standardizes country names using
    COUNTRY_NAME_MAPPING, and removes duplicate country rows so the merge
    can never inflate the row count.
    """
    df = pd.read_excel(xlsx_path, sheet_name=CONTINENT_REGION_SHEET)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.rename(columns={"Country": "country"})

    df["country"] = standardize_country_series(df["country"])

    # Remove exact duplicate country entries -- keep the first occurrence.
    before = len(df)
    df = df.drop_duplicates(subset="country", keep="first").reset_index(drop=True)
    removed = before - len(df)
    if removed > 0:
        print(f"Continent & Region lookup: removed {removed} duplicate country row(s).")

    df = df[["country", "Continent", "Region"]]
    return df


# ---------------------------------------------------------------------------
# STEP 3: LOAD AND MERGE GDP DATA (LATEST YEAR PER COUNTRY)
# ---------------------------------------------------------------------------

def load_latest_gdp(xlsx_path):
    """
    Loads GDP data from 'GDP - 1' and 'GDP - 2', standardizes country names,
    keeps only the latest available year per country, and guarantees exactly
    one row per country so the merge can never inflate the row count.
    """
    gdp_1 = pd.read_excel(xlsx_path, sheet_name=GDP_SHEET_1)
    gdp_2 = pd.read_excel(xlsx_path, sheet_name=GDP_SHEET_2)

    gdp_1.columns = [str(c).strip() for c in gdp_1.columns]
    gdp_2.columns = [str(c).strip() for c in gdp_2.columns]

    gdp_combined = pd.concat([gdp_1, gdp_2], ignore_index=True)
    gdp_combined = gdp_combined.rename(columns={"Country": "country"})

    gdp_combined["country"] = standardize_country_series(gdp_combined["country"])
    gdp_combined["Year"] = pd.to_numeric(gdp_combined["Year"], errors="coerce")
    gdp_combined["GDP"] = pd.to_numeric(gdp_combined["GDP"], errors="coerce")

    # Drop rows with no GDP value before selecting the latest year, so a
    # missing/blank latest-year entry never overrides a real earlier value.
    gdp_combined = gdp_combined.dropna(subset=["GDP"])

    # Sort so the latest year comes first, then keep exactly one row per country.
    gdp_combined = gdp_combined.sort_values("Year", ascending=False)
    latest_gdp = gdp_combined.drop_duplicates(subset="country", keep="first")

    latest_gdp = latest_gdp[["country", "GDP"]].reset_index(drop=True)

    # Final safety check: guarantee uniqueness before this ever reaches a merge.
    duplicate_count = latest_gdp["country"].duplicated().sum()
    if duplicate_count > 0:
        raise ValueError(
            f"GDP lookup still has {duplicate_count} duplicate country row(s) "
            f"after standardization -- fix COUNTRY_NAME_MAPPING before merging."
        )
    print("\nChecking Syria entries in GDP lookup:")
    print(latest_gdp[latest_gdp["country"].str.contains("Syria", case=False, na=False)])

    print("\nChecking Syrian entries:")
    print(latest_gdp[latest_gdp["country"].str.contains("Syrian", case=False, na=False)])

    return latest_gdp


# ---------------------------------------------------------------------------
# STEP 4: LOAD NATO ALLIANCE LOOKUP
# ---------------------------------------------------------------------------

def load_nato_countries(xlsx_path):
    """Loads the list of NATO member countries, standardized to canonical names."""
    df = pd.read_excel(xlsx_path, sheet_name=NATO_SHEET)
    df.columns = [str(c).strip() for c in df.columns]
    nato_series = standardize_country_series(df["NATO Allied Countries"])
    return set(nato_series.tolist())


# ---------------------------------------------------------------------------
# STEP 5: MERGE ALL ENRICHMENT DATA
# ---------------------------------------------------------------------------

def enrich_dataset(df, continent_region_df, gdp_df, nato_countries):
    """
    Merges Continent, Region, GDP, and Alliance information onto the dataset,
    guaranteeing the row count never changes from the original dataset.
    """
    df = df.copy()

    original_rows = len(df)
    print(f"Original rows: {original_rows}")

    # --- Continent & Region merge ---------------------------------------
    df = df.merge(
        continent_region_df,
        on="country",
        how="left",
        validate="many_to_one",  # raises an error instead of silently duplicating rows
    )
    print(f"Rows after Continent merge: {len(df)}")

    # --- GDP merge ----------------------------------------------------------
    df = df.merge(
        gdp_df,
        on="country",
        how="left",
        validate="many_to_one",
    )
    print(f"Rows after GDP merge: {len(df)}")
    # Fill missing GDP values with 0
    df["GDP"] = df["GDP"].fillna(0)

    # --- NATO Alliance (lookup, not a merge -- row count cannot change) -----
    df["Alliance"] = df["country"].apply(
        lambda c: "NATO" if c in nato_countries else "Non-NATO"
    )
    print(f"Rows after NATO merge: {len(df)}")

    # --- Manual overrides for countries genuinely absent from the workbook ---
    for country_name, values in MANUAL_CONTINENT_REGION_OVERRIDES.items():
        mask = df["country"] == country_name
        if mask.any():
            for column_name, value in values.items():
                still_missing = mask & df[column_name].isna()
                df.loc[still_missing, column_name] = value

    # --- Missing value reporting ---------------------------------------------
    missing_continent = df.loc[df["Continent"].isna(), "country"].tolist()
    missing_region = df.loc[df["Region"].isna(), "country"].tolist()
    missing_gdp = df.loc[df["GDP"].isna(), "country"].tolist()

    print(f"Countries missing Continent: {missing_continent}")
    print(f"Countries missing Region: {missing_region}")
    print(f"Countries missing GDP: {missing_gdp}")

    final_rows = len(df)
    print(f"Final rows: {final_rows}")

    # --- Hard guarantee: row count must never change --------------------------
    if final_rows != original_rows:
        raise ValueError(
            f"Row count changed during enrichment! "
            f"Original: {original_rows}, Final: {final_rows}. "
            f"Check COUNTRY_NAME_MAPPING and lookup sheets for duplicate entries."
        )

    # --- Duplicate country guarantee -------------------------------------------
    duplicate_countries = df["country"].duplicated().sum()
    if duplicate_countries > 0:
        raise ValueError(
            f"Enrichment introduced {duplicate_countries} duplicate country row(s)."
        )

    return df


# ---------------------------------------------------------------------------
# STEP 6: COMPUTE KPIs
# ---------------------------------------------------------------------------

def compute_kpis(df):
    """Computes Power Index Rank Gap, Assets per Capita, and Budget-to-GDP Ratio."""

    df["power_index_rank_gap"] = df["power_index_rank"] - 1

    total_assets = (
        df["total_military_aircraft"]
        + df["tanks"]
        + df["armored_fighting_vehicles"]
        + df["self_propelled_artillery"]
        + df["towed_artillery"]
        + df["rocket_projectors"]
        + df["total_naval_fleet"]
    )
    df["assets_per_capita"] = total_assets / df["total_population"]

    df["budget_to_gdp_ratio"] = np.where(
    df["GDP"] > 0,
    (df["defense_budget_usd"] / df["GDP"]) * 100,
    0
)

    # Replace infinite values (e.g. division by zero population/GDP) and
    # fill any remaining missing KPI values with 0.
    df = df.replace([np.inf, -np.inf], 0)
    kpi_columns = ["power_index_rank_gap", "assets_per_capita", "budget_to_gdp_ratio"]
    df[kpi_columns] = df[kpi_columns].fillna(0)

    return df


# ---------------------------------------------------------------------------
# STEP 7: SAVE WIDE-FORMAT DATASET
# ---------------------------------------------------------------------------

def save_wide_format(df, output_path):
    """Saves the final enriched wide-format dataset as an Excel file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_excel(output_path, index=False, sheet_name="Military Final")
    print(f"Saved wide-format dataset -> {output_path}")
    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")


# ---------------------------------------------------------------------------
# STEP 8: BUILD AND SAVE LONG-FORMAT DATASET (TABLEAU-READY)
# ---------------------------------------------------------------------------

def save_long_format(df, output_path):
    """
    Converts the wide-format dataset into long format using pandas melt(),
    keeping identifying/enrichment columns fixed and unpivoting all metric
    and KPI columns into 'Metric' / 'Value' pairs.
    """
    id_columns = ["country", "Continent", "Region", "Alliance"]
    value_columns = [c for c in df.columns if c not in id_columns]

    long_df = df.melt(
        id_vars=id_columns,
        value_vars=value_columns,
        var_name="Metric",
        value_name="Value",
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    long_df.to_excel(output_path, index=False, sheet_name="Military Long")
    print(f"Saved long-format dataset -> {output_path}")
    print(f"Shape: {long_df.shape[0]} rows x {long_df.shape[1]} columns")


# ---------------------------------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------------------------------

def main():
    df = load_cleaned_dataset(CLEANED_CSV_PATH)

    continent_region_df = load_continent_region(LOOKUP_XLSX_PATH)
    gdp_df = load_latest_gdp(LOOKUP_XLSX_PATH)
    nato_countries = load_nato_countries(LOOKUP_XLSX_PATH)

    df = enrich_dataset(df, continent_region_df, gdp_df, nato_countries)
    df = compute_kpis(df)

    save_wide_format(df, FINAL_XLSX_PATH)
    save_long_format(df, LONG_XLSX_PATH)

    print("KPI feature engineering completed successfully.")


if __name__ == "__main__":
    main()