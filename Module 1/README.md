# Military Analytics Scraper

This project contains a Python script for scraping 140+ countries and their military capabilities across 50+ different indicators from globalfirepower.com.

## Files Provided
- `scrape_military_metrics.py`: Main scraping script that reads `links_for_military_data.txt`, fetches data from each provided URL, and generates a unified CSV file.
- `requirements.txt`: Python package dependencies.
- `links_for_military_data.txt`: Target URLs to scrape (dynamically parsed by the script).
- `military_raw_data.csv`: The finalized dataset containing all scraped metrics (generated upon execution).
- `debug_html/`: A directory containing raw HTML pages from the scraper (useful for debugging).

## Execution Instructions

1. Ensure Python 3 is installed.
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the scraper:
   ```bash
   python scrape_military_metrics.py
   ```
4. Check the `military_raw_data.csv` for the generated dataset.

## Dataset Structure
The dataset contains columns such as:
- `Country`
- `Power Index`
- `total_population`
- `tanks`
- `total_military_aircraft`
- `defense_budget_usd`
- And 50+ other metrics.
