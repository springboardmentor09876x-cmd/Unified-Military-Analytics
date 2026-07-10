import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0"
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0 Safari/537.36"
}

URLS = {
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

def scrape_page(url):
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.find_all("div", class_="picTrans recordsetContainer boxShadow zoom")

    data = {}

    for card in cards:
        try:
            country = card.find("div", class_="longFormName").get_text(strip=True)
            value = card.find("div", class_="valueContainer").find_all("span")[-1].get_text(strip=True)

            data[country] = value

        except:
            continue

    return data
    
all_data = {}

for url, column in URLS.items():
    print(f"Scraping {column}...")

    try:
        all_data[column] = scrape_page(url)
        time.sleep(1)

    except Exception as e:
        print(f"Error in {column}: {e}")

df = pd.DataFrame(all_data)
df = df.sort_index().reset_index()
df.rename(columns={"index": "country_name"}, inplace=True)

print("\nPreview:")
print(df.head())

print("\nRows, Columns:")
print(df.shape)

# Save CSV
df.to_csv("military_raw_data.csv", index=False, encoding="utf-8-sig")

print("\nCSV file saved successfully!")


try:
    from IPython.display import display
    display(df)
except:
    pass
    
