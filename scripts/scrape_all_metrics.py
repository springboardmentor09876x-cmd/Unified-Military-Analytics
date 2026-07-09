"""
scrape_all_metrics.py
----------------------
Unified Military Analytics and Comparison Dashboard
Module 1: Scraping Setup

This script scrapes country-level military and economic metrics from
GlobalFirepower.com and merges them into a single dataset:
    data/military_raw_data.csv

Design principle:
    Every metric this scraper knows about is listed ONE TIME in the
    URL_MAP dictionary below. To add a new metric later, add ONE new
    line here — no other code needs to change.

Author: Sahana
"""

import os
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------

# The "base" page is special: it lists ALL countries plus their overall
# Power Index rank and score. Every other page only gives ONE metric per
# country, keyed by country name, which we merge onto this base list.
BASE_URL = "https://www.globalfirepower.com/countries-listing.php"

# URL_MAP: every additional metric page we scrape.
#   key   -> the final, clean column name that will appear in the CSV
#   value -> the GlobalFirepower URL that provides that column
#
# THIS IS THE ONLY PLACE YOU EDIT TO ADD A NEW METRIC LATER.
URL_MAP = {
    "total_population": "https://www.globalfirepower.com/total-population-by-country.php",
    "total_military_manpower": "https://www.globalfirepower.com/available-military-manpower.php",
    "fit_for_service": "https://www.globalfirepower.com/manpower-fit-for-military-service.php",
    "population_reaching_military_age_annually": "https://www.globalfirepower.com/manpower-reaching-military-age-annually.php",
    "active_personnel": "https://www.globalfirepower.com/active-military-manpower.php",
    "reserve_personnel": "https://www.globalfirepower.com/active-reserve-military-manpower.php",
    "paramilitary": "https://www.globalfirepower.com/manpower-paramilitary.php",

    "total_military_aircraft": "https://www.globalfirepower.com/aircraft-total.php",
    "fighter_aircraft": "https://www.globalfirepower.com/aircraft-total-fighters.php",
    "attack_aircraft": "https://www.globalfirepower.com/aircraft-total-attack-types.php",
    "transport_aircraft": "https://www.globalfirepower.com/aircraft-total-transports.php",
    "trainer_aircraft": "https://www.globalfirepower.com/aircraft-total-trainers.php",
    "special_mission_aircraft": "https://www.globalfirepower.com/aircraft-total-special-mission.php",
    "tanker_aircraft": "https://www.globalfirepower.com/aircraft-total-tanker-fleet.php",
    "total_military_helicopters": "https://www.globalfirepower.com/aircraft-helicopters-total.php",
    "attack_helicopters": "https://www.globalfirepower.com/aircraft-helicopters-attack.php",

    "tanks": "https://www.globalfirepower.com/armor-tanks-total.php",
    "armored_fighting_vehicles": "https://www.globalfirepower.com/armor-apc-total.php",
    "self_propelled_artillery": "https://www.globalfirepower.com/armor-self-propelled-guns-total.php",
    "towed_artillery": "https://www.globalfirepower.com/armor-towed-artillery-total.php",
    "rocket_projectors": "https://www.globalfirepower.com/armor-mlrs-total.php",

    "total_naval_fleet": "https://www.globalfirepower.com/navy-ships.php",
    "total_naval_fleet_tonnage_mt": "https://www.globalfirepower.com/navy-force-by-tonnage.php",
    "aircraft_carriers": "https://www.globalfirepower.com/navy-aircraft-carriers.php",
    "helicopter_carriers": "https://www.globalfirepower.com/navy-helo-carriers.php",
    "submarines": "https://www.globalfirepower.com/navy-submarines.php",
    "destroyers": "https://www.globalfirepower.com/navy-destroyers.php",
    "frigates": "https://www.globalfirepower.com/navy-frigates.php",
    "corvettes": "https://www.globalfirepower.com/navy-corvettes.php",
    "coastal_patrol_craft": "https://www.globalfirepower.com/navy-patrol-coastal-craft.php",
    "mine_warfare_craft": "https://www.globalfirepower.com/navy-mine-warfare-craft.php",

    "defense_budget_usd": "https://www.globalfirepower.com/defense-spending-budget.php",
    "external_debt_usd": "https://www.globalfirepower.com/external-debt-by-country.php",
    "purchasing_power_parity_usd": "https://www.globalfirepower.com/purchasing-power-parity.php",
    "foreign_exchange_and_gold_reserves_usd": "https://www.globalfirepower.com/reserves-of-foreign-exchange-and-gold.php",

    "total_serviceable_airports": "https://www.globalfirepower.com/major-serviceable-airports-by-country.php",
    "labour_force": "https://www.globalfirepower.com/labor-force-by-country.php",
    "major_ports_and_terminals": "https://www.globalfirepower.com/major-ports-and-terminals.php",
    "total_merchant_marine_fleet": "https://www.globalfirepower.com/merchant-marine-strength-by-country.php",
    "railway_coverage_km": "https://www.globalfirepower.com/railway-coverage.php",
    "roadway_coverage_km": "https://www.globalfirepower.com/roadway-coverage.php",
    "waterway_coverage_km": "https://www.globalfirepower.com/waterway-coverage.php",

    "oil_production_bbl": "https://www.globalfirepower.com/oil-production-by-country.php",
    "oil_consumption_bbl": "https://www.globalfirepower.com/oil-consumption-by-country.php",
    "proven_oil_reserves_bbl": "https://www.globalfirepower.com/proven-oil-reserves-by-country.php",
    "natural_gas_production_cum": "https://www.globalfirepower.com/natural-gas-production-by-country.php",
    "natural_gas_consumption_cum": "https://www.globalfirepower.com/natural-gas-consumption-by-country.php",
    "proven_natural_gas_reserves_cum": "https://www.globalfirepower.com/proven-natural-gas-reserves-by-country.php",
    "coal_production_cum": "https://www.globalfirepower.com/coal-production-by-country.php",
    "coal_consumption_mt": "https://www.globalfirepower.com/coal-consumption-by-country.php",
    "proven_coal_reserves_cum": "https://www.globalfirepower.com/proven-coal-reserves-by-country.php",

    "total_land_area_sq_km": "https://www.globalfirepower.com/square-land-area.php",
    "coastline_coverage_km": "https://www.globalfirepower.com/coastline-coverage.php",
    "border_coverage_km": "https://www.globalfirepower.com/border-coverage.php",
}

