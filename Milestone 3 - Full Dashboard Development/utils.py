"""
utils.py
--------
Unified Military Analytics and Comparison Dashboard
Module 5 - Dashboard Development (Quick Stats)

Responsibilities of this file ONLY:
    - Load the two Excel datasets (cached)
    - Clean / safely coerce numeric columns
    - Apply sidebar filters
    - Compute KPI values
    - Provide number-formatting helpers used across the app

No Streamlit UI code and no Plotly chart-building code lives here.
"""

import os
import pandas as pd
import numpy as np
import streamlit as st

# ---------------------------------------------------------------------------
# FILE PATHS
# ---------------------------------------------------------------------------
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
FINAL_XLSX_PATH = os.path.join(DATA_DIR, "military_final.xlsx")
LONG_XLSX_PATH = os.path.join(DATA_DIR, "military_long.xlsx")

# ---------------------------------------------------------------------------
# COLUMN NAMES (exact, as confirmed from the real dataset -- do not rename)
# ---------------------------------------------------------------------------
COL_COUNTRY = "country"
COL_RANK = "power_index_rank"
COL_SCORE = "power_index_score"
COL_CONTINENT = "Continent"
COL_REGION = "Region"
COL_ALLIANCE = "Alliance"
COL_GDP = "GDP"
COL_BUDGET = "defense_budget_usd"
COL_AIRCRAFT = "total_military_aircraft"
COL_TANKS = "tanks"
COL_NAVAL = "total_naval_fleet"
COL_MANPOWER = "total_military_manpower"
COL_ACTIVE = "active_personnel"
COL_RESERVE = "reserve_personnel"
COL_POP = "total_population"
COL_PPP = "purchasing_power_parity_usd"
COL_ASSETS_PER_CAPITA = "assets_per_capita"
COL_BUDGET_TO_GDP = "budget_to_gdp_ratio"

# Columns that must be numeric for the dashboard to work correctly.
NUMERIC_COLUMNS = [
    COL_RANK, COL_SCORE, "total_population", "total_military_manpower",
    "fit_for_service", "population_reaching_military_age_annually",
    "active_personnel", "reserve_personnel", "paramilitary",
    "total_military_aircraft", "fighter_aircraft", "attack_aircraft",
    "transport_aircraft", "trainer_aircraft", "special_mission_aircraft",
    "tanker_aircraft", "total_military_helicopters", "attack_helicopters",
    "tanks", "armored_fighting_vehicles", "self_propelled_artillery",
    "towed_artillery", "rocket_projectors", "total_naval_fleet",
    "total_naval_fleet_tonnage_mt", "aircraft_carriers", "helicopter_carriers",
    "submarines", "destroyers", "frigates", "corvettes",
    "coastal_patrol_craft", "mine_warfare_craft", "defense_budget_usd",
    "external_debt_usd", "purchasing_power_parity_usd",
    "foreign_exchange_and_gold_reserves_usd", "total_serviceable_airports",
    "labour_force", "major_ports_and_terminals", "total_merchant_marine_fleet",
    "railway_coverage_km", "roadway_coverage_km", "waterway_coverage_km",
    "oil_production_bbl", "oil_consumption_bbl", "proven_oil_reserves_bbl",
    "natural_gas_production_cum", "natural_gas_consumption_cum",
    "proven_natural_gas_reserves_cum", "coal_production_cum",
    "coal_consumption_mt", "proven_coal_reserves_cum", "total_land_area_sq_km",
    "coastline_coverage_km", "border_coverage_km", "GDP",
    "power_index_rank_gap", "assets_per_capita", "budget_to_gdp_ratio",
]


def _clean_numeric_series(series: pd.Series) -> pd.Series:
    """
    Safely converts a column to numeric, regardless of what junk is inside it.
    Handles: commas, currency symbols, stray text, NaN, None, empty strings.
    Never raises -- unparseable values simply become NaN.
    """
    if series.dtype.kind in "if":  # already int or float
        return series
    cleaned = (
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.strip()
    )
    cleaned = cleaned.replace({"": np.nan, "None": np.nan, "nan": np.nan, "N/A": np.nan})
    return pd.to_numeric(cleaned, errors="coerce")


