import pandas as pd

print("="*60)
print("MILITARY KPI GENERATION STARTED")
print("="*60)

# Load cleaned dataset
df = pd.read_csv("final_military_cleaned.csv")

print("Dataset Loaded Successfully!")
print("Shape :", df.shape)

# -------------------------------------------------
# KPI 1 : Power Index Rank Gap
# -------------------------------------------------

df["power_index_rank_gap"] = df["power_index_rank"] - 1

# -------------------------------------------------
# KPI 2 : Assets Per Capita
# -------------------------------------------------

df["assets_per_capita"] = (
    (
        df["total_military_aircraft"] +
        df["tanks"] +
        df["total_naval_fleet"]
    ) /
    df["total_population"]
)

# -------------------------------------------------
# KPI 3 : Budget to GDP Ratio
# -------------------------------------------------

df["budget_to_gdp_ratio"] = (
    df["defense_budget_usd"] /
    df["gdp_usd"]
)

# -------------------------------------------------
# KPI 4 : Military Personnel Per Capita
# -------------------------------------------------

df["military_personnel_per_capita"] = (
    df["active_personnel"] /
    df["total_population"]
)

# -------------------------------------------------
# KPI 5 : Force Readiness Index
# -------------------------------------------------

df["force_readiness_index"] = (
    df["active_personnel"] /
    df["fit_for_service"]
)

# -------------------------------------------------
# KPI 6 : Naval to Land Ratio
# -------------------------------------------------

df["naval_to_land_ratio"] = (
    df["total_naval_fleet"] /
    df["tanks"]
)

# -------------------------------------------------
# KPI 7 : Air Superiority Index
# -------------------------------------------------

df["air_superiority_index"] = (
    df["fighter_aircraft"] /
    df["total_military_aircraft"]
)

# -------------------------------------------------
# KPI 8 : Logistics Index
# -------------------------------------------------

df["logistics_index"] = (
    df["roadway_coverage_km"] +
    df["railway_coverage_km"] +
    df["major_ports_and_terminals"] +
    df["total_serviceable_airports"]
)

# -------------------------------------------------
# Replace Infinity values
# -------------------------------------------------

df.replace([float("inf"), float("-inf")], 0, inplace=True)

# Fill Missing Values

df.fillna(0, inplace=True)

# -------------------------------------------------
# Save Excel
# -------------------------------------------------

df.to_excel(
    "military_final.xlsx",
    index=False
)

# -------------------------------------------------
# Create Long Format
# -------------------------------------------------

long_df = df.melt(
    id_vars=[
        "country",
        "continent",
        "region",
        "alliance"
    ],
    var_name="Metric",
    value_name="Value"
)

long_df.to_excel(
    "military_long.xlsx",
    index=False
)

print("="*60)
print("MODULE 3 COMPLETED SUCCESSFULLY")
print("="*60)

print("Files Generated")
print("1. military_final.xlsx")
print("2. military_long.xlsx")