# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Website URL
url = "https://www.globalfirepower.com/aircraft-total.php"

# Download webpage
response = requests.get(url)

# Convert webpage into BeautifulSoup object
soup = BeautifulSoup(response.text, "html.parser")

# Print page title
print(soup.title.text)

# Save webpage HTML for debugging
with open("html/aircraft_total.html", "w", encoding="utf-8") as file:
    file.write(response.text)

print("HTML file saved successfully!")
# Find all country cards
cards = soup.find_all("div", class_="picTrans recordsetContainer boxShadow zoom")

print("Total cards found:", len(cards))

# Create an empty list
countries_data = []

# Loop through each country card
for card in cards:

    # Find country name
    country = card.find("div", class_="longFormName")

    if country:
        country = country.get_text(strip=True)
    else:
        country = "N/A"

    # Find aircraft count
    value = card.find("div", class_="valueContainer")

    if value:
        aircraft = value.get_text(strip=True)
    else:
        aircraft = "N/A"

    # Store data
    countries_data.append({
        "Country": country,
        "Military Aircraft": aircraft
    })

    # Convert to DataFrame
df = pd.DataFrame(countries_data)

print(df.head())

# Save CSV
df.to_csv("data/aircraft_total.csv", index=False)

print("CSV File Created Successfully!")
print("Total Countries:", len(df))