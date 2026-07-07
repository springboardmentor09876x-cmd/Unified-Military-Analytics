import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

# Website URL
URL = "https://www.globalfirepower.com/aircraft-total.php"

# Request Headers
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# Fetch webpage
page = requests.get(URL, headers=HEADERS)

if page.status_code == 200:

    soup = BeautifulSoup(page.content, "html.parser")

    # Extract all visible text
    page_text = soup.get_text(separator="\n")

    # Regex Pattern
    regex = re.compile(
        r'(\d+)\s+([A-Za-z\s\'\-]+)\s+[A-Z]{3}\s+(\d{1,3}(?:,\d{3})*)'
    )

    records = []

    for match in regex.finditer(page_text):
        rank = int(match.group(1))
        country = match.group(2).strip()
        aircraft = int(match.group(3).replace(",", ""))

        records.append({
            "Rank": rank,
            "Country": country,
            "Aircraft_Count": aircraft
        })

    # Create DataFrame
    df = pd.DataFrame(records)

    # Display first rows
    print(df.head())

    # Save CSV
    output_file = "military_data_Sample.csv"
    df.to_csv(output_file, index=False)

    print(f"\nData saved successfully to {output_file}")

else:
    print(f"Request Failed! Status Code: {page.status_code}")