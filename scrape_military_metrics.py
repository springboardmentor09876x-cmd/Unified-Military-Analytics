import os
import re
import sys
import time
import io
import requests
import pandas as pd
from bs4 import BeautifulSoup

http_headers = {"User-Agent": "Mozilla/5.0"}

#url=https://www.globalfirepower.com/aircraft-total.php
lookup_source_url = "https://drive.google.com/drive/home"

part1_checkpoint_file = "Part1.csv"       
output_file_name = "military_raw_data.csv"


def load_lookup_csv(source_url):
    """Reads a lookup CSV from a URL. Handles both plain links (GitHub raw, etc.)
    and Google Drive share links, including Drive's virus-scan interstitial page."""
    drive_id_match = re.search(r"drive\.google\.com.*?/d/([\w-]+)|id=([\w-]+)", source_url)
    if "drive.google.com" in source_url and drive_id_match:
        drive_file_id = drive_id_match.group(1) or drive_id_match.group(2)
        http_session = requests.Session()
        response = http_session.get(
            "https://drive.google.com/uc",
            params={"export": "download", "id": drive_file_id},
            headers=http_headers,
            stream=True,
        )
        # Large/flagged files return an HTML confirmation page instead of the file
        confirm_token = None
        for ck, cv in response.cookies.items():
            if ck.startswith("download_warning"):
                confirm_token = cv
        if confirm_token is None and response.text.lstrip().startswith("<"):
            confirm_match = re.search(r"confirm=([0-9A-Za-z_-]+)", response.text)
            if confirm_match:
                confirm_token = confirm_match.group(1)
        if confirm_token:
            response = http_session.get(
                "https://drive.google.com/uc",
                params={"export": "download", "id": drive_file_id, "confirm": confirm_token},
                headers=http_headers,
                stream=True,
            )
        return pd.read_csv(io.StringIO(response.content.decode("utf-8")))
    else:
        return pd.read_csv(source_url)


if lookup_source_url == "PASTE_YOUR_LINK_HERE":
    sys.exit("ERROR: Set lookup_source_url at the top of the script to your Part2.csv link.")

try:
    lookup_dataframe = load_lookup_csv(lookup_source_url)
except Exception as err:
    sys.exit(f"ERROR: Could not read lookup data from lookup_source_url.\n{err}")


print("=" * 60)
print("STEP 1: Scraping Power Index")
print("=" * 60)

gfp_listing_url = "https://www.globalfirepower.com/countries-listing.php"
html_page = requests.get(gfp_listing_url, headers=http_headers)
parsed_html = BeautifulSoup(html_page.text, "html.parser")

power_index_data = {}
for country_element in parsed_html.find_all("div", class_="longFormName"):
    country_name = country_element.get_text(strip=True)
    ancestor_row = country_element
    value_element = None
    for _ in range(6):
        ancestor_row = ancestor_row.parent
        if ancestor_row is None:
            break
        value_element = ancestor_row.find("div", class_="pwrIndxContainer")
        if value_element:
            break
    if value_element:
        raw_value = value_element.get_text(strip=True)
        power_index_data[country_name] = raw_value.replace("PwrIndx:", "").strip()
    else:
        print(f"Warning: no Power Index found for {country_name}")

power_index_df = pd.DataFrame({
    "Country": list(power_index_data.keys()),
    "Power Index": list(power_index_data.values())
})
print("Power Index Scrape:", "Success" if power_index_df.shape == (145, 2) and not power_index_df.isnull().values.any() else "Failure")

