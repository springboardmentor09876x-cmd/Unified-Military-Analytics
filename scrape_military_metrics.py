import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

def extract_number(text):
    numbers = re.findall(r'[\d,]+', text)

    if len(numbers) == 0:
        return ""

    return numbers[-1].replace(",", "")

headers = {"User-Agent": "Mozilla/5.0"}

with open("links_for_military_data.txt", "r") as f:
    urls = [line.strip() for line in f if line.strip()]

data = []

for url in urls:

    print("\n" + "=" * 50)
    print(url)

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    country = (
        soup.find("title")
        .text.replace("2026", "")
        .replace("Military Strength", "")
        .strip()
    )

    row = {"Country": country}

    blocks = soup.find_all("div", class_="specsGenContainers")

    for block in blocks:

        text = block.get_text(" ", strip=True)

        if "Total Population:" in text:
            row["total_population"] = extract_number(text)

        elif "Available Manpower" in text:
            row["available_manpower"] = extract_number(text)

        elif "Fit-for-Service" in text:
            row["fit_for_service"] = extract_number(text)

        elif "Reaching Mil Age Annually" in text:
            row["population_reaching_military_age_annually"] = extract_number(text)

        elif "Active Personnel" in text:
            row["active_personnel"] = extract_number(text)

        elif "Reserve Personnel" in text:
            row["reserve_personnel"] = extract_number(text)

        elif "Paramilitary" in text:
            row["paramilitary"] = extract_number(text)

        elif "Aircraft Total:" in text:
            row["total_military_aircraft"] = extract_number(text)

        elif "Fighters:" in text:
            row["fighter_aircraft"] = extract_number(text)

        elif "Attack Types:" in text:
            row["attack_aircraft"] = extract_number(text)

        elif "Transports (Fixed-Wing):" in text:
            row["transport_aircraft"] = extract_number(text)

        elif "Trainers:" in text:
            row["trainer_aircraft"] = extract_number(text)

        elif "Special-Mission:" in text:
            row["special_mission_aircraft"] = extract_number(text)

        elif "Tanker Fleet:" in text:
            row["tanker_aircraft"] = extract_number(text)

        elif "Helicopters:" in text:
            row["total_military_helicopters"] = extract_number(text)

        elif "Attack Helicopters:" in text:
            row["attack_helicopters"] = extract_number(text)

        elif "Tanks:" in text:
            row["tanks"] = extract_number(text)
        elif "Armored Vehicles:" in text:
            row["armored_fighting_vehicles"] = extract_number(text)

        elif "Self-Propelled Artillery:" in text:
            row["self_propelled_artillery"] = extract_number(text)

        elif "Towed Artillery:" in text:
            row["towed_artillery"] = extract_number(text)

        elif "Rocket Projectors:" in text:
            row["rocket_projectors"] = extract_number(text)

        elif "Naval Fleet:" in text:
            row["total_naval_fleet"] = extract_number(text)

        elif "Fleet Tonnage:" in text:
            row["total_naval_fleet_tonnage_mt"] = extract_number(text)

        elif "Aircraft Carriers:" in text:
            row["aircraft_carriers"] = extract_number(text)

        elif "Helicopter Carriers:" in text:
            row["helicopter_carriers"] = extract_number(text)

        elif "Submarines:" in text:
            row["submarines"] = extract_number(text)

        elif "Destroyers:" in text:
            row["destroyers"] = extract_number(text)

        elif "Frigates:" in text:
            row["frigates"] = extract_number(text)

        elif "Corvettes:" in text:
            row["corvettes"] = extract_number(text)

        elif "Patrol Vessels:" in text:
            row["coastal_patrol_craft"] = extract_number(text)

        elif "Mine Warfare:" in text:
            row["mine_warfare_craft"] = extract_number(text)
        elif "Defense Budget:" in text:
            row["defense_budget_usd"] = extract_number(text)

        elif "External Debt:" in text:
            row["external_debt_usd"] = extract_number(text)

        elif "Purchasing Power Parity:" in text:
            row["purchasing_power_parity_usd"] = extract_number(text)

        elif "Foreign Exchange/Gold:" in text:
            row["foreign_exchange_and_gold_reserves_usd"] = extract_number(text)
        elif "Square Land Area:" in text:
            row["total_land_area_sq_km"] = extract_number(text)

        elif "Coastline Coverage:" in text:
            row["coastline_coverage_km"] = extract_number(text)

        elif "Shared Borders:" in text:
            row["border_coverage_km"] = extract_number(text)

        elif "Waterways (usable):" in text:
            row["waterway_coverage_km"] = extract_number(text)
        elif "Labor Force:" in text:
            row["labour_force"] = extract_number(text)

        elif "Merchant Marine Fleet:" in text:
            row["total_merchant_marine_fleet"] = extract_number(text)

        elif "Ports / Trade Terminals:" in text:
            row["major_ports_and_terminals"] = extract_number(text)

        elif "Airports:" in text:
            row["total_serviceable_airports"] = extract_number(text)

        elif "Roadway Coverage:" in text:
            row["roadway_coverage_km"] = extract_number(text)

        elif "Railway Coverage:" in text:
            row["railway_coverage_km"] = extract_number(text)
        elif "Oil Production:" in text:
            row["oil_production_bbl"] = extract_number(text)

        elif "Oil Consumption:" in text:
            row["oil_consumption_bbl"] = extract_number(text)

        elif "Proven Oil Reserves:" in text:
            row["proven_oil_reserves_bbl"] = extract_number(text)

        elif "Natural Gas Production:" in text:
            row["natural_gas_production_cum"] = extract_number(text)

        elif "Natural Gas Consumption:" in text:
            row["natural_gas_consumption_cum"] = extract_number(text)

        elif "Proven Gas Reserves:" in text:
            row["proven_natural_gas_reserves_cum"] = extract_number(text)

        elif "Coal Production:" in text:
            row["coal_production_cum"] = extract_number(text)

        elif "Coal Consumption:" in text:
            row["coal_consumption_mt"] = extract_number(text)

        elif "Coal Reserves:" in text:
            row["proven_coal_reserves_cum"] = extract_number(text)
    data.append(row)

for key, value in row.items():
    print(f"{key}: {value}")
df = pd.DataFrame(data)
df.to_csv("military_raw_data.csv", index=False)

print("Saved", len(df), "countries")