# Unified Military Analytics

## Module 1 - Aircraft Data Scraper

### Objective
Scrape Military Aircraft Fleet Strength data from the Global Firepower website and store it in a CSV file.

### Website
https://www.globalfirepower.com/aircraft-total.php

### Technologies Used
- Python 3
- Requests
- BeautifulSoup (bs4)
- Pandas

### Project Structure

Unified-Military-Analytics/

├── README.md

├── data/

│   └── aircraft_total.csv

├── html/

│   └── aircraft_total.html

└── scripts/

    └── scrape_military_metrics.py

### Output Files
- `aircraft_total.html` - Saved HTML page for debugging.
- `aircraft_total.csv` - Extracted military aircraft data for 145 countries.

### Features
- Downloads webpage automatically.
- Saves HTML locally.
- Extracts Country Name.
- Extracts Military Aircraft count.
- Stores the data in a CSV file.
- Processes data for 145 countries.

### How to Run

Open Terminal and run:

```bash
python3 scripts/scrape_military_metrics.py
```

### Sample Output

```
Military Aircraft Fleet Strength by Country (2026)

HTML file saved successfully!

Total cards found: 145

CSV File Created Successfully!

Total Countries: 145
```

### Author

**Sahana N**

Branch: **sahana-module1**