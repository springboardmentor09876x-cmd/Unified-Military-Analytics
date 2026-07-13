####   MODULE 1 - Scraping Setup and Execution   #####

#importing packages
import requests
from bs4 import BeautifulSoup
import pandas as pd 
import re
#TASK 2
metric_urls = {
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
    "https://www.globalfirepower.com/waterway-coverage.php": "waterway_coverage_km"
}

#---------------Checking the status of each URL------------------
headers = {"User-Agent": "Mozilla/5.0"}
working = 0
failed = 0
for url, metric in metric_urls.items():
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            #print(f"{metric:45} {response.status_code}")
            working += 1
        else:
            #print(f"{metric:45} {response.status_code}")
            failed += 1
    except Exception as e:
        print(f"{metric:45} ERROR: {e}")
        failed += 1
print(f"Working URLs : {working}")
print(f"Failed URLs  : {failed}")
print(f"Total URLs   : {len(metric_urls)}")
#-------------Function to scrape data from a given URL-------------------
def scrape_metric(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.find_all("div", class_="picTrans recordsetContainer boxShadow zoom")
    data = {}
    for card in cards:
        #Country name
        long_name = card.find("div", class_="longFormName")
        if long_name:
          country = long_name.get_text(strip=True)
        else:
          country = card.find("div", class_="shortFormName").get_text(strip=True)
        #Value
        value_div = card.find("div", class_="valueContainer")
        if value_div:
          value = next(value_div.stripped_strings)
          value = re.sub(r"\s+", " ", value).strip()
        else:
          value = None
        data[country] = value
    #print(url, len(data))
    return data
#----------Merge all metrics into a single DataFrame------------------
master_data={}
for url, metric in metric_urls.items():
    #print(f"Scraping {metric}")
    metric_data = scrape_metric(url)
    for country, value in metric_data.items():
      if country not in master_data:
        master_data[country] = {}
      master_data[country][metric] = value
df = pd.DataFrame.from_dict(master_data,orient="index")
df.index.name = "Country"
df.reset_index(inplace=True)
#print(df.shape)
#print(df.head())
#print(df.columns.tolist())
#-------------Save the DataFrame to a CSV file-------------
df.to_csv("military_raw_data.csv", index=False, encoding="utf-8")
#print("military_raw_data.csv created successfully.")


#          ********MERGING WITH EXISTING DATASET**********

lookup_file = "Military_Dataset_Missed_Columns.xlsx"
#Correcting country name discrepancies

country_mapping = {
    "Democratic Republic of the Congo": "Congo (Democratic Republic Of The)",
    "Republic of the Congo": "Congo",
    "Turkiye": "Turkey",
    "Czechia": "Czech Republic",
    "Bosnia and Herzegovina": "Bosnia And Herzegovina",
    "North Macedonia": "Macedonia",
    "Beliz": "Belize",
    "Ivory Coast": "Côte D'Ivoire",
}
df["Country"] = df["Country"].replace(country_mapping)
#print(df[df["Country"].isin(country_mapping.values())][["Country"]])


#----------Continent and Region information-------------
continent_df = pd.read_excel( lookup_file, sheet_name="Continent & Region")
df = df.merge(continent_df, on="Country", how="left")
#print(df.columns.tolist())
#print(continent_df.columns.tolist())

#---------Merging GDP information-----------
gdp_df = pd.read_excel(lookup_file,sheet_name="GDP - 1")
# Keep only the latest year for each country
gdp_latest = (gdp_df.sort_values("Year").groupby("Country", as_index=False).last())
# Standardize GDP country names to match the main dataset
gdp_mapping = {
    "Russian Federation": "Russia",
    "Egypt, Arab Rep.": "Egypt",
    "Iran, Islamic Rep.": "Iran",
    "Korea, Rep.": "South Korea",
    "Congo, Dem. Rep.": "Congo (Democratic Republic Of The)",
    "Congo, Rep.": "Congo",
    "Bosnia and Herzegovina": "Bosnia And Herzegovina",
    "Czechia": "Czech Republic",
    "Lao PDR": "Laos",
    "North Macedonia": "Macedonia",
    "Slovak Republic": "Slovakia",
    "Venezuela, RB": "Venezuela",
    "Yemen, Rep.": "Yemen",
    "Turkiye": "Turkey",
    "Cote d'Ivoire": "Côte D'Ivoire",
    "Kyrgyz Republic": "Kyrgyzstan",
    "Syrian Arab Republic": "Syria"
}
gdp_latest["Country"] = gdp_latest["Country"].replace(gdp_mapping)
# Rename GDP column
gdp_latest.rename(columns={"GDP": "GDP_USD"}, inplace=True)
gdp_latest = gdp_latest[["Country", "GDP_USD"]]
df = df.merge(gdp_latest, on="Country", how="left")

#----------Merging NATO membership information-----------
nato_df = pd.read_excel(lookup_file, sheet_name="NATO Alliance")
nato_df["NATO_Member"] = "Yes"
nato_df.rename(columns={"NATO Allied Countries": "Country"}, inplace=True)
df = df.merge(nato_df[["Country", "NATO_Member"]],on="Country",how="left")
df["NATO_Member"] = df["NATO_Member"].fillna("No")
#print(df[df["NATO_Member"] == "Yes"].head())
#print(df["NATO_Member"].value_counts())

#------------Saving the merged DataFrame to a CSV file---------------
df.to_csv("military_raw_data.csv", index=False)
#print("Merged military_raw_data.csv created successfully.")
#print(df.shape)
#print(df.head())


#         *******Scraping and Merging Power Index Rank and Score**********

url = "https://www.globalfirepower.com/countries-listing.php"
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
power_data = []
records = soup.find_all("div", class_="picTrans recordsetContainer boxShadow zoom")
for record in records:
    # Country Name
    country = record.find("div", class_="longFormName").get_text(strip=True)
     # Rank
    rank = record.find("div", class_="rankNumContainer").get_text(strip=True)
     # Power Index Score
    pwr = record.find("div", class_="pwrIndxContainer").get_text(strip=True)
    pwr = pwr.replace("PwrIndx:", "").strip()
    power_data.append({
        "Country": country,
        "power_index_rank": rank,
        "power_index_score": pwr
    })
#----------Convert to DataFrame----------------------
power_df = pd.DataFrame(power_data)
#print(power_df.head())
#print(power_df.shape)

# Fix country name if necessary
# Standardize country names in Power Index data
power_mapping = {
    "Turkiye": "Turkey",
    "Czechia": "Czech Republic",
    "Democratic Republic of the Congo": "Congo (Democratic Republic Of The)",
    "Republic of the Congo": "Congo",
    "Ivory Coast": "Côte D'Ivoire",
    "North Macedonia": "Macedonia",
    "Bosnia and Herzegovina": "Bosnia And Herzegovina",
    "Beliz": "Belize",
    "United States of America": "United States"
}
power_df["Country"] = power_df["Country"].replace(power_mapping)

#-----------Merging Power Index DataFrame with the main DataFrame------------
df = df.merge(power_df, on="Country", how="left")
df.columns = df.columns.str.lower()
#print(df.head())
#print(df.shape)


#         ********FINAL DATASET FOR ANALYSIS******
df.to_csv("military_raw_data.csv", index=False)
print("Final military_raw_data.csv created successfully.")
print(df.shape)
print(df)
