# Unified Military Analytics

A data engineering and analytics pipeline that collects, cleans, and structures global military statistics from **Global Firepower** to create an analysis-ready dataset for interactive dashboards and military intelligence visualization.

---

## Overview

Unified Military Analytics is designed to automate the collection and preprocessing of global military data. The project extracts military, economic, infrastructure, manpower, and geographical indicators from multiple Global Firepower pages, transforms the raw data into a standardized dataset, and prepares it for visualization and analytical applications.

The project follows a modular data engineering and analytics pipeline consisting of data collection, preprocessing, feature engineering, dashboard planning, and interactive visualization using Tableau.

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
Module 3
KPI Feature Engineering
        │
        ▼
Tableau Ready Dataset
        │
        ▼
Module 4
Dashboard Planning & Prototyping
        │
        ▼
Tableau Dashboard Development
        │
        ▼
Military Analytics
```

---

# Project Structure

```text
Unified-Military-Analytics/
│
├── military_raw_data.csv
├── military_cleaned.csv
├── military_final.xlsx
├── military_long.xlsx
│
├── scrape_military_metrics.ipynb
├── clean_data.ipynb
├── generate_kpis.py
│
├── Storyboard for dashboard layouts.pdf
├── dashboard application prototype with link.pdf
│
├── README.md
└── requirements.txt
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

# Technologies

* Python
* Pandas
* BeautifulSoup
* Requests
* Regular Expressions
* Jupyter Notebook

---

# Module 3: KPI Feature Engineering & Tableau Preparation

## Objective

Enhance the cleaned military dataset by integrating economic and regional metadata and generating analytical KPIs required for military comparison, ranking analysis, and Tableau dashboard development.

---

## Features

* Integration of GDP and country metadata datasets
* Country-wise economic enrichment
* Feature engineering for military analytics
* Generation of derived performance indicators
* Tableau-ready dataset preparation
* Export of final analytical dataset

---

## Data Enrichment

The cleaned military dataset is enriched with:

### Economic Indicators

* GDP (USD)
* GDP Rank
* Defense Budget to GDP Ratio

### Regional Metadata

* Region
* Income Group
* Continent Classification

### Alliance Information

* NATO Membership Flag

---

## Engineered KPIs

### Power Index Rank Gap

Measures the difference between economic ranking and military ranking.

Formula:

```
Power Index Rank Gap = GDP Rank - Global Firepower Rank
```

---

### Assets per Capita

Measures military asset availability relative to population size.

Formula:

```
Assets per Capita = Total Military Assets / Total Population
```

---

### Budget-to-GDP Ratio

Measures defense spending intensity relative to national GDP.

Formula:

```
Budget-to-GDP Ratio = (Defense Budget / GDP) × 100
```

---

## Output Files

```
military_final.xlsx
```

Contains:

* Original military indicators
* Economic indicators
* Regional metadata
* Engineered KPIs
* NATO classification

---

## Technologies Used

* Python
* Pandas
* Excel
* Data Engineering
* Feature Engineering

---

# Module 4: Dashboard Planning & Prototyping

## Objective

Design the complete analytical dashboard architecture before implementation by creating storyboard layouts, navigation flow, user interactions, and a high-fidelity dashboard prototype for military intelligence visualization.

---

## Features

* Dashboard storyboard planning
* High-fidelity UI prototype
* Navigation flow design
* KPI mapping
* Interactive filter planning
* Tableau-ready dashboard layout

---

## Dashboard Modules

### Cover Dashboard

* Project introduction
* Dashboard navigation
* Military analytics overview

---

### Quick Stats

* Total Countries
* Average GDP
* Defense Budget
* Average Power Index
* Top Military Powers
* Assets per Capita
* NATO Distribution

---

### Nation Overview

* Country Profile
* Military Assets
* GDP
* Population
* Defense Budget
* Capability Radar
* Personnel Analysis

---

### Compare Powers

* Country A vs Country B
* KPI Comparison
* Radar Chart
* Military Asset Comparison
* Difference Summary

---

### Coalition Builder

* Multi-country Selection
* Coalition Statistics
* Combined Defense Budget
* Combined Personnel
* Coalition vs Reference Country
* Strategic Insights

---

### Navigation Flow

Designed navigation between all dashboard pages including:

* Home
* Quick Stats
* Nation Overview
* Compare Powers
* Coalition Builder

---

## Deliverables

* Dashboard Storyboard
* Dashboard Prototype
* Navigation Flow Design

---

## Output Files

```
Storyboard for dashboard layouts.pdf

dashboard application prototype with link.pdf
```

---

## Technologies Used

* Figma
* Tableau
* UI/UX Design
* Dashboard Planning

---

# Dataset Pipeline

```text
Web Scraping
      │
      ▼
Raw Dataset
      │
      ▼
Data Cleaning
      │
      ▼
Feature Engineering
      │
      ▼
Tableau Ready Dataset
      │
      ▼
Dashboard Planning
      │
      ▼
Interactive Dashboard
```

---

# Deliverables

## Module 1

* Web Scraper
* Raw Military Dataset

## Module 2

* Data Cleaning Notebook
* Clean Military Dataset

## Module 3

* KPI Generation Script
* Tableau-ready Dataset
* Feature Engineered Dataset

## Module 4

* Dashboard Storyboard
* Dashboard Prototype
* Navigation Flow

---

# Future Modules

* Interactive Tableau Dashboard
* Drill-down Analytics
* Time-series Military Trends
* Predictive Military Intelligence
* Machine Learning Models
* REST API Integration
* Web Deployment

---

# Dashboard Preview

## Module 4 Prototype

Dashboard storyboard and prototype created during Module 4.

### Cover Page

<img width="1452" height="913" alt="Screenshot 2026-07-23 234525 webp" src="https://github.com/user-attachments/assets/7e1b3f9e-e95a-4da7-a0e0-f04563b86e71" />

### Quick Stats

<img width="1447" height="796" alt="Screenshot 2026-07-23 234558" src="https://github.com/user-attachments/assets/c775b99a-1197-4b5b-b856-ec8138a536a7" />

### Nation Overview

<img width="1455" height="836" alt="Screenshot 2026-07-23 234614" src="https://github.com/user-attachments/assets/60e949b9-dffe-4cfa-b6df-ba1d2e5c313e" />

### Compare Powers

<img width="1455" height="842" alt="Screenshot 2026-07-23 234630" src="https://github.com/user-attachments/assets/7a75d0b5-6a0c-44f3-8f33-f150ed4e1029" />

### Coalition Builder

<img width="1456" height="817" alt="Screenshot 2026-07-23 234647" src="https://github.com/user-attachments/assets/5e61f529-f7ab-4447-a021-67ceda8eca1f" />

### Navigation Flow

<img width="1456" height="837" alt="Screenshot 2026-07-23 234703" src="https://github.com/user-attachments/assets/312caa28-74f2-4f27-b9b4-3ea9401906ce" />

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
