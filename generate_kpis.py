import pandas as pd

print("Loading datasets...")

# -------------------------
# Read files
# -------------------------

military = pd.read_csv("military_data.csv")
power = pd.read_csv("power_rank.csv")

continent = pd.read_csv("dataset/continents2.csv")
gdp = pd.read_csv("dataset/gdp_data.csv")
nato = pd.read_csv("dataset/NATO_1_Country_Stats.csv")

# -------------------------
# Rename columns
# -------------------------

continent.rename(columns={"name":"Country"}, inplace=True)

gdp = gdp[gdp["year"]==2022]

gdp.rename(columns={
    "country_name":"Country",
    "value":"GDP_USD"
}, inplace=True)

# -------------------------
# Country name fixes
# -------------------------

military["Country"] = military["Country"].replace({
    "Beliz":"Belize"
})

continent["Country"] = continent["Country"].replace({
    "Congo, Dem. Rep.":"Democratic Republic of the Congo",
    "Congo, Rep.":"Republic of the Congo",
    "Korea, Dem. People's Rep.":"North Korea",
    "Türkiye":"Turkiye",
    "Czech Republic":"Czechia",
    "Côte d'Ivoire":"Ivory Coast"
})

gdp["Country"] = gdp["Country"].replace({
    "Russian Federation":"Russia",
    "Korea, Rep.":"South Korea",
    "Korea, Dem. People's Rep.":"North Korea",
    "Iran, Islamic Rep.":"Iran",
    "Egypt, Arab Rep.":"Egypt",
    "Congo, Dem. Rep.":"Democratic Republic of the Congo",
    "Congo, Rep.":"Republic of the Congo",
    "Syrian Arab Republic":"Syria",
    "Yemen, Rep.":"Yemen",
    "Venezuela, RB":"Venezuela",
    "Slovak Republic":"Slovakia",
    "Kyrgyz Republic":"Kyrgyzstan",
    "Lao PDR":"Laos",
    "Cote d'Ivoire":"Ivory Coast"
})

# -------------------------
# Keep required columns
# -------------------------

continent = continent[["Country","region","sub-region"]]

gdp = gdp[["Country","GDP_USD"]]

nato = nato[["Country"]].drop_duplicates()
nato["NATO"]="Yes"

# -------------------------
# Merge
# -------------------------

df = military.merge(power,on="Country",how="left")

df = df.merge(continent,on="Country",how="left")

df = df.merge(gdp,on="Country",how="left")

df = df.merge(nato,on="Country",how="left")

df["NATO"] = df["NATO"].fillna("No")

# -------------------------
# Numeric Conversion
# -------------------------

cols = [
    "total_population",
    "total_military_aircraft",
    "tanks",
    "total_naval_fleet",
    "defense_budget_usd",
    "GDP_USD",
    "power_rank"
]

for c in cols:

    df[c] = (
        df[c]
        .astype(str)
        .str.replace(",","",regex=False)
        .str.replace("$","",regex=False)
    )

    df[c] = pd.to_numeric(df[c],errors="coerce")

# -------------------------
# GDP Rank
# -------------------------

df["GDP_Rank"] = df["GDP_USD"].rank(
    ascending=False,
    method="min"
)

# -------------------------
# KPIs
# -------------------------

df["Power_Index_Rank_Gap"] = (
    df["power_rank"] -
    df["GDP_Rank"]
)

df["Assets_per_Capita"] = (
    (
        df["total_military_aircraft"].fillna(0)
        +
        df["tanks"].fillna(0)
        +
        df["total_naval_fleet"].fillna(0)
    )
    /
    df["total_population"]
)

df["Budget_to_GDP_Ratio"] = (
    df["defense_budget_usd"] /
    df["GDP_USD"]
)

# -------------------------
# Long Format
# -------------------------

long_df = pd.melt(

    df,

    id_vars=["Country"],

    value_vars=[
        "Power_Index_Rank_Gap",
        "Assets_per_Capita",
        "Budget_to_GDP_Ratio"
    ],

    var_name="Metric",

    value_name="Value"
)

# -------------------------
# Save Excel
# -------------------------

with pd.ExcelWriter("military_final.xlsx") as writer:

    df.to_excel(
        writer,
        sheet_name="Wide",
        index=False
    )

    long_df.to_excel(
        writer,
        sheet_name="Long",
        index=False
    )

print("\nDone!")
print("military_final.xlsx created successfully.")