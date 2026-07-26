"""
Module 3: KPI Feature Engineering
-----------------------------------
Reads military_cleaned.csv (Module 2 output) and produces military_final.xlsx
for Tableau, with three engineered KPIs, alliance flags, and both wide and
long table layouts.

KPIs
----
1. Power Index Rank Gap
   power_index_rank : country's rank by Power Index (1 = strongest military;
                       Global Firepower's Power Index is "lower is stronger")
   gdp_rank          : country's rank by GDP (1 = largest economy)
   power_index_rank_gap = gdp_rank - power_index_rank
     -> positive  : military strength outranks the country's economic size
                    ("punching above its weight")
     -> negative  : economy outranks military strength
                    ("punching below its weight")

2. Assets per Capita
   total_military_assets = active_personnel + total_aircraft + tanks
                            + armored_vehicles + submarines + destroyers
                            + frigates + helicopters + rocket_projectors
   assets_per_capita = total_military_assets / population * 1000
     -> military assets per 1,000 people (keeps the number readable)

3. Budget-to-GDP Ratio
   budget_to_gdp_ratio_pct = defense_budget / gdp * 100

Metadata enrichment
--------------------
   is_nato : True if the country's Alliance field is "NATO"

Output
------
   military_final.xlsx
     - "Wide"     : one row per country, all metrics + KPIs + metadata
     - "Long"     : one row per (country, metric) pair -- tidy format for
                    Tableau parameters/dynamic metric selection
     - "KPI_Only" : just country + the 3 engineered KPIs + metadata, for
                    quick KPI-focused dashboards
"""

import numpy as np
import pandas as pd

CLEAN_FILE = "military_cleaned.csv"
FINAL_FILE = "military_final.xlsx"

ASSET_COLUMNS = [
    "active_personnel", "total_aircraft", "tanks", "armored_vehicles",
    "submarines", "destroyers", "frigates", "helicopters", "rocket_projectors",
]

ID_COLUMNS = ["country", "continent", "region", "alliance", "is_nato"]


def compute_power_index_rank_gap(df):
    # Power Index: lower value = stronger military -> rank ascending
    df["power_index_rank"] = df["power_index"].rank(method="min", ascending=True).astype(int)
    # GDP: higher value = larger economy -> rank descending
    df["gdp_rank"] = df["gdp"].rank(method="min", ascending=False).astype(int)
    df["power_index_rank_gap"] = df["gdp_rank"] - df["power_index_rank"]
    return df


def compute_assets_per_capita(df):
    df["total_military_assets"] = df[ASSET_COLUMNS].sum(axis=1)
    df["assets_per_capita"] = np.where(
        df["population"] > 0,
        df["total_military_assets"] / df["population"] * 1000,
        0.0,
    )
    return df


def compute_budget_to_gdp_ratio(df):
    df["budget_to_gdp_ratio_pct"] = np.where(
        df["gdp"] > 0,
        df["defense_budget"] / df["gdp"] * 100,
        0.0,
    )
    return df


def enrich_metadata(df):
    df["is_nato"] = df["alliance"].astype(str).str.upper().eq("NATO")
    return df


def build_long_format(wide_df):
    """Melt every metric column (everything except id/metadata columns)
    into a tidy country-metric-value table for Tableau."""
    metric_columns = [c for c in wide_df.columns if c not in ID_COLUMNS]
    long_df = wide_df.melt(
        id_vars=ID_COLUMNS,
        value_vars=metric_columns,
        var_name="metric",
        value_name="value",
    )
    return long_df


def main():
    print("=" * 60)
    print("MODULE 3: KPI Feature Engineering")
    print("=" * 60)

    df = pd.read_csv(CLEAN_FILE)
    print(f"Loaded {CLEAN_FILE}: {df.shape[0]} rows, {df.shape[1]} columns")

    # ---------------------------------------------------------
    # Compute KPIs
    # ---------------------------------------------------------
    df = compute_power_index_rank_gap(df)
    df = compute_assets_per_capita(df)
    df = compute_budget_to_gdp_ratio(df)
    print("Computed KPIs: power_index_rank_gap, assets_per_capita, budget_to_gdp_ratio_pct")

    # ---------------------------------------------------------
    # Enrich with metadata / alliance flags
    # ---------------------------------------------------------
    df = enrich_metadata(df)
    print(f"Enriched with alliance flag: is_nato ({df['is_nato'].sum()} NATO countries)")

    # Reorder: identifying/metadata columns first, then everything else
    front = ["country", "continent", "region", "alliance", "is_nato"]
    kpi_cols = ["power_index_rank", "gdp_rank", "power_index_rank_gap",
                "total_military_assets", "assets_per_capita", "budget_to_gdp_ratio_pct"]
    other_cols = [c for c in df.columns if c not in front + kpi_cols]
    wide_df = df[front + kpi_cols + other_cols]

    # ---------------------------------------------------------
    # Build long format
    # ---------------------------------------------------------
    long_df = build_long_format(wide_df)
    print(f"Built long format: {long_df.shape[0]} rows")

    # KPI-only sheet
    kpi_only_df = wide_df[front + kpi_cols].copy()

    # ---------------------------------------------------------
    # Sanity checks
    # ---------------------------------------------------------
    assert wide_df[kpi_cols].isnull().sum().sum() == 0, "KPI columns contain nulls"
    assert wide_df.shape[0] == 145, "Unexpected row count"
    print("All KPIs present and populated for every country")

    # ---------------------------------------------------------
    # Save to Excel (wide, long, KPI-only sheets -- flat tables,
    # header row 1, no merged cells: loads straight into Tableau)
    # ---------------------------------------------------------
    with pd.ExcelWriter(FINAL_FILE, engine="openpyxl") as writer:
        wide_df.to_excel(writer, sheet_name="Wide", index=False)
        long_df.to_excel(writer, sheet_name="Long", index=False)
        kpi_only_df.to_excel(writer, sheet_name="KPI_Only", index=False)

    print("=" * 60)
    print(f"Saved -> {FINAL_FILE}")
    print(f"  Wide     : {wide_df.shape[0]} rows x {wide_df.shape[1]} cols")
    print(f"  Long     : {long_df.shape[0]} rows x {long_df.shape[1]} cols")
    print(f"  KPI_Only : {kpi_only_df.shape[0]} rows x {kpi_only_df.shape[1]} cols")
    print("=" * 60)


if __name__ == "__main__":
    main()
