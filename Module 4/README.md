# Infosys Military Analysis

This repository contains an end-to-end data pipeline and visualization dashboard for analyzing global military capabilities. The project is split into distinct modules, taking raw data from the web all the way to a fully interactive, serverless analytical dashboard.

## Project Structure

The project is divided into sequential modules:

### [Module 1: Data Scraping](Module%201/README.md)
Contains a Python web scraper (`scrape_military_metrics.py`) that uses `BeautifulSoup` to extract over 50 military and economic indicators across 140+ countries from GlobalFirepower. The output is a raw dataset (`military_raw_data.csv`).

### [Module 2: Data Cleaning](Module%202/README.md)
Contains a Jupyter Notebook (`clean_data.ipynb`) demonstrating the data wrangling process using `pandas`. This step cleans up currencies, string artifacts, handles missing values, and normalizes column headers to output a pristine dataset (`military_cleaned.csv`).

### [Module 3: KPI Generation](Module%203/README.md)
Contains a Python script (`generate_kpis.py`) that enriches the dataset by computing new Key Performance Indicators (KPIs) such as Budget-to-GDP Ratio and Assets per Capita. The final dataset is exported to an Excel file (`military_final.xlsx`) optimized for BI tools like Tableau.

### [Module 4: Dashboard Prototype](Module%204/README.md)
Contains a completely static, blazing fast, serverless web application prototype. Built with Vanilla HTML, CSS, JavaScript, and Plotly.js, it provides an interactive, neon-themed dashboard for exploring the finalized military data.

## Module 4 Features
- **Professional Neon Dark Theme**: Custom CSS injection (`style.css`) mimicking a modern, elegant aesthetic with neon borders, glowing text, and shadows.
- **Quick Stats (Global View)**: Shows global KPIs and high-level interactive Plotly charts. Includes filters for Continent and Region.
- **Nation Overview**: Detailed drill-down into specific countries with a searchable dropdown and radar charts.
- **Interactive Collapsible Sidebar**: Allows for seamless navigation and a full-screen dashboard experience.
- **Plotly.js Integration**: Interactive, vibrant glowing charts rendered entirely client-side.

## How to Run the Dashboard

The dashboard in Module 4 is completely static and serverless. You do not need Python or any backend frameworks to run it.

1. Navigate to the `Module 4` directory:
   ```bash
   cd "C:\Users\ADMIN\Desktop\Infosys Military Analysis\Module 4"
   ```
2. Open `index.html` in any modern web browser.
3. Alternatively, for the best local experience, start a local HTTP server:
   ```bash
   python -m http.server 8000
   ```
   Then navigate to `http://localhost:8000` in your browser.

## Deployment
This folder can be dragged and dropped directly into static hosting services like **Netlify**, **Vercel**, or **GitHub Pages** without any further configuration.

The hosted app in Netlify to be opened in pc: "https://infosys-military-analysis-1.netlify.app/"

## Requirements (For Python Scripts)

To run the Python scripts in Modules 1, 2, and 3, you will need Python 3 installed. Install the dependencies using the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

*(Note: Module 4 requires zero dependencies).*

## Files in Module 4
- `index.html`: Main structural layout.
- `style.css`: Custom neon dark theme styling.
- `script.js`: Data fetching, logic, toggling, and Plotly.js chart rendering.
- `military_data.json`: Static dataset powering the dashboard.
- `storyboard.md`: The storyboard containing layout sketches and logic.
