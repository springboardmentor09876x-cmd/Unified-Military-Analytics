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
        Module 1: Data Collection & Web Scraping
                           │
                           ▼
                  Raw Military Dataset
                           │
                           ▼
        Module 2: Data Cleaning & Structuring
                           │
                           ▼
                 Clean Military Dataset
                           │
                           ▼
      Module 3: KPI Feature Engineering
                           │
                           ▼
             Tableau-Ready Analytical Dataset
                           │
                           ▼
      Module 4: Dashboard Planning & Prototyping
                           │
                           ▼
     Module 5: Quick Stats & Nation Overview
                           │
                           ▼
    Module 6: Compare Powers & Coalition Builder
                           │
                           ▼
         Module 7: Testing & Debugging (QA)
                           │
                           ▼
         Interactive Military Analytics Platform
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
├── Quick Stats.twbx
├── Nation Overview.twbx
├── Compare Powers.twbx
├── Coalition Builder.twbx
├── global_military_firepower_2025.twbx
│
├── QA_Checklist.md
├── README.md
├── requirements.txt
└── LICENSE
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

# Module 5: Quick Stats & Nation Overview Dashboard Development

## Objective

Develop interactive Tableau dashboards that enable users to explore global military capabilities through dynamic KPIs, country profiles, filters, and analytical visualizations.

---

## Features

### Quick Stats Dashboard

- Top 10 Countries by Global Firepower Power Index
- Dynamic KPI Cards
- Region Filter
- Continent Filter
- NATO Alliance Filter
- Interactive Dashboard Visualizations

### Nation Overview Dashboard

- Country Selection Filter
- Dynamic Country Profile
- Global Firepower Rank
- Power Index
- GDP
- Defense Budget
- Population
- Military Assets Visualization
- Military Manpower Visualization
- Interactive Tooltips

---

## Dashboard Components

### Quick Stats

- Top 10 Military Powers
- Total Countries
- Average Power Index
- Total Defense Budget
- Region-wise Filtering
- Continent-wise Filtering
- NATO Membership Filtering

### Nation Overview

- Country Profile
- Military Strength Overview
- Economic Indicators
- Population Statistics
- Military Assets Analysis
- Military Manpower Analysis

---

## Deliverables

- Interactive Quick Stats Dashboard
- Interactive Nation Overview Dashboard
- Tableau Workbook
- Tableau Public Dashboard

---

## Output Files

```text
Quick Stats.twbx
Nation Overview.twbx
```

---

## Technologies Used

- Tableau Desktop
- Tableau Public
- Data Visualization
- Dashboard Design
- Interactive Analytics

---

# Module 6: Compare Powers & Coalition Builder Dashboard Development

## Objective

Develop advanced comparative analytics dashboards in Tableau that enable users to compare military capabilities between two nations and simulate coalition strength by aggregating the combined military resources of multiple countries.

---

## Features

### Compare Powers Dashboard

- Side-by-side comparison of two selected countries
- Dynamic Country A and Country B selectors
- KPI comparison cards
- Military capability comparison
- Economic strength comparison
- Interactive parameter-based filtering
- Country-wise military asset comparison

### Coalition Builder Dashboard

- Multi-country coalition simulation
- Interactive country selection
- Coalition military asset aggregation
- Combined population analysis
- Combined defense budget analysis
- Combined manpower analysis
- Coalition aircraft and naval fleet analysis
- Reference country comparison
- Coalition strength evaluation

---

## Dashboard Components

### Compare Powers

- Country A Selector
- Country B Selector
- Population Comparison
- Global Firepower Rank Comparison
- Power Index Comparison
- GDP Comparison
- Defense Budget Comparison
- Military Manpower Comparison
- Aircraft Comparison
- Naval Fleet Comparison
- Economic Strength Indicator

---

### Coalition Builder

- Coalition Country Selector
- Coalition Countries List
- Coalition Population
- Coalition Defense Budget
- Coalition Military Manpower
- Coalition Aircraft
- Coalition Naval Fleet
- Reference Country Selector
- Coalition vs Reference Comparison

---

## Interactive Features

### Compare Powers

- Dynamic parameter-based country selection
- Automatic KPI updates
- Independent Country A and Country B comparison
- Responsive dashboard interactions

### Coalition Builder

- Multi-country filtering
- Automatic aggregation of coalition metrics
- Reference country selection
- Coalition strength comparison
- Interactive Tableau filters

---

## Deliverables

- Compare Powers Dashboard
- Coalition Builder Dashboard
- Interactive Tableau Workbook
- Tableau Public Dashboard

---