@st.cache_data(show_spinner="Loading military datasets...")
def load_data():
    """
    Loads both Excel datasets ONCE (Streamlit caches the result across reruns).
    Returns a tuple: (final_df, long_df)

    Uses pandas + openpyxl only -- no pyarrow involved, so this is safe on
    machines where pyarrow has caused segmentation faults.
    """
    final_df = pd.read_excel(FINAL_XLSX_PATH, sheet_name="Military Final", engine="openpyxl")
    long_df = pd.read_excel(LONG_XLSX_PATH, sheet_name="Military Long", engine="openpyxl")

    final_df = final_df.copy()
    long_df = long_df.copy()

    # Safely coerce every numeric column -- protects against stray text,
    # commas, or currency symbols without ever crashing the app.
    for col in NUMERIC_COLUMNS:
        if col in final_df.columns:
            final_df[col] = _clean_numeric_series(final_df[col])

    if "Value" in long_df.columns:
        long_df["Value"] = _clean_numeric_series(long_df["Value"])

    # Clean text columns
    for col in [COL_COUNTRY, COL_CONTINENT, COL_REGION, COL_ALLIANCE]:
        if col in final_df.columns:
            final_df[col] = final_df[col].astype(str).str.strip()

    return final_df, long_df


def get_filter_options(df: pd.DataFrame) -> dict:
    """Returns sorted unique values for each filter, safe against missing columns."""
    def _opts(col):
        if col in df.columns:
            return sorted(df[col].dropna().unique().tolist())
        return []

    return {
        "country": _opts(COL_COUNTRY),
        "region": _opts(COL_REGION),
        "continent": _opts(COL_CONTINENT),
        "alliance": _opts(COL_ALLIANCE),
    }


def apply_filters(df: pd.DataFrame, countries=None, regions=None, continents=None, alliances=None) -> pd.DataFrame:
    """
    Applies the sidebar filters. Any empty/None selection means "no filter
    on that dimension" (i.e. include everything for that column).
    Always returns a DataFrame (possibly empty) -- never raises.
    """
    filtered = df.copy()

    if countries:
        filtered = filtered[filtered[COL_COUNTRY].isin(countries)]
    if regions:
        filtered = filtered[filtered[COL_REGION].isin(regions)]
    if continents:
        filtered = filtered[filtered[COL_CONTINENT].isin(continents)]
    if alliances:
        filtered = filtered[filtered[COL_ALLIANCE].isin(alliances)]

    return filtered


# ---------------------------------------------------------------------------
# NUMBER FORMATTING HELPERS
# ---------------------------------------------------------------------------

def format_number(value, prefix="", decimals=2):
    """
    Formats large numbers into readable short form: 1.2T / 845B / 2.18K.
    Never uses scientific notation. Handles NaN/None gracefully.
    """
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return "N/A"
    try:
        value = float(value)
    except (TypeError, ValueError):
        return "N/A"

    abs_value = abs(value)
    if abs_value >= 1_000_000_000_000:
        formatted = f"{value / 1_000_000_000_000:.{decimals}f}T"
    elif abs_value >= 1_000_000_000:
        formatted = f"{value / 1_000_000_000:.{decimals}f}B"
    elif abs_value >= 1_000_000:
        formatted = f"{value / 1_000_000:.{decimals}f}M"
    elif abs_value >= 1_000:
        formatted = f"{value / 1_000:.{decimals}f}K"
    else:
        formatted = f"{value:.0f}" if abs_value == int(abs_value) else f"{value:.{decimals}f}"

    return f"{prefix}{formatted}"


def format_currency(value, decimals=2):
    """Shortcut for format_number with a '$' prefix."""
    return format_number(value, prefix="$", decimals=decimals)


def format_plain(value):
    """Formats a plain integer count with thousands separators (e.g. 12,345)."""
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return "N/A"
    try:
        return f"{int(round(float(value))):,}"
    except (TypeError, ValueError):
        return "N/A"


