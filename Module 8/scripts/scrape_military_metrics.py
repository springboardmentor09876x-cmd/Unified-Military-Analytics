import os
import re
import ast
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}
OUTPUT_FILE = "military_raw_data.csv"
DEBUG_DIR = "debug_html"

base_url = 'https://www.globalfirepower.com/countries-listing.php'
other_sources = {
    'https://www.globalfirepower.com/total-population-by-country.php': 'total_population',
    'https://www.globalfirepower.com/available-military-manpower.php': 'total_military_manpower',
    'https://www.globalfirepower.com/manpower-fit-for-military-service.php': 'fit_for_service',
    'https://www.globalfirepower.com/manpower-reaching-military-age-annually.php': 'population_reaching_military_age_annually',
    'https://www.globalfirepower.com/active-military-manpower.php': 'active_personnel',
    'https://www.globalfirepower.com/active-reserve-military-manpower.php': 'reserve_personnel',
    'https://www.globalfirepower.com/manpower-paramilitary.php': 'paramilitary',
    'https://www.globalfirepower.com/aircraft-total.php': 'total_military_aircraft',
    'https://www.globalfirepower.com/aircraft-total-fighters.php': 'fighter_aircraft',
    'https://www.globalfirepower.com/aircraft-total-attack-types.php': 'attack_aircraft',
    'https://www.globalfirepower.com/aircraft-total-transports.php': 'transport_aircraft',
    'https://www.globalfirepower.com/aircraft-total-trainers.php': 'trainer_aircraft',
    'https://www.globalfirepower.com/aircraft-total-special-mission.php': 'special_mission_aircraft',
    'https://www.globalfirepower.com/aircraft-total-tanker-fleet.php': 'tanker_aircraft',
    'https://www.globalfirepower.com/aircraft-helicopters-total.php': 'total_military_helicopters',
    'https://www.globalfirepower.com/aircraft-helicopters-attack.php': 'attack_helicopters',
    'https://www.globalfirepower.com/armor-tanks-total.php': 'tanks',
    'https://www.globalfirepower.com/armor-apc-total.php': 'armored_fighting_vehicles',
    'https://www.globalfirepower.com/armor-self-propelled-guns-total.php': 'self_propelled_artillery',
    'https://www.globalfirepower.com/armor-towed-artillery-total.php': 'towed_artillery',
    'https://www.globalfirepower.com/armor-mlrs-total.php': 'rocket_projectors',
    'https://www.globalfirepower.com/navy-ships.php': 'total_naval_fleet',
    'https://www.globalfirepower.com/navy-force-by-tonnage.php': 'total_naval_fleet_tonnage_mt',
    'https://www.globalfirepower.com/navy-aircraft-carriers.php': 'aircraft_carriers',
    'https://www.globalfirepower.com/navy-helo-carriers.php': 'helicopter_carriers',
    'https://www.globalfirepower.com/navy-submarines.php': 'submarines',
    'https://www.globalfirepower.com/navy-destroyers.php': 'destroyers',
    'https://www.globalfirepower.com/navy-frigates.php': 'frigates',
    'https://www.globalfirepower.com/navy-corvettes.php': 'corvettes',
    'https://www.globalfirepower.com/navy-patrol-coastal-craft.php': 'coastal_patrol_craft',
    'https://www.globalfirepower.com/navy-mine-warfare-craft.php': 'mine_warfare_craft',
    'https://www.globalfirepower.com/defense-spending-budget.php': 'defense_budget_usd',
    'https://www.globalfirepower.com/external-debt-by-country.php': 'external_debt_usd',
    'https://www.globalfirepower.com/purchasing-power-parity.php': 'purchasing_power_parity_usd',
    'https://www.globalfirepower.com/reserves-of-foreign-exchange-and-gold.php': 'foreign_exchange_and_gold_reserves_usd',
    'https://www.globalfirepower.com/major-serviceable-airports-by-country.php': 'total_serviceable_airports',
    'https://www.globalfirepower.com/labor-force-by-country.php': 'labour_force',
    'https://www.globalfirepower.com/major-ports-and-terminals.php': 'major_ports_and_terminals',
    'https://www.globalfirepower.com/merchant-marine-strength-by-country.php': 'total_merchant_marine_fleet',
    'https://www.globalfirepower.com/railway-coverage.php': 'railway_coverage_km',
    'https://www.globalfirepower.com/roadway-coverage.php': 'roadway_coverage_km',
    'https://www.globalfirepower.com/oil-production-by-country.php': 'oil_production_bbl',
    'https://www.globalfirepower.com/oil-consumption-by-country.php': 'oil_consumption_bbl',
    'https://www.globalfirepower.com/proven-oil-reserves-by-country.php': 'proven_oil_reserves_bbl',
    'https://www.globalfirepower.com/natural-gas-production-by-country.php': 'natural_gas_production_cum',
    'https://www.globalfirepower.com/natural-gas-consumption-by-country.php': 'natural_gas_consumption_cum',
    'https://www.globalfirepower.com/proven-natural-gas-reserves-by-country.php': 'proven_natural_gas_reserves_cum',
    'https://www.globalfirepower.com/coal-production-by-country.php': 'coal_production_cum',
    'https://www.globalfirepower.com/coal-consumption-by-country.php': 'coal_consumption_mt',
    'https://www.globalfirepower.com/proven-coal-reserves-by-country.php': 'proven_coal_reserves_cum',
    'https://www.globalfirepower.com/square-land-area.php': 'total_land_area_sq_km',
    'https://www.globalfirepower.com/coastline-coverage.php': 'coastline_coverage_km',
    'https://www.globalfirepower.com/border-coverage.php': 'border_coverage_km',
    'https://www.globalfirepower.com/waterway-coverage.php': 'waterway_coverage_km'
}

