# ============================================================
# Import Required Libraries
# ============================================================

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# ============================================================
# Base URL - Global Firepower Countries Listing
# ============================================================

base_url = "https://www.globalfirepower.com/countries-listing.php"


# ============================================================
# Military Metrics URLs
# Key   -> GFP URL
# Value -> Column name in the final dataset
# ============================================================

other_sources = {
    "https://www.globalfirepower.com/total-population-by-country.php": "total_population",
    "https://www.globalfirepower.com/available-military-manpower.php": "total_military_manpower",
    "https://www.globalfirepower.com/manpower-fit-for-military-service.php": "fit_for_service",
    "https://www.globalfirepower.com/manpower-reaching-military-age-annually.php": "population_reaching_military_age_annually",
    "https://www.globalfirepower.com/active-military-manpower.php": "active_personnel",
    "https://www.globalfirepower.com/active-reserve-military-manpower.php": "reserve_personnel",
    "https://www.globalfirepower.com/manpower-paramilitary.php": "paramilitary",
    "https://www.globalfirepower.com/aircraft-total.php": "total_military_aircraft",
    "https://www.globalfirepower.com/aircraft-total-fighters.php": "fighter_aircraft",
    "https://www.globalfirepower.com/aircraft-total-attack-types.php": "attack_aircraft",
    "https://www.globalfirepower.com/aircraft-total-transports.php": "transport_aircraft",
    "https://www.globalfirepower.com/aircraft-total-trainers.php": "trainer_aircraft",
    "https://www.globalfirepower.com/aircraft-total-special-mission.php": "special_mission_aircraft",
    "https://www.globalfirepower.com/aircraft-total-tanker-fleet.php": "tanker_aircraft",
    "https://www.globalfirepower.com/aircraft-helicopters-total.php": "total_military_helicopters",
    "https://www.globalfirepower.com/aircraft-helicopters-attack.php": "attack_helicopters",
    "https://www.globalfirepower.com/armor-tanks-total.php": "tanks",
    "https://www.globalfirepower.com/armor-apc-total.php": "armored_fighting_vehicles",
    "https://www.globalfirepower.com/armor-self-propelled-guns-total.php": "self_propelled_artillery",
    "https://www.globalfirepower.com/armor-towed-artillery-total.php": "towed_artillery",
    "https://www.globalfirepower.com/armor-mlrs-total.php": "rocket_projectors",
    "https://www.globalfirepower.com/navy-ships.php": "total_naval_fleet",
    "https://www.globalfirepower.com/navy-force-by-tonnage.php": "total_naval_fleet_tonnage_mt",
    "https://www.globalfirepower.com/navy-aircraft-carriers.php": "aircraft_carriers",
    "https://www.globalfirepower.com/navy-helo-carriers.php": "helicopter_carriers",
    "https://www.globalfirepower.com/navy-submarines.php": "submarines",
    "https://www.globalfirepower.com/navy-destroyers.php": "destroyers",
    "https://www.globalfirepower.com/navy-frigates.php": "frigates",
    "https://www.globalfirepower.com/navy-corvettes.php": "corvettes",
    "https://www.globalfirepower.com/navy-patrol-coastal-craft.php": "coastal_patrol_craft",
    "https://www.globalfirepower.com/navy-mine-warfare-craft.php": "mine_warfare_craft",
    "https://www.globalfirepower.com/defense-spending-budget.php": "defense_budget_usd",
    "https://www.globalfirepower.com/external-debt-by-country.php": "external_debt_usd",
    "https://www.globalfirepower.com/purchasing-power-parity.php": "purchasing_power_parity_usd",
    "https://www.globalfirepower.com/reserves-of-foreign-exchange-and-gold.php": "foreign_exchange_and_gold_reserves_usd",
    "https://www.globalfirepower.com/major-serviceable-airports-by-country.php": "total_serviceable_airports",
    "https://www.globalfirepower.com/labor-force-by-country.php": "labour_force",
    "https://www.globalfirepower.com/major-ports-and-terminals.php": "major_ports_and_terminals",
    "https://www.globalfirepower.com/merchant-marine-strength-by-country.php": "total_merchant_marine_fleet",
    "https://www.globalfirepower.com/railway-coverage.php": "railway_coverage_km",
    "https://www.globalfirepower.com/roadway-coverage.php": "roadway_coverage_km",
    "https://www.globalfirepower.com/oil-production-by-country.php": "oil_production_bbl",
    "https://www.globalfirepower.com/oil-consumption-by-country.php": "oil_consumption_bbl",
    "https://www.globalfirepower.com/proven-oil-reserves-by-country.php": "proven_oil_reserves_bbl",
    "https://www.globalfirepower.com/natural-gas-production-by-country.php": "natural_gas_production_cum",
    "https://www.globalfirepower.com/natural-gas-consumption-by-country.php": "natural_gas_consumption_cum",
    "https://www.globalfirepower.com/proven-natural-gas-reserves-by-country.php": "proven_natural_gas_reserves_cum",
    "https://www.globalfirepower.com/coal-production-by-country.php": "coal_production_cum",
    "https://www.globalfirepower.com/coal-consumption-by-country.php": "coal_consumption_mt",
    "https://www.globalfirepower.com/proven-coal-reserves-by-country.php": "proven_coal_reserves_cum",
    "https://www.globalfirepower.com/square-land-area.php": "total_land_area_sq_km",
    "https://www.globalfirepower.com/coastline-coverage.php": "coastline_coverage_km",
    "https://www.globalfirepower.com/border-coverage.php": "border_coverage_km",
    "https://www.globalfirepower.com/waterway-coverage.php": "waterway_coverage_km",
}


