# Unified Military Analytics and Comparison Dashboard

## Module 1 – Web Scraping and Data Collection

### Project Overview

This project is part of the **Unified Military Analytics and Comparison Dashboard**, which aims to collect, process, and visualize military and economic data for more than **140 countries**.

The first module focuses on building an automated web scraping pipeline using Python to extract military statistics from GlobalFirepower.com. The scraped data serves as the foundation for subsequent modules involving data cleaning, KPI engineering, and dashboard development. :contentReference[oaicite:1]{index=1}

---

## Objectives

- Scrape military data for 140+ countries.
- Extract 50+ military and economic metrics.
- Store the scraped data in a structured CSV file.
- Prepare the dataset for further cleaning and dashboard development.

---

## Technologies Used

- Python 3.x
- Requests
- BeautifulSoup (bs4)
- Pandas
- NumPy
- Jupyter Notebook

---

## Project Structure

```
Unified-Military-Analytics/
│
├── Military_Data_Scraper_Nagashree.ipynb
├── military_raw_data.csv
├── README.md
```

---

## Dataset Information

The scraper collects information such as:

- Power Index
- Total Population
- Military Manpower
- Active Personnel
- Reserve Personnel
- Air Force Strength
- Naval Strength
- Ground Assets
- Defense Budget
- GDP (merged)
- Region (merged)
- Continent (merged)
- Alliance Information (merged)

The final raw dataset contains data for **145 countries**.

---

## Features

- Automated scraping from GlobalFirepower.
- Supports scraping of more than 50 military indicators.
- Handles missing pages gracefully.
- Merges external lookup data (Region, Continent, GDP, Alliance).
- Exports results into a structured CSV file.

---

## Output

Generated file:

```
military_raw_data.csv
```

---

## Results

- Countries Scraped: **145**
- Metrics Collected: **56**
- Lookup Columns Added:
  - Continent
  - Region
  - GDP
  - Alliance

---

## Future Work

The remaining modules of the project include:

- Data Cleaning and Structuring
- KPI Feature Engineering
- Tableau Dashboard Development
- Dashboard Integration
- Testing and Documentation

---

## Author

**Nagashree K S**

Computer Science and Engineering Student

GitHub: https://github.com/Nagashreemurthy21

---

## Acknowledgements

- GlobalFirepower.com (Data Source)
- Infosys Springboard Internship
- Unified Military Analytics Project
