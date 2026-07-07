from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

driver = webdriver.Chrome()

driver.get("https://www.globalfirepower.com/aircraft-total.php")
time.sleep(5)

soup = BeautifulSoup(driver.page_source, "html.parser")

driver.quit()

records = soup.find_all("div", class_="recordsetContainer")

data = []

for record in records:

    country = record.find("div", class_="countryNameContainer")
    value = record.find("div", class_="valueContainer")

    if country and value:
        data.append({
            "Country": country.get_text(strip=True),
            "Total Aircraft": value.get_text(strip=True)
        })

df = pd.DataFrame(data)

print(df)

df.to_csv("aircraft_data.csv", index=False)

print("CSV saved successfully.")