def format_score(value, decimals=4):
    """Formats the Power Index score (small decimal values, lower = stronger)."""
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return "N/A"
    try:
        return f"{float(value):.{decimals}f}"
    except (TypeError, ValueError):
        return "N/A"


# ---------------------------------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------------------------------

def compute_kpis(df: pd.DataFrame) -> dict:
    """
    Computes every KPI card value from the (already filtered) dataframe.
    Returns safe defaults ("N/A" / 0) if the filtered dataframe is empty,
    so the dashboard never crashes on a zero-result filter combination.
    """
    if df.empty:
        return {
            "total_countries": 0,
            "avg_power_index": "N/A",
            "total_budget": "N/A",
            "total_aircraft": "N/A",
            "total_tanks": "N/A",
            "total_naval": "N/A",
            "total_manpower": "N/A",
            "best_country": "N/A",
        }

    best_country = "N/A"
    if COL_RANK in df.columns and df[COL_RANK].notna().any():
        best_row = df.loc[df[COL_RANK].idxmin()]
        best_country = best_row[COL_COUNTRY]

    return {
        "total_countries": int(df[COL_COUNTRY].nunique()),
        "avg_power_index": format_score(df[COL_SCORE].mean()) if COL_SCORE in df.columns else "N/A",
        "total_budget": format_currency(df[COL_BUDGET].sum()) if COL_BUDGET in df.columns else "N/A",
        "total_aircraft": format_plain(df[COL_AIRCRAFT].sum()) if COL_AIRCRAFT in df.columns else "N/A",
        "total_tanks": format_plain(df[COL_TANKS].sum()) if COL_TANKS in df.columns else "N/A",
        "total_naval": format_plain(df[COL_NAVAL].sum()) if COL_NAVAL in df.columns else "N/A",
        "total_manpower": format_number(df[COL_MANPOWER].sum()) if COL_MANPOWER in df.columns else "N/A",
        "best_country": best_country,
    }


def get_country_profile(df: pd.DataFrame, country_name: str) -> dict:
    """Returns a dict of every key stat for one selected country (for the search card)."""
    row = df[df[COL_COUNTRY] == country_name]
    if row.empty:
        return {}
    row = row.iloc[0]

    return {
        "Country": row.get(COL_COUNTRY, "N/A"),
        "Continent": row.get(COL_CONTINENT, "N/A"),
        "Region": row.get(COL_REGION, "N/A"),
        "Alliance": row.get(COL_ALLIANCE, "N/A"),
        "Power Index Rank": f"#{int(row[COL_RANK])}" if pd.notna(row.get(COL_RANK)) else "N/A",
        "Power Index Score": format_score(row.get(COL_SCORE)),
        "Defense Budget": format_currency(row.get(COL_BUDGET)),
        "Active Personnel": format_plain(row.get(COL_ACTIVE)),
        "Reserve Personnel": format_plain(row.get(COL_RESERVE)),
        "Total Aircraft": format_plain(row.get(COL_AIRCRAFT)),
        "Tanks": format_plain(row.get(COL_TANKS)),
        "Naval Fleet": format_plain(row.get(COL_NAVAL)),
        "GDP": format_currency(row.get(COL_GDP)),
        "Assets per Capita": f"{row.get(COL_ASSETS_PER_CAPITA):.6f}" if pd.notna(row.get(COL_ASSETS_PER_CAPITA)) else "N/A",
        "Budget-to-GDP Ratio": f"{row.get(COL_BUDGET_TO_GDP):.2f}%" if pd.notna(row.get(COL_BUDGET_TO_GDP)) else "N/A",
    }


def get_country_long_metrics(long_df: pd.DataFrame, country_name: str) -> pd.DataFrame:
    """Returns every raw metric/value pair for one country from the long-format dataset."""
    if long_df.empty or COL_COUNTRY not in long_df.columns:
        return pd.DataFrame(columns=["Metric", "Value"])
    subset = long_df[long_df[COL_COUNTRY] == country_name][["Metric", "Value"]].reset_index(drop=True)
    return subset