import pandas as pd

# Main dataset
main = pd.read_csv("../data/military_dashboard_dataset.csv")

# Rank + Power Index
rank = pd.read_csv("../output/country_rank_power.csv")

# Region + Continent
meta = pd.read_csv("../metadata/Continent Region Country.csv")

# NATO Countries
nato = pd.read_csv("../metadata/NATO_1_Country_Stats.csv")

# Keep only needed columns
meta = meta[["Country", "Continent", "Region"]]

# Create NATO flag
nato = nato[["Country"]].drop_duplicates()
nato["NATO_Flag"] = 1

# Merge Rank + Power Index
main = pd.merge(main, rank, on="Country", how="left")

# Merge Region + Continent
main = pd.merge(main, meta, on="Country", how="left")

# Merge NATO Flag
main = pd.merge(main, nato, on="Country", how="left")

# Fill non-NATO countries with 0
main["NATO_Flag"] = main["NATO_Flag"].fillna(0)

# Convert to integer
main["NATO_Flag"] = main["NATO_Flag"].astype(int)

# Save final dataset
main.to_csv(
    "../output/military_dashboard_final.csv",
    index=False
)

print("Rows:", main.shape[0])
print("Columns:", main.shape[1])
print("Saved Successfully!")
print(main.columns.tolist())