metric_sources = {
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


def scrape_metric_page(metric_url):
    html_page = requests.get(metric_url, headers=http_headers)
    if html_page.status_code != 200:
        print(f"Failed : {metric_url}")
        return None
    parsed_html = BeautifulSoup(html_page.text, "html.parser")
    metric_data = {}
    for country_element in parsed_html.find_all("div", class_="longFormName"):
        country_name = country_element.get_text(strip=True)
        ancestor_row = country_element
        value_element = None
        for _ in range(6):
            ancestor_row = ancestor_row.parent
            if ancestor_row is None:
                break
            value_element = ancestor_row.find("div", class_="valueContainer")
            if value_element:
                break
        if value_element:
            metric_data[country_name] = value_element.get_text(strip=True)
        else:
            print(f"Warning: no value found for {country_name} on {metric_url}")
    if len(metric_data) == 0:
        print(f"No data extracted : {metric_url}")
        return None
    return metric_data


print("\n" + "=" * 60)
print("STEP 2: Scraping remaining 54 metrics")
print("=" * 60)

combined_df = None
for idx, (metric_url, metric_column) in enumerate(metric_sources.items(), start=1):
    print(f"[{idx}/{len(metric_sources)}] Scraping {metric_column}")
    metric_data = scrape_metric_page(metric_url)
    if metric_data is None:
        continue
    if combined_df is None:
        combined_df = pd.DataFrame({"Country": list(metric_data.keys())})
    combined_df[metric_column] = combined_df["Country"].map(metric_data)
    time.sleep(1)


combined_df = power_index_df.merge(combined_df, on="Country", how="left")
combined_df.to_csv(part1_checkpoint_file, index=False)

print("\n" + "=" * 60)
print("STEP 1+2 COMPLETE — Part1.csv saved")
print("=" * 60)
print("Shape:", combined_df.shape)
print(combined_df.head())
print("\nRows with any missing values:\n", combined_df[combined_df.isnull().any(axis=1)][["Country"]])


print("\n" + "=" * 60)
print("STEP 3: Merging with lookup file")
print("=" * 60)

merged_master_df = combined_df.copy()
# lookup_dataframe was already fetched from lookup_source_url at the top of the script

lookup_columns_to_add = ["Continent", "Region", "GDP", "Alliance"]

if "Country" not in lookup_dataframe.columns:
    raise ValueError(f"The column 'Country' was not found in {LOOKUP_FILE}")

missing_lookup_columns = [col for col in lookup_columns_to_add if col not in lookup_dataframe.columns]
if missing_lookup_columns:
    raise ValueError(f"These required columns are missing from the lookup CSV: {missing_lookup_columns}")

merged_master_df["_country_match_key"] = merged_master_df["Country"].astype(str).str.strip().str.casefold()
lookup_dataframe["_country_match_key"] = lookup_dataframe["Country"].astype(str).str.strip().str.casefold()

duplicate_country_names = lookup_dataframe[lookup_dataframe["_country_match_key"].duplicated(keep=False)]["Country"].unique()
if len(duplicate_country_names) > 0:
    raise ValueError(
        "Duplicate countries found in lookup file after ignoring case differences "
        f"and extra spaces. Duplicate countries: {list(duplicate_country_names)}"
    )

lookup_columns_subset = lookup_dataframe[["_country_match_key"] + lookup_columns_to_add].copy()

final_result_df = merged_master_df.merge(
    lookup_columns_subset,
    on="_country_match_key",
    how="left",
    sort=False,
    validate="many_to_one"
)
final_result_df.drop(columns=["_country_match_key"], inplace=True)
final_result_df.to_csv(output_file_name, index=False, na_rep="")

matched_country_count = merged_master_df["_country_match_key"].isin(set(lookup_dataframe["_country_match_key"])).sum()
unmatched_country_count = len(merged_master_df) - matched_country_count

print("=" * 60)
print("PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 60)
print(f"\nOriginal rows          : {len(merged_master_df)}")
print(f"Final rows             : {len(final_result_df)}")
print(f"Original columns       : {len(merged_master_df.columns) - 1}")
print(f"Final columns          : {len(final_result_df.columns)}")
print(f"\nCountries matched      : {matched_country_count}")
print(f"Countries not matched  : {unmatched_country_count}")
print("\nColumns added:")
for col_name in lookup_columns_to_add:
    print(f"  - {col_name}")
print(f"\nOutput saved as: {output_file_name}")
print("=" * 60)

if os.path.exists(part1_checkpoint_file):
    os.remove(part1_checkpoint_file)
    print(f"\nCleanup: deleted temporary checkpoint '{part1_checkpoint_file}'")
