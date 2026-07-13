# Unified-Militar# Unified Military Analytics

A data engineering and analytics pipeline that collects, cleans, and structures global military statistics from **Global Firepower** to create an analysis-ready dataset for interactive dashboards and military intelligence visualization.

---

## Overview

Unified Military Analytics is designed to automate the collection and preprocessing of global military data. The project extracts military, economic, infrastructure, manpower, and geographical indicators from multiple Global Firepower pages, transforms the raw data into a standardized dataset, and prepares it for visualization and analytical applications.

The project is divided into multiple modules, with the first two modules focusing on data acquisition and preprocessing.

---

## Project Objectives

* Automate military data collection from multiple Global Firepower sources.
* Consolidate country-wise metrics into a single dataset.
* Clean and standardize raw data.
* Produce an analysis-ready dataset for Tableau dashboards.
* Build a scalable data pipeline for future analytics and machine learning applications.

---

# Project Architecture

```text
Global Firepower
        │
        ▼
Module 1
Data Collection & Web Scraping
        │
        ▼
Raw Military Dataset
        │
        ▼
Module 2
Data Cleaning & Structuring
        │
        ▼
Clean Military Dataset
        │
        ▼
Tableau Dashboard
        │
        ▼
Military Analytics
```

---

# Project Structure

```text
## Project Structure

```text
Unified-Military-Analytics/
│
├── military_raw_data.csv          # Raw dataset generated after web scraping
├── military_cleaned.csv           # Cleaned dataset ready for analysis and Tableau
│
├── scrape_military_metrics.ipynb  # Module 1: Web scraping and raw data generation
├── clean_data.ipynb               # Module 2: Data cleaning and preprocessing
│
└── README.md                      # Project documentation
```

---

# Module 1: Data Collection & Web Scraping

## Objective

Collect country-wise military statistics from Global Firepower and consolidate all metrics into a unified raw dataset.

---

## Features

* Automated web scraping using Python
* Country-wise metric extraction
* Multi-page data collection
* Dataset merging using country names
* Progress logging during execution
* Raw CSV generation

---

## Data Collected

The scraper collects information related to:

### Military Strength

* Total Military Aircraft
* Fighter Aircraft
* Attack Aircraft
* Transport Aircraft
* Trainer Aircraft
* Tanker Aircraft
* Helicopters
* Tanks
* Armored Vehicles
* Artillery
* Rocket Projectors
* Naval Fleet
* Aircraft Carriers
* Destroyers
* Frigates
* Corvettes
* Submarines

### Manpower

* Total Population
* Military Manpower
* Active Personnel
* Reserve Personnel
* Paramilitary
* Military Age Population

### Economy

* Defense Budget
* Purchasing Power Parity
* External Debt
* Foreign Exchange Reserves

### Infrastructure

* Airports
* Ports
* Merchant Fleet
* Railway Network
* Road Network

### Natural Resources

* Oil Production
* Oil Consumption
* Oil Reserves
* Natural Gas
* Coal Production
* Coal Reserves

### Geography

* Land Area
* Coastline
* Border Length
* Waterways

---

## Technologies Used

* Python
* Requests
* BeautifulSoup
* Pandas

---

## Output

```
military_raw_data.csv
```

---

# Module 2: Data Cleaning & Structuring

## Objective

Transform the raw scraped dataset into a standardized and analysis-ready format suitable for visualization and further analytics.

---

## Data Cleaning Steps

### Standardize Column Names

* Convert column names to lowercase
* Replace spaces with underscores
* Maintain consistent naming conventions

---

### Clean Text Values

Remove:

* Commas
* Currency symbols
* Percentage symbols
* Units
* Special characters
* Extra descriptive text

---

### Convert Data Types

* Convert all military metrics into numeric values
* Automatically handle invalid values

---

### Handle Missing Values

* Replace missing numeric values
* Remove duplicate records
* Validate dataset consistency

---

### Export Dataset

Generate the cleaned dataset.

```
military_cleaned.csv
```

---

# Dataset Pipeline

```
Web Pages
      │
      ▼
Scraping
      │
      ▼
Raw Dataset
      │
      ▼
Cleaning
      │
      ▼
Structured Dataset
      │
      ▼
Visualization
```

---

# Technologies

* Python
* Pandas
* BeautifulSoup
* Requests
* Regular Expressions
* Jupyter Notebook

---

# Deliverables

## Module 1

* Web Scraper
* Raw Military Dataset

## Module 2

* Data Cleaning Notebook
* Clean Military Dataset

---

# Future Modules

* Tableau Dashboard Development
* Exploratory Data Analysis
* Military Strength Comparison
* Predictive Analytics
* Machine Learning Models
* Interactive Web Dashboard
* API Integration

---

# License

This project is developed for educational, research, and analytical purposes. All data belongs to its respective source and is used in accordance with publicly available information.

---

# Acknowledgements

* Global Firepower
* Python Open Source Community
* Pandas
* BeautifulSoup
* Requests
y-Analytics