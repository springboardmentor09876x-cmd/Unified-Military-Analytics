import pandas as pd
import numpy as np

# Load cleaned dataset
clean_df = pd.read_csv("military_cleaned.csv")

print("Dataset Loaded Successfully!")
print(clean_df.shape)

# =====================================================
# KPI 1 : Assets per Capita
# =====================================================

clean_df["assets_per_capita"] = (
    clean_df["total_military_aircraft"]
    + clean_df["tanks"]
    + clean_df["total_naval_fleet"]
) / clean_df["total_population"]

print("✓ Assets per Capita calculated")

print(
    clean_df[
        ["country", "assets_per_capita"]
    ].head()
)

# =====================================================
# KPI 2 : Budget-to-GDP Ratio
# =====================================================

clean_df["budget_to_gdp_ratio"] = (
    clean_df["defense_budget_usd"]
    / clean_df["gdp_usd"]
)

print("✓ Budget to GDP Ratio calculated")

print(
    clean_df[
        ["country", "budget_to_gdp_ratio"]
    ].head()
)

# =====================================================
# KPI 3 : Power Index Rank Gap
# =====================================================

clean_df["power_index_rank_gap"] = (
    clean_df["power_index_rank"] - 1
)

print("✓ Power Index Rank Gap calculated")

print(
    clean_df[
        ["country", "power_index_rank", "power_index_rank_gap"]
    ].head()
)


# =====================================================
# Alliance Flag
# =====================================================

clean_df["alliance_flag"] = np.where(
    clean_df["alliance"] == "NATO",
    1,
    0
)

print("✓ Alliance Flag created")

print(clean_df[["country", "alliance", "alliance_flag"]].head(10))

# =====================================================
# Save Final Dataset (Wide Format)
# =====================================================

clean_df.to_excel("military_final.xlsx", index=False)

print("✓ military_final.xlsx saved successfully")