## Output Files

```text
global_military_firepower_2025.twbx
```

---

## Technologies Used

- Tableau Desktop
- Tableau Public
- Interactive Dashboard Design
- Parameter Actions
- Dashboard Filters
- Calculated Fields
- Aggregate Analytics

---

## Key Metrics Compared

### Compare Powers

- Global Firepower Rank
- Power Index
- Population
- GDP
- Defense Budget
- Military Manpower
- Aircraft Count
- Naval Fleet
- Economic Strength

### Coalition Builder

- Coalition Population
- Coalition Defense Budget
- Coalition Military Manpower
- Coalition Aircraft
- Coalition Naval Fleet
- Coalition Countries
- Reference Country Metrics
- Coalition vs Reference Analysis

---

# Module 7: Testing & Debugging

## Objective

Perform comprehensive quality assurance testing on all Tableau dashboards to ensure data accuracy, interactive functionality, navigation, and overall dashboard usability before final deployment.

---

## Features

- End-to-end dashboard testing
- Filter validation
- Parameter validation
- Navigation testing
- KPI verification
- Manual data validation
- Layout optimization
- Tooltip verification
- Performance testing
- Tableau Public/Desktop compatibility testing

---

## Testing Performed

### Dashboard Validation

#### Quick Stats

- Verified Region filter
- Verified Continent filter
- Verified NATO filter
- Validated KPI cards
- Verified Top 10 Countries visualization
- Verified Defense Budget chart
- Verified Assets per Capita chart

---

#### Nation Overview

- Verified Country selector
- Validated country profile information
- Verified GDP values
- Verified Defense Budget values
- Verified Population statistics
- Verified Military Assets visualization
- Verified Personnel visualization

---

#### Compare Powers

- Verified Country A parameter
- Verified Country B parameter
- Validated comparative KPIs
- Verified side-by-side comparison
- Tested interactive parameter updates

---

#### Coalition Builder

- Verified multi-country coalition selection
- Verified coalition aggregation
- Validated reference country selection
- Tested coalition vs reference comparison
- Verified aggregated coalition metrics

---

## Quality Assurance

### Functional Testing

- Dashboard filters validated
- Parameters validated
- Navigation validated
- Interactive actions verified

---

### Data Validation

- Manual spot checks performed
- KPI calculations verified
- Aggregated values validated
- Source dataset cross-checked

---

### UI/UX Validation

- Dashboard layouts aligned
- Labels verified
- Tooltips validated
- Consistent styling maintained
- Responsive dashboard behavior confirmed

---

### Performance Testing

- Workbook tested in Tableau Desktop
- Workbook tested in Tableau Public
- Dashboard loading verified
- Interactive performance validated

---

## Deliverables

- Debugged Tableau Workbook
- QA Checklist
- Verified Interactive Dashboards

---

## Output Files

```text
global_military_firepower_2025.twbx
QA_Checklist.md
```

---

## Technologies Used

- Tableau Desktop
- Tableau Public
- Dashboard Testing
- Manual QA
- Data Validation

---

# Dataset Pipeline

```text
Web Scraping
      │
      ▼
Raw Military Dataset
      │
      ▼
Data Cleaning
      │
      ▼
Feature Engineering
      │
      ▼
Tableau-Ready Dataset
      │
      ▼
Dashboard Planning
      │
      ▼
Quick Stats Dashboard
      │
      ▼
Nation Overview Dashboard
      │
      ▼
Compare Powers Dashboard
      │
      ▼
Coalition Builder Dashboard
      │
      ▼
Testing & Debugging
      │
      ▼
Interactive Military Analytics Platform
```

---

# Deliverables

## Module 1

- Web Scraper
- Raw Military Dataset

## Module 2

- Data Cleaning Notebook
- Clean Military Dataset

## Module 3

- KPI Generation Script
- Tableau-ready Dataset
- Feature Engineered Dataset

## Module 4

- Dashboard Storyboard
- Dashboard Prototype
- Navigation Flow

## Module 5

- Quick Stats Dashboard
- Nation Overview Dashboard

## Module 6

- Compare Powers Dashboard
- Coalition Builder Dashboard
- Interactive Country Comparison
- Coalition Strength Simulation
- Reference Country Comparison

## Module 7

- Debugged Tableau Workbook
- QA Checklist
- Verified Interactive Dashboards

--- 

# Future Enhancements

- Real-time military data integration
- Time-series military trend analysis
- Machine Learning based military capability prediction
- REST API integration
- Web deployment using Tableau Embedded Analytics
- Automated data refresh pipeline

---

# Dashboard Preview
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