# Request Headers
# Helps avoid request blocking while scraping


headers = {
    "User-Agent": "Mozilla/5.0"
}

# ============================================================
# Check whether all URLs are working
# ============================================================

working = 0
failed = 0

for url, metric in other_sources.items():
    try:
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code == 200:
            working += 1
        else:
            failed += 1

    except Exception as e:
        print(f"{metric} -> ERROR: {e}")
        failed += 1


print(f"Working URLs : {working}")
print(f"Failed URLs  : {failed}")
print(f"Total URLs   : {len(other_sources)}")

# ============================================================
# Function to Scrape Data from a Single GFP Metric Page
# ============================================================

def scrape_metric(url):
    """
    Scrapes country names and corresponding metric values
    from a single Global Firepower metric page.

    Parameters:
        url (str): GFP metric page URL

    Returns:
        dict: {country_name: metric_value}
    """

    # Send request to the webpage
    response = requests.get(url, headers=headers)

    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all country cards
    cards = soup.find_all(
        "div",
        class_="picTrans recordsetContainer boxShadow zoom"
    )

    data = {}

    # Loop through each country card
    for card in cards:

        # Get full country name
        long_name = card.find("div", class_="longFormName")

        if long_name:
            country = long_name.get_text(strip=True)
        else:
            country = card.find(
                "div",
                class_="shortFormName"
            ).get_text(strip=True)

        # Get metric value
        value_div = card.find("div", class_="valueContainer")

        if value_div:
            value = next(value_div.stripped_strings)
            value = re.sub(r"\s+", " ", value).strip()
        else:
            value = None

        # Store country and value
        data[country] = value

    return data
# ============================================================
# Function to Scrape Power Index Ranking
# ============================================================

def scrape_power_index():

    url = "https://www.globalfirepower.com/countries-listing.php"

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    cards = soup.find_all(
        "div",
        class_="picTrans recordsetContainer boxShadow zoom"
    )

    power_data = []

    rank = 1

    for card in cards:

        long_name = card.find("div", class_="longFormName")

        if long_name:
            country = long_name.get_text(strip=True)
        else:
            country = card.find(
                "div",
                class_="shortFormName"
            ).get_text(strip=True)

        power_index = None

        value_div = card.find("div", class_="valueContainer")

        if value_div:
            power_index = next(value_div.stripped_strings)

        power_data.append({
            "Country": country,
            "power_index_rank": rank,
            "power_index_score": power_index
        })

        rank += 1

    return pd.DataFrame(power_data)
# ============================================================
# Merge all scraped metrics into one dataset
# ============================================================

master_data = {}

# Loop through every metric URL
for url, metric in other_sources.items():

    print(f"Scraping: {metric}")

    # Scrape data for one metric
    metric_data = scrape_metric(url)

    # Merge into master dictionary using Country as key
    for country, value in metric_data.items():

        if country not in master_data:
            master_data[country] = {}

        master_data[country][metric] = value
        
        # ============================================================
# Convert Master Dictionary to DataFrame
# ============================================================

# Create DataFrame from the master dictionary
df = pd.DataFrame.from_dict(master_data, orient="index")

# Move country names from index to a normal column
df.index.name = "Country"
df.reset_index(inplace=True)

# Display dataset information
print("\nDataset Shape:", df.shape)
print("\nFirst 5 Rows:")
print(df.head())

# ============================================================
# Save DataFrame as CSV
# ============================================================

df.to_csv(
    "military_raw_data.csv",
    index=False,
    encoding="utf-8"
)

# ============================================================
# Merge Power Index into Main Dataset
# ============================================================

# Scrape Power Index data
power_df = scrape_power_index()

# Merge with main dataframe
df = df.merge(
    power_df,
    on="Country",
    how="left"
)

print("\nPower Index merged successfully!")

print("\nDataset Shape After Power Index Merge:")
print(df.shape)