def scrape_page(url, metric_name, retries=3):
    page = None
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code == 200:
                page = resp
                break
            else:
                print(f"Attempt {attempt+1} failed: Status {resp.status_code} on {url}")
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt+1} error: {e} on {url}")
        time.sleep(3)
        
    if page is None:
        print(f"Failed to fetch: {url}")
        return None
        
    # Save debug HTML
    safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', metric_name)
    with open(os.path.join(DEBUG_DIR, f"{safe_name}.html"), "w", encoding="utf-8") as f:
        f.write(page.text)

    soup = BeautifulSoup(page.text, "html.parser")
    data = {}
    for country_div in soup.find_all("div", class_="longFormName"):
        country = country_div.get_text(strip=True)
        row = country_div
        value_div = None
        for _ in range(6):
            row = row.parent
            if row is None:
                break
            value_div = row.find("div", class_="valueContainer")
            if value_div:
                break
        if value_div:
            data[country] = value_div.get_text(strip=True)
        else:
            print(f"Warning: no value found for {country} on {url}")
            
    if len(data) == 0:
        print(f"No data extracted : {url}")
        return None
    return data

def main():
    os.makedirs(DEBUG_DIR, exist_ok=True)
    
    print("=" * 60)
    print("Starting pipeline using hardcoded URLs")
    if not base_url:
        print("Error: base_url not found.")
        return
        
    print("=" * 60)
    print("STEP 1: Scraping Power Index")
    print("=" * 60)
    
    try:
        page = requests.get(base_url, headers=headers, timeout=15)
        page.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch base URL: {e}")
        return
    
    with open(os.path.join(DEBUG_DIR, "power_index.html"), "w", encoding="utf-8") as f:
        f.write(page.text)
        
    soup = BeautifulSoup(page.text, "html.parser")
    pi_data = {}
    for country_div in soup.find_all("div", class_="longFormName"):
        country = country_div.get_text(strip=True)
        row = country_div
        value_div = None
        for _ in range(6):
            row = row.parent
            if row is None:
                break
            value_div = row.find("div", class_="pwrIndxContainer")
            if value_div:
                break
        if value_div:
            raw = value_div.get_text(strip=True)
            pi_data[country] = raw.replace("PwrIndx:", "").strip()
        else:
            print(f"Warning: no Power Index found for {country}")
            
    df = pd.DataFrame({
        "Country": list(pi_data.keys()),
        "Power Index": list(pi_data.values())
    })
    print("Power Index Scrape:", "Success" if df.shape[0] >= 140 else "Failure or too few countries")
    
    print("\n" + "=" * 60)
    print("STEP 2: Scraping remaining metrics")
    print("=" * 60)
    
    master = None
    success_count = 0
    total_urls = len(other_sources)
    
    for i, (src_url, column_name) in enumerate(other_sources.items(), start=1):
        print(f"[{i}/{total_urls}] Scraping {column_name}")
        data = scrape_page(src_url, column_name)
        if data is None:
            continue
            
        success_count += 1
        if master is None:
            master = pd.DataFrame({"Country": list(data.keys())})
            
        # Add data map to master df
        # Create temporary df to merge and handle countries that might not exist in first metric
        temp_df = pd.DataFrame({"Country": list(data.keys()), column_name: list(data.values())})
        master = master.merge(temp_df, on="Country", how="outer")
        time.sleep(1)
        
    url_success_rate = (success_count / total_urls) * 100
    print(f"\nURL Success Rate: {url_success_rate:.2f}%")
    
    # Merge Power Index into Master
    if master is not None:
        master = df.merge(master, on="Country", how="left")
        master.to_csv(OUTPUT_FILE, index=False)
        print("\n" + "=" * 60)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print(f"Final rows             : {len(master)}")
        print(f"Final columns          : {len(master.columns)}")
        print(f"Output saved as        : {OUTPUT_FILE}")
        print("=" * 60)
    else:
        print("Error: No data was collected.")

print("\n Goshen Robert")

if __name__ == "__main__":
    main()