# Folders (relative to project root, NOT relative to scripts/)
DATA_DIR = "data"
HTML_DIR = "html"
OUTPUT_CSV = os.path.join(DATA_DIR, "military_raw_data.csv")

# Be a polite scraper: identify yourself, and pause between requests.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Educational Project; Military Analytics Dashboard)"
}
REQUEST_DELAY_SECONDS = 1.5

# ---------------------------------------------------------------------------
# STEP 2: SCRAPE THE BASE URL (country list + rank + score)
# ---------------------------------------------------------------------------

def fetch_page(url):
    """
    Download one page and return a BeautifulSoup object.
    Every scraping function in this project calls this ONE function,
    so if GlobalFirepower ever needs special headers or retry logic,
    we only fix it in one place.
    """
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()  # crashes loudly if the page didn't load (e.g. 404, 500)
    return BeautifulSoup(response.text, "html.parser")


def save_html_for_debugging(soup, filename):
    """
    Saves the raw HTML to the html/ folder so we can open it in a browser
    later and manually check what the scraper actually saw, if something
    looks wrong in the final CSV.
    """
    os.makedirs(HTML_DIR, exist_ok=True)
    filepath = os.path.join(HTML_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(str(soup))


def scrape_base_rankings():
    """
    Scrapes the base URL (countries-listing.php).
    This page lists ALL countries at once, each with:
        - power_index_rank
        - country name
        - power_index_score

    Every other metric we scrape later gets merged onto this table,
    using 'country' as the join key. So this function must run first.

    Returns:
        pandas.DataFrame with columns: country, power_index_rank, power_index_score
    """
    print("Scraping base rankings page...")
    soup = fetch_page(BASE_URL)
    save_html_for_debugging(soup, "countries-listing.php.html")

    # Every country on this page is a link pointing to its detail page.
    # We find ALL such links, then parse the visible text of each one.
    country_links = soup.find_all("a", href=lambda h: h and "country-military-strength-detail.php" in h)

    # Text inside each link always follows this pattern:
    #   "<rank> <country name> <3-4 letter code> <trend words> PwrIndx: <score>"
    # Example: "1 United States USA Stable rrow graphic PwrIndx: 0.0741"
    pattern = re.compile(r'^(\d+)\s+(.+?)\s+([A-Z]{2,4})\s+.*?PwrIndx:\s*([\d.]+)')

    records = []
    for link in country_links:
        text = link.get_text(separator=" ", strip=True)
        match = pattern.match(text)
        if match:
            rank, country, _code, score = match.groups()
            records.append({
                "country": country.strip(),
                "power_index_rank": int(rank),
                "power_index_score": float(score),
            })

    df = pd.DataFrame(records)

    # Some countries can legitimately appear twice on the page (e.g. flag
    # grid at the bottom links to the same detail page). Keep the first
    # occurrence only, since that's the one with rank + score attached.
    df = df.drop_duplicates(subset="country", keep="first").reset_index(drop=True)

    print(f"Base rankings scraped: {len(df)} countries found.")
    return df

    # ---------------------------------------------------------------------------
# STEP 3: GENERIC SINGLE-METRIC SCRAPER
# ---------------------------------------------------------------------------

# Matches lines like: "1 China CHN 1,415,043,270" or "88 United Arab Emirates UAE 10,032,213"
# Groups: (rank) (country name) (3-4 letter code) (numeric value, possibly with commas/decimals)
# Matches lines like:
#   "1 China CHN 1,415,043,270"                (plain number, no unit)
#   "1 United States USA $ 831,500,000,000"    (currency symbol before number)
#   "1 United States USA 293,564 km"           (unit label AFTER the number)
#   "1 Russia RUS 17,098,242 km2"              (unit label with a digit in it)
# Groups: (rank) (country name) (3-4 letter code) (numeric value)
# [\$€£]?         -> optional currency symbol BEFORE the number
# \s*.*$          -> allow ANY trailing text (a unit label like "km", "bbl/day",
#                    "metric tons", or nothing at all) AFTER the number.
#                    This is what fixes railway/roadway/waterway/oil/gas/coal/
#                    land-area/coastline/border pages, which all end in a unit.
METRIC_LINE_PATTERN = re.compile(r'^(\d+)\s+(.+?)\s+([A-Z]{2,4})\s+[\$€£]?\s*([\d,]+\.?\d*)\s*.*$')

def clean_numeric_value(raw_value):
    """
    Converts a raw scraped string like '1,415,043,270' or '10,032,213.5'
    into a proper Python float, by stripping commas.
    Returns None if the value can't be converted (so bad data becomes a
    clean missing value instead of crashing the whole scraper).
    """
    try:
        return float(raw_value.replace(",", ""))
    except (ValueError, AttributeError):
        return None


def scrape_single_metric(column_name, url):
    """
    Generic scraper for ANY single-metric GlobalFirepower page.
    ...
    """
    print(f"Scraping '{column_name}' from {url} ...")
    soup = fetch_page(url)
    save_html_for_debugging(soup, f"{column_name}.html")

    country_links = soup.find_all("a", href=lambda h: h and "country-military-strength-detail.php" in h)

    records = []
    for link in country_links:
        text = link.get_text(separator=" ", strip=True)
        match = METRIC_LINE_PATTERN.match(text)
        if match:
            _rank, country, _code, raw_value = match.groups()
            records.append({
                "country": country.strip(),
                column_name: clean_numeric_value(raw_value),
            })

    # SAFETY NET: if nothing matched (e.g. an unexpected page format we
    # haven't handled yet), don't let this silently corrupt the merge.
    # Return an empty-but-correctly-shaped DataFrame instead, so the
    # merge in build_full_dataset() still works -- the column will just
    # be all NaN for this metric, and we'll get a clear warning to
    # investigate the saved HTML file.
    if not records:
        print(f"  WARNING: 0 records matched for '{column_name}'. "
              f"Check html/{column_name}.html to see why the pattern didn't match.")
        return pd.DataFrame(columns=["country", column_name])

    df = pd.DataFrame(records)
    df = df.drop_duplicates(subset="country", keep="first").reset_index(drop=True)

    print(f"  -> '{column_name}' scraped for {len(df)} countries.")
    time.sleep(REQUEST_DELAY_SECONDS)

    return df

# ---------------------------------------------------------------------------
# STEP 4: MERGE ALL METRICS INTO ONE DATASET
# ---------------------------------------------------------------------------

def build_full_dataset():
    """
    Runs the full scraping pipeline:
        1. Scrape the base rankings page (country, rank, score).
        2. Loop through every entry in URL_MAP, scraping one metric at a time.
        3. Merge each metric onto the base table using 'country' as the key.

    Because this loops over URL_MAP instead of calling 54 separate hardcoded
    functions, adding a new metric later means adding ONE line to URL_MAP --
    this function never needs to change.

    Returns:
        pandas.DataFrame: one row per country, one column per metric.
    """
    # Start with the base table: country, power_index_rank, power_index_score
    final_df = scrape_base_rankings()

    total_metrics = len(URL_MAP)
    for index, (column_name, url) in enumerate(URL_MAP.items(), start=1):
        print(f"[{index}/{total_metrics}] ", end="")
        metric_df = scrape_single_metric(column_name, url)

        # LEFT merge: always keep every country from the base table, even if
        # this particular metric page is missing some countries. Missing
        # values become NaN instead of dropping rows.
        final_df = final_df.merge(metric_df, on="country", how="left")

    return final_df


def save_dataset(df, output_path):
    """
    Saves the final merged dataset to CSV.
    Creates the data/ folder first if it doesn't exist yet.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\nSaved final dataset -> {output_path}")
    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")    

if __name__ == "__main__":
    print("Step 4: Running full scrape across all 54 metrics + base rankings...\n")
    full_df = build_full_dataset()

    print("\nPreview of final merged dataset:")
    print(full_df.head(10))

    save_dataset(full_df, OUTPUT_CSV)