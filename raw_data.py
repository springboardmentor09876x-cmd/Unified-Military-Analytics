import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

# Dictionary of URLs and metric names
metric_urls = {
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

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9"
}

# -------------------------
# Check URL status
# -------------------------
working = 0
failed = 0

print("Checking URLs...\n")

for url in metric_urls:

    try:
        response = requests.get(url, headers=headers, timeout=20)

        if response.status_code == 200:
            working += 1
        else:
            failed += 1
            print(f"Failed ({response.status_code}) : {url}")

    except Exception as e:
        failed += 1
        print(f"Error : {url}")
        print(e)

print("\nWorking URLs :", working)
print("Failed URLs  :", failed)
print("Total URLs   :", len(metric_urls))


# -------------------------
# Scraping Function
# -------------------------
def scrape_metric(url):

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()

    except Exception as e:
        print(f"Unable to open {url}")
        print(e)
        return {}

    soup = BeautifulSoup(response.text, "html.parser")

    cards = soup.find_all(
        "div",
        class_="picTrans recordsetContainer boxShadow zoom"
    )

    print(f"{url} -> {len(cards)} countries")

    data = {}

    for card in cards:

        long_name = card.find("div", class_="longFormName")
        short_name = card.find("div", class_="shortFormName")

        if long_name:
            country = long_name.get_text(strip=True)

        elif short_name:
            country = short_name.get_text(strip=True)

        else:
            continue

        value_div = card.find("div", class_="valueContainer")

        if value_div:
            value = next(value_div.stripped_strings)
            value = re.sub(r"\s+", " ", value).strip()
        else:
            value = None

        data[country] = value

    return data


# -------------------------
# Merge all data
# -------------------------
master_data = {}

print("\nScraping all pages...\n")

for url, metric in metric_urls.items():

    print(metric)

    metric_data = scrape_metric(url)

    for country, value in metric_data.items():

        if country not in master_data:
            master_data[country] = {}

        master_data[country][metric] = value

    time.sleep(2)


# -------------------------
# Create DataFrame
# -------------------------
df = pd.DataFrame.from_dict(master_data, orient="index")

df.index.name = "Country"

df.reset_index(inplace=True)

print("\nDataFrame Shape:", df.shape)

print(df.head())


# -------------------------
# Save CSV
# -------------------------
df.to_csv(
    "military_raw_data.csv",
    index=False,
    encoding="utf-8"
)

print("\nCSV file created successfully.")