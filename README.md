# Unified Military Analytics

## Overview

Unified Military Analytics is a data analytics and visualization project focused on analyzing and comparing global military capabilities using country-level military, defense, economic, and geographic data.

The project brings together data collection, cleaning, KPI engineering, dashboard development, comparison analysis, and coalition-level analysis into one unified analytics solution.

## Project Objectives

- Analyze global military strength across countries.
- Work with 140+ countries and 50+ military and economic indicators.
- Transform raw military data into an analysis-ready dataset.
- Create meaningful military and economic KPIs.
- Develop interactive dashboards for global, country-level, comparative, and coalition analysis.
- Provide an integrated dashboard experience with filters, parameters, navigation, and interactive visualizations.
- Maintain the complete project in a GitHub repository.

## Technologies Used

- **Python** – Data scraping, cleaning, transformation, and KPI generation
- **Pandas / NumPy** – Data processing and analysis
- **BeautifulSoup / Requests** – Web scraping
- **Excel** – Dataset preparation and validation
- **Power BI** – Dashboard prototyping and visualization
- **Tableau** – Interactive dashboard development and integration
- **Streamlit / Dash** – Dashboard application prototyping
- **Git & GitHub** – Version control and project documentation

## Project Workflow

```text
Data Sources
     ↓
Web Scraping
     ↓
Raw Military Dataset
     ↓
Data Cleaning
     ↓
KPI Feature Engineering
     ↓
Dashboard Prototyping
     ↓
Quick Stats & Nation Overview
     ↓
Compare Powers & Coalition Builder
     ↓
Dashboard Integration
     ↓
Testing & Documentation
```

## Project Modules

### Module 1 – Scraping Setup and Execution

The first module focuses on collecting country-level military data from GlobalFirepower using predefined URLs.

The scraping pipeline uses Python with Requests and BeautifulSoup to collect military metrics for 140+ countries. The collected information is stored as raw structured data and country-level HTML files are maintained where required for debugging and validation.

**Main files:**
- `links_for_military_data.txt`
- `scrape_military_metrics.py`
- `military_raw_data.csv`

### Module 2 – Data Cleaning and Structuring

This module converts the raw scraped information into a clean and standardized dataset.

The cleaning process handles unwanted characters, converts metrics into appropriate numeric formats, standardizes column names, manages missing values, and prepares the dataset for dashboard development.

**Main files:**
- `military_cleaned.csv`
- `clean_data.ipynb`

### Module 3 – KPI Feature Engineering

The third module focuses on creating derived KPIs and enriching the dataset with additional metadata.

The project includes KPIs such as:

- **Power Index Rank Gap**
- **Assets per Capita**
- **Budget-to-GDP Ratio**

Additional metadata includes Region, Continent, and Alliance information used for interactive dashboard filtering and analysis.

**Main files:**
- `military_final.xlsx`
- `generate_kpis.py`

### Module 4 – Dashboard Planning and Prototyping

This module establishes the structure and interaction model of the final dashboard solution.

The dashboard suite is organized into four major analytical views:

- **Quick Stats**
- **Nation Overview**
- **Compare Powers**
- **Coalition Builder**

Dashboard layouts, interactions, filters, buttons, navigation, KPI placement, and visualization requirements are planned before the final dashboard integration.

### Module 5 – Quick Stats and Nation Overview

#### Quick Stats

Quick Stats provides a global overview of military power and defense-related information.

Key dashboard features include:

- Top 10 Countries by Power Index
- Region filter
- Continent filter
- Alliance filter
- Dynamic KPI cards
- Defense budget analysis
- Regional military and defense comparisons

#### Nation Overview

Nation Overview provides a detailed profile of a selected country.

It focuses on:

- Country-level military capabilities
- Major military metrics
- Military strength indicators
- Rankings and comparisons
- Interactive country selection
- Supporting charts and tooltips

### Module 6 – Compare Powers and Coalition Builder

#### Compare Powers

Compare Powers allows users to select two countries and compare their military capabilities side by side.

The dashboard compares important areas such as:

- Manpower
- Aircraft
- Navy
- Defense Budget
- Military KPIs

#### Coalition Builder

Coalition Builder allows users to select multiple countries and analyze their combined military capabilities.

It provides:

- Multi-country selection
- Aggregated military metrics
- Coalition-level analysis
- Comparison against another coalition or reference country

#### Dashboard Integration

The final dashboard environment connects the major dashboard views through navigation and interactive controls.

The integrated dashboard suite contains:

1. Quick Stats
2. Nation Overview
3. Compare Powers
4. Coalition Builder

## Dashboard Features

### Interactive Filters

The dashboards use interactive filters including:

- Region
- Continent
- Alliance
- Country selection where applicable

### Dynamic KPIs

KPI cards provide dynamic values based on the selected dashboard filters and parameters.

### Interactive Comparisons

Country and coalition selections allow users to dynamically compare military capabilities.

### Navigation

Dashboard navigation connects the different analytical views into a unified experience.

### Tooltips

Charts provide additional context such as rankings, values, and comparative information.

## Key KPIs

### Power Index Rank Gap

Represents the project-defined difference associated with Power Index rankings.

### Assets per Capita

Represents military assets in relation to population.

### Budget-to-GDP Ratio

Represents defense spending relative to GDP.

## Dashboard Suite

| Dashboard | Description |
|---|---|
| **Quick Stats** | Global overview of military strength, rankings, KPIs, and defense budget |
| **Nation Overview** | Detailed analysis of an individual country's military profile |
| **Compare Powers** | Side-by-side comparison of two countries |
| **Coalition Builder** | Analysis of combined military capabilities of selected countries |

## Project Structure

```text
Unified-Military-Analytics/
│
├── Module 1/
│   ├── links_for_military_data.txt
│   ├── scrape_military_metrics.py
│   └── military_raw_data.csv
│
├── Module 2/
│   ├── military_cleaned.csv
│   └── clean_data.ipynb
│
├── Module 3/
│   ├── military_final.xlsx
│   └── generate_kpis.py
│
├── Module 4/
│   └── Dashboard Prototype
│
├── Module 5/
│   ├── Quick Stats
│   ├── Nation Overview
│   └── Dashboard files
│
├── Module 6/
│   └── global_military_firepower_2025.twbx
│
└── README.md
```

## Final Output

The final project combines military data engineering and interactive visualization into a unified analytics solution.

It enables users to explore global military rankings, inspect individual countries, compare military powers, and analyze the combined strength of selected countries through the integrated dashboard suite.

## Conclusion

Unified Military Analytics provides an end-to-end approach to transforming global military data into interactive analytical insights.

The project combines **Python-based data engineering, KPI feature engineering, Power BI prototyping, Tableau visualization, dashboard integration, and GitHub-based project management** into a single unified solution.
