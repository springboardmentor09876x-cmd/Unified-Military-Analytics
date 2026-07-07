import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.globalfirepower.com/aircraft-total.php"

response = requests.get(url)

print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

rows = soup.find_all("div", class_="topRow")

print("Total Rows:", len(rows))

country_names = []
aircraft_counts = []

for row in rows:

    country = row.find("div", class_="longFormName").get_text(strip=True)

    aircraft = row.find("div", class_="valueContainer").get_text(strip=True)

    country_names.append(country)

    aircraft_counts.append(aircraft)
    
    df = pd.DataFrame({
    "Country Name": country_names,
    "Total Aircraft": aircraft_counts
})

print(df)


df.to_csv("aircraft_data.csv", index=False)

print("Files created successfully!")



print(country)