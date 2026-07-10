aircraft_urls = {
    "https://www.globalfirepower.com/aircraft-total.php": "total_aircraft",
    "https://www.globalfirepower.com/aircraft-total-fighters.php": "fighter_aircraft",
    "https://www.globalfirepower.com/aircraft-total-attack.php": "attack_aircraft",
    "https://www.globalfirepower.com/aircraft-total-transport.php": "transport_aircraft",
    "https://www.globalfirepower.com/aircraft-total-trainer.php": "trainer_aircraft",
    "https://www.globalfirepower.com/aircraft-total-special-mission.php": "special_mission_aircraft",
    "https://www.globalfirepower.com/aircraft-total-tanker.php": "tanker_aircraft",
    "https://www.globalfirepower.com/aircraft-total-helicopters.php": "helicopters",
    "https://www.globalfirepower.com/aircraft-total-attack-helicopters.php": "attack_helicopters"
}
import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0"
}

session = requests.Session()

all_data = {}

for url, column in aircraft_urls.items():

    print(f"Scraping {column}")

    response = session.get(url, headers=headers, timeout=20)

    if response.status_code != 200:
        print(f"Could not open {url}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    cards = soup.find_all(
        "div",
        class_="picTrans recordsetContainer boxShadow zoom"
    )

    for card in cards:

        country = card.find(
            "div",
            class_="longFormName"
        ).get_text(strip=True)

        value = card.find(
            "div",
            class_="valueContainer"
        ).find_all("span")[-1].get_text(strip=True)

        if country not in all_data:
            all_data[country] = {}

        all_data[country][column] = value

df = pd.DataFrame.from_dict(all_data, orient="index")

df.index.name = "Country"

df.reset_index(inplace=True)

df.to_csv(
    "aircraft_data.csv",
    index=False,
    encoding="utf-8-sig"
)

print(df.head())
print(df.shape)