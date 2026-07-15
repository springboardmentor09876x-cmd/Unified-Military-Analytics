import os
import re
import sys
import time
import io
import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}

# Paste your Part2 (Continent/Region/GDP/Alliance) link here.
# GitHub raw link  -> https://raw.githubusercontent.com/user/repo/main/Part2.csv
# Google Drive     -> any share link works, e.g. https://drive.google.com/file/d/FILE_ID/view?usp=sharing
LOOKUP_URL = "https://drive.google.com/file/d/1xlStXEGGaXIGkfJVgAPB5GgJs1ZYrxgA/view?usp=sharing"

PART1_FILE = "Part1.csv"       # temporary checkpoint, deleted at the end
OUTPUT_FILE = "military_raw_data.csv"


def fetch_lookup_csv(url):
    """Reads a lookup CSV from a URL. Handles both plain links (GitHub raw, etc.)
    and Google Drive share links, including Drive's virus-scan interstitial page."""
    drive_match = re.search(r"drive\.google\.com.*?/d/([\w-]+)|id=([\w-]+)", url)
    if "drive.google.com" in url and drive_match:
        file_id = drive_match.group(1) or drive_match.group(2)
        session = requests.Session()
        resp = session.get(
            "https://drive.google.com/uc",
            params={"export": "download", "id": file_id},
            headers=headers,
            stream=True,
        )
        # Large/flagged files return an HTML confirmation page instead of the file
        token = None
        for key, value in resp.cookies.items():
            if key.startswith("download_warning"):
                token = value
        if token is None and resp.text.lstrip().startswith("<"):
            match = re.search(r"confirm=([0-9A-Za-z_-]+)", resp.text)
            if match:
                token = match.group(1)
        if token:
            resp = session.get(
                "https://drive.google.com/uc",
                params={"export": "download", "id": file_id, "confirm": token},
                headers=headers,
                stream=True,
            )
        return pd.read_csv(io.StringIO(resp.content.decode("utf-8")))
    else:
        return pd.read_csv(url)


# ===================================================
# PRE-CHECK: lookup URL must be reachable before we bother scraping
# ===================================================
if LOOKUP_URL == "PASTE_YOUR_LINK_HERE":
    sys.exit("ERROR: Set LOOKUP_URL at the top of the script to your Part2.csv link.")

try:
    lookup_df = fetch_lookup_csv(LOOKUP_URL)
except Exception as e:
    sys.exit(f"ERROR: Could not read lookup data from LOOKUP_URL.\n{e}")

# ===================================================
# STEP 1: Power Index (Country, Power Index)
# ===================================================
print("=" * 60)
print("STEP 1: Scraping Power Index")
print("=" * 60)

url = "https://www.globalfirepower.com/countries-listing.php"
page = requests.get(url, headers=headers)
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
print("Power Index Scrape:", "Success" if df.shape == (145, 2) and not df.isnull().values.any() else "Failure")

# ===================================================
# STEP 2: All other 54 metrics
# ===================================================
sources = {
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


def scrape_page(url):
    page = requests.get(url, headers=headers)
    if page.status_code != 200:
        print(f"Failed : {url}")
        return None
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


print("\n" + "=" * 60)
print("STEP 2: Scraping remaining 54 metrics")
print("=" * 60)

master = None
for i, (src_url, column_name) in enumerate(sources.items(), start=1):
    print(f"[{i}/{len(sources)}] Scraping {column_name}")
    data = scrape_page(src_url)
    if data is None:
        continue
    if master is None:
        master = pd.DataFrame({"Country": list(data.keys())})
    master[column_name] = master["Country"].map(data)
    time.sleep(1)

# ===================================================
# STEP 3: Merge Power Index into Master, save Part1.csv
# ===================================================
master = df.merge(master, on="Country", how="left")
master.to_csv(PART1_FILE, index=False)

print("\n" + "=" * 60)
print("STEP 1+2 COMPLETE — Part1.csv saved")
print("=" * 60)
print("Shape:", master.shape)
print(master.head())
print("\nRows with any missing values:\n", master[master.isnull().any(axis=1)][["Country"]])

# ===================================================
# STEP 4: Merge Part1.csv with Part2.csv lookup -> military_raw_data.csv
# ===================================================
print("\n" + "=" * 60)
print("STEP 3: Merging with lookup file")
print("=" * 60)

master_df = master.copy()
# lookup_df was already fetched from LOOKUP_URL at the top of the script

columns_to_add = ["Continent", "Region", "GDP", "Alliance"]

if "Country" not in lookup_df.columns:
    raise ValueError(f"The column 'Country' was not found in {LOOKUP_FILE}")

missing_columns = [col for col in columns_to_add if col not in lookup_df.columns]
if missing_columns:
    raise ValueError(f"These required columns are missing from the lookup CSV: {missing_columns}")

master_df["_country_match_key"] = master_df["Country"].astype(str).str.strip().str.casefold()
lookup_df["_country_match_key"] = lookup_df["Country"].astype(str).str.strip().str.casefold()

duplicate_countries = lookup_df[lookup_df["_country_match_key"].duplicated(keep=False)]["Country"].unique()
if len(duplicate_countries) > 0:
    raise ValueError(
        "Duplicate countries found in lookup file after ignoring case differences "
        f"and extra spaces. Duplicate countries: {list(duplicate_countries)}"
    )

lookup_subset = lookup_df[["_country_match_key"] + columns_to_add].copy()

result_df = master_df.merge(
    lookup_subset,
    on="_country_match_key",
    how="left",
    sort=False,
    validate="many_to_one"
)
result_df.drop(columns=["_country_match_key"], inplace=True)
result_df.to_csv(OUTPUT_FILE, index=False, na_rep="")

matched_count = master_df["_country_match_key"].isin(set(lookup_df["_country_match_key"])).sum()
unmatched_count = len(master_df) - matched_count

print("=" * 60)
print("PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 60)
print(f"\nOriginal rows          : {len(master_df)}")
print(f"Final rows             : {len(result_df)}")
print(f"Original columns       : {len(master_df.columns) - 1}")
print(f"Final columns          : {len(result_df.columns)}")
print(f"\nCountries matched      : {matched_count}")
print(f"Countries not matched  : {unmatched_count}")
print("\nColumns added:")
for column in columns_to_add:
    print(f"  - {column}")
print(f"\nOutput saved as: {OUTPUT_FILE}")
print("=" * 60)

# ===================================================
# CLEANUP: only the script + final CSV should remain
# ===================================================
if os.path.exists(PART1_FILE):
    os.remove(PART1_FILE)
    print(f"\nCleanup: deleted temporary checkpoint '{PART1_FILE}'")

print("\nPipeline by Yaswanth — Done.")