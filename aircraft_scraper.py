import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.globalfirepower.com/aircraft-total.php"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

records = soup.find_all("div", class_="recordsetContainer")

data = []

for record in records:
    country = record.find("div", class_="longFormName").text.strip()
    aircraft = record.find("div", class_="valueContainer").text.strip()

    data.append([country, aircraft])

print(data[:5])
df = pd.DataFrame(data, columns=["Country", "Aircraft Count"])
print(df)
df.to_csv("aircraft_data.csv", index=False)

print("CSV created successfully!")
