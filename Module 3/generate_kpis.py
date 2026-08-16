import pandas as pd

df = pd.read_csv("military_master.csv")
df["gdp_rank"] = (
    df["purchasing_power_parity_usd"]
    .rank(ascending=False, method="dense")
    .astype(int)
)
df["total_assets"] = (
    df["total_military_aircraft"] +
    df["tanks"] +
    df["destroyers"] +
    df["frigates"] +
    df["corvettes"] +
    df["submarines"] +
    df["aircraft_carriers"] +
    df["helicopter_carriers"]
)
df["assets_per_capita"] = (
    df["total_assets"] /
    df["total_population"]
)
df["budget_to_gdp_ratio"] = (
    df["defense_budget_usd"] /
    df["purchasing_power_parity_usd"]
)
df["power_index_rank_gap"] = (
    df["power_index_rank"] -
    df["gdp_rank"]
)
# print(df[[
#     "country",
#     "power_index_rank",
#     "gdp_rank",
#     "power_index_rank_gap",
#     "total_assets",
#     "assets_per_capita",
#     "budget_to_gdp_ratio"
# ]].head())
df.to_csv("data/military_final.csv", index=False)
df.to_excel("military_final.xlsx", index=False)