print("\nPower Index Preview:")
print(df[["Country", "power_index_rank", "power_index_score"]].head())
# ------------------------------------------------------------
# Load External Datasets
# ------------------------------------------------------------
# ------------------------------------------------------------
# Load External Datasets
# ------------------------------------------------------------

# continent_df = pd.read_csv("datasets/continents2.csv")

# gdp_df = pd.read_csv("datasets/gdp_data.csv")

# nato_df = pd.read_csv("datasets/NATO_1_Country_Stats.csv")

# print("External datasets loaded successfully!")

# print("\n military_raw_data.csv created successfully!")

# print("\nMilitary Dataset Columns:")
# print(df.columns.tolist())

# print("\nContinent Dataset Columns:")
# print(continent_df.columns.tolist())

# print("\nGDP Dataset Columns:")
# print(gdp_df.columns.tolist())

# print("\nNATO Dataset Columns:")
# print(nato_df.columns.tolist())

# ============================================================
# Compare Master Dashboard Columns with Scraped Dataset
# ============================================================

# Read Master Dashboard (reference file)
master_df = pd.read_excel("GFP_Military_Dashboard.xlsx")

# Get column names
scraped_columns = set(df.columns)
master_columns = set(master_df.columns)

# Find missing columns
missing_columns = master_columns - scraped_columns
extra_columns = scraped_columns - master_columns

print("\n" + "=" * 60)
print("COLUMN COMPARISON")
print("=" * 60)

print(f"Total Scraped Columns : {len(scraped_columns)}")
print(f"Total Master Columns  : {len(master_columns)}")

print("\nColumns Missing from Scraped Dataset:")
for col in sorted(missing_columns):
    print("-", col)

print("\nExtra Columns in Scraped Dataset:")
for col in sorted(extra_columns):
    print("-", col)
    
    
    # ============================================================
# Load External Datasets
# ============================================================

continent_df = pd.read_csv("datasets/continents2.csv")
gdp_df = pd.read_csv("datasets/gdp_data.csv")
nato_df = pd.read_csv("datasets/NATO_1_Country_Stats.csv")

print("External datasets loaded successfully!")

print("\nContinent Columns")
print(continent_df.columns.tolist())

print("\nGDP Columns")
print(gdp_df.columns.tolist())

print("\nNATO Columns")
print(nato_df.columns.tolist())

# ============================================================
# Prepare Lookup Tables
# ============================================================

# Keep only required columns from Continent dataset
continent_df = continent_df[["name", "region", "sub-region"]]
continent_df.rename(columns={
    "name": "Country",
    "region": "continent",
    "sub-region": "region"
}, inplace=True)

# Keep only latest GDP values
gdp_df = gdp_df.sort_values("year").drop_duplicates(
    subset="country_name",
    keep="last"
)

gdp_df = gdp_df[["country_name", "value"]]
gdp_df.rename(columns={
    "country_name": "Country",
    "value": "gdp_usd"
}, inplace=True)

# Create Alliance column from NATO dataset
nato_df["alliance"] = "NATO"

nato_df = nato_df[["Country", "alliance"]]
nato_df.drop_duplicates(inplace=True)

print("\nLookup tables prepared successfully!")

# ============================================================
# Merge External Datasets with Scraped Dataset
# ============================================================

# Merge Continent & Region
df = df.merge(
    continent_df,
    on="Country",
    how="left"
)

# Merge GDP
df = df.merge(
    gdp_df,
    on="Country",
    how="left"
)

# Merge Alliance
df = df.merge(
    nato_df,
    on="Country",
    how="left"
)

print("\nExternal datasets merged successfully!")


# ============================================================
# Save Final Merged Dataset
# ============================================================

df.to_csv(
    "military_raw_data.csv",
    index=False,
    encoding="utf-8"
)

print("\nFinal merged dataset saved successfully!")

print("\nFinal Dataset Shape:", df.shape)

print("\nFinal Dataset Columns:")
print(df.columns.tolist())

# ============================================================
# Verify Merged Data
# ============================================================

print("\nMerged Dataset Preview:")
print(df[["Country", "continent", "region", "gdp_usd", "alliance"]].head(15))

print("\nMissing Values:")
print(df[["continent", "region", "gdp_usd", "alliance"]].isnull().sum())

print("\nFinal Dataset Shape:", df.shape)


# Rename Country column
df.rename(columns={"Country": "country"}, inplace=True)

# Add Country ID
df.insert(0, "country_id", range(1, len(df) + 1))

# Save updated dataset
df.to_csv(
    "military_raw_data.csv",
    index=False,
    encoding="utf-8"
)

print("\nFinal dataset saved successfully!")

print("\nColumns still missing:")

missing = sorted(list(set(master_columns) - set(df.columns)))

for col in missing:
    print("-", col)