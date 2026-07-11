import pandas as pd

# ---------------------------------------------------------------------------
# 1. File paths  (edit if your files live somewhere else)
# ---------------------------------------------------------------------------
MILITARY_FILE   = "military_raw_data.csv"
CONTINENTS_FILE = "continents2.csv"
GDP_FILE        = "gdp_data.csv"
NATO_FILE       = "NATO_1_Country_Stats.csv"

OUTPUT_FILE     = "military_data_merged.csv"

# ---------------------------------------------------------------------------
# 2. Load the raw data
# ---------------------------------------------------------------------------
mil  = pd.read_csv(MILITARY_FILE)
cont = pd.read_csv(CONTINENTS_FILE)
gdp  = pd.read_csv(GDP_FILE)
nato = pd.read_csv(NATO_FILE)

# Strip whitespace from country name columns so matching is clean
mil["Country"]         = mil["Country"].str.strip()
cont["name"]            = cont["name"].str.strip()
gdp["country_name"]     = gdp["country_name"].str.strip()
nato["Country"]         = nato["Country"].str.strip()

# ---------------------------------------------------------------------------
# 3. Name-mapping dictionaries
#    military_raw_data.csv country name -> matching name in the other file
# ---------------------------------------------------------------------------
MIL_TO_CONTINENTS = {
    "Beliz": "Belize",
    "Bosnia and Herzegovina": "Bosnia And Herzegovina",
    "Czechia": "Czech Republic",
    "Democratic Republic of the Congo": "Congo (Democratic Republic Of The)",
    "Ivory Coast": "Côte D'Ivoire",
    "North Macedonia": "Macedonia",
    "Republic of the Congo": "Congo",
    "South Korea": "South Korea",
    "Turkiye": "Turkey",
    # No match available in continents2.csv for these -> left as NaN
    # "Kosovo": None,
    # "North Korea": None,
}

MIL_TO_GDP = {
    "Beliz": "Belize",
    "Democratic Republic of the Congo": "Congo, Dem. Rep.",
    "Egypt": "Egypt, Arab Rep.",
    "Iran": "Iran, Islamic Rep.",
    "Ivory Coast": "Cote d'Ivoire",
    "Kyrgyzstan": "Kyrgyz Republic",
    "Laos": "Lao PDR",
    "Republic of the Congo": "Congo, Rep.",
    "Russia": "Russian Federation",
    "Slovakia": "Slovak Republic",
    "South Korea": "Korea, Rep.",
    "Syria": "Syrian Arab Republic",
    "Venezuela": "Venezuela, RB",
    "Yemen": "Yemen, Rep.",
    # No match available in gdp_data.csv for these -> left as NaN
    # "North Korea": None,
    # "Taiwan": None,
}

MIL_TO_NATO = {
    "Czechia": "Czech Republic",
    "Turkiye": "Türkiye",
    # everything else in nato['Country'] already matches military names
}

# ---------------------------------------------------------------------------
# 4. Prepare continents2.csv lookup: Country -> Continent, Region
# ---------------------------------------------------------------------------
cont_lookup = cont[["name", "region", "sub-region"]].drop_duplicates(subset="name")
cont_lookup = cont_lookup.rename(
    columns={"name": "Country", "region": "Continent", "sub-region": "Region"}
)

# Build a helper column on military data holding the name to use for the join
mil["_cont_join_name"] = mil["Country"].replace(MIL_TO_CONTINENTS)

mil = mil.merge(
    cont_lookup,
    left_on="_cont_join_name",
    right_on="Country",
    how="left",
    suffixes=("", "_cont"),
)
mil = mil.drop(columns=["_cont_join_name", "Country_cont"], errors="ignore")

# ---------------------------------------------------------------------------
# 5. Prepare gdp_data.csv lookup: Country -> most recent Year, GDP
# ---------------------------------------------------------------------------
gdp_clean = gdp.dropna(subset=["value"])
# Keep only the most recent year with a non-null GDP value for each country
gdp_latest = (
    gdp_clean.sort_values("year")
    .groupby("country_name", as_index=False)
    .last()[["country_name", "year", "value"]]
    .rename(columns={"country_name": "Country", "year": "GDP_Year", "value": "GDP"})
)

mil["_gdp_join_name"] = mil["Country"].replace(MIL_TO_GDP)

mil = mil.merge(
    gdp_latest,
    left_on="_gdp_join_name",
    right_on="Country",
    how="left",
    suffixes=("", "_gdp"),
)
mil = mil.drop(columns=["_gdp_join_name", "Country_gdp"], errors="ignore")

# ---------------------------------------------------------------------------
# 6. Prepare NATO_1_Country_Stats.csv lookup: set of NATO member countries
# ---------------------------------------------------------------------------
nato_members = set(nato["Country"].unique())

mil["_nato_join_name"] = mil["Country"].replace(MIL_TO_NATO)
mil["NATO_Ally"] = mil["_nato_join_name"].isin(nato_members)
mil = mil.drop(columns=["_nato_join_name"])

# ---------------------------------------------------------------------------
# 7. Report any countries that still failed to match (for QA)
# ---------------------------------------------------------------------------
unmatched_continent = mil.loc[mil["Continent"].isna(), "Country"].unique()
unmatched_gdp        = mil.loc[mil["GDP"].isna(), "Country"].unique()

if len(unmatched_continent):
    print("No Continent/Region match found for:", sorted(unmatched_continent))
if len(unmatched_gdp):
    print("No GDP match found for:", sorted(unmatched_gdp))

print(f"NATO allies flagged: {mil['NATO_Ally'].sum()} of {len(mil)} countries")

# ---------------------------------------------------------------------------
# 8. Save merged result
# ---------------------------------------------------------------------------
mil.to_csv(OUTPUT_FILE, index=False)
print(f"\nMerged file saved to: {OUTPUT_FILE}")
print(f"Final shape: {mil.shape[0]} rows x {mil.shape[1]} columns")