# Unified Military Analytics

An end-to-end data engineering and analytics pipeline that collects, cleans, enriches, analyzes, and visualizes global military statistics from **Global Firepower** to create an interactive military intelligence analytics platform.

The project combines **Python-based web scraping, data preprocessing, feature engineering, Tableau visualization, interactive dashboard development, testing, documentation, and GitHub-based project delivery**.

---

## Overview

**Unified Military Analytics** is designed to transform publicly available global military data into a structured, analysis-ready dataset and an interactive visualization platform.

The system collects country-wise military, manpower, economic, infrastructure, natural resource, and geographical indicators from multiple Global Firepower pages. The collected information is processed through a modular data engineering pipeline involving:

- Automated web scraping
- Data cleaning and preprocessing
- Data enrichment
- KPI and feature engineering
- Tableau data preparation
- Interactive dashboard development
- Testing and debugging
- Documentation and GitHub release

The final system allows users to explore global military capabilities through four major interactive dashboards:

1. **Quick Stats**
2. **Nation Overview**
3. **Compare Powers**
4. **Coalition Builder**

---

# Project Objectives

The major objectives of Unified Military Analytics are:

- Automate military data collection from publicly available sources.
- Consolidate country-wise military statistics into a unified dataset.
- Clean and standardize raw web-scraped data.
- Integrate military information with economic and regional metadata.
- Generate meaningful analytical KPIs.
- Develop interactive Tableau dashboards.
- Enable dynamic country-to-country comparison.
- Enable multi-country coalition analysis.
- Validate dashboard calculations, filters, parameters, and navigation.
- Maintain a clean and documented GitHub repository.
- Provide a shareable and portfolio-ready analytics solution.

---

# Project Architecture

```text
                         Global Firepower
                                │
                                ▼
              Module 1: Data Collection & Scraping
                                │
                                ▼
                       Raw Military Data
                                │
                                ▼
              Module 2: Cleaning & Structuring
                                │
                                ▼
                     Clean Military Data
                                │
                                ▼
               Module 3: KPI Feature Engineering
                                │
                                ▼
                 Tableau-Ready Dataset
                                │
                                ▼
               Module 4: Dashboard Planning
                                │
                                ▼
              Module 5: Quick Stats & Nation
                         Overview
                                │
                                ▼
             Module 6: Compare Powers &
                       Coalition Builder
                                │
                                ▼
                Module 7: Testing & QA
                                │
                                ▼
             Module 8: Documentation &
                    GitHub Release
                                │
                                ▼
              Interactive Military Analytics
                         Platform

```
---

# Project Structure

```text
Unified-Military-Analytics/
│
├── data/
│   │
│   ├── military_raw_data.csv
│   ├── military_cleaned.csv
│   ├── military_final.xlsx
│   └── military_long.xlsx
│
├── scripts/
│   │
│   ├── scrape_military_metrics.ipynb
│   ├── clean_data.ipynb
│   └── generate_kpis.py
│
├── dashboard/
│   │
│   ├── Quick Stats.twbx
│   ├── Nation Overview.twbx
│   ├── Compare Powers.twbx
│   ├── Coalition Builder.twbx
│   └── global_military_firepower_2025.twbx
│
├── docs/
│   │
│   ├── Storyboard for dashboard layouts.pdf
│   ├── dashboard application prototype with link.pdf
│   ├── Dashboard_Usage_Guide.md
│   └── QA_Checklist.md
│
├── links_for_military_data.txt
├── requirements.txt
├── README.md
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

# Module 8: Documentation & GitHub Release

## Objective

Finalize the Unified Military Analytics project by documenting the complete data pipeline, organizing project files, preparing dashboard usage guidance, and releasing the final project through GitHub.

---

## Documentation Steps

### Final README

Document:

* Project overview
* Project objectives
* Project architecture
* Data pipeline
* Scraping methodology
* Data cleaning process
* KPI definitions
* Dashboard modules
* Technologies used
* Installation and usage information

---

### Dashboard Usage Guide

Provide instructions for using:

* Quick Stats Dashboard
* Nation Overview Dashboard
* Compare Powers Dashboard
* Coalition Builder Dashboard
* Filters and parameters
* Country selectors
* Dashboard navigation
* Interactive charts and tooltips

---

### Repository Organization

Organize the final project into structured directories:

```text
data/
scripts/
dashboard/
docs/
```

---
# Dataset Pipeline

```text
Global Firepower
       │
       ▼
Web Scraping
       │
       ▼
Raw Dataset
       │
       ▼
Data Cleaning
       │
       ▼
Data Structuring
       │
       ▼
Economic & Regional Enrichment
       │
       ▼
KPI / Feature Engineering
       │
       ▼
Tableau-Ready Dataset
       │
       ▼
Dashboard Development
       │
       ├───────────────┐
       ▼               ▼
 Quick Stats     Nation Overview
       │               │
       └───────┬───────┘
               ▼
        Compare Powers
               │
               ▼
       Coalition Builder
               │
               ▼
       Testing & Debugging
               │
               ▼
      Documentation & Release
               │
               ▼
        GitHub Repository
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

## Module 8

- README.md
- docs/Dashboard_Usage_Guide.md
- Documentation
  
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

## Scraping Method

The project collects country-wise military, economic, manpower, infrastructure, natural resource, and geographical statistics from publicly available **Global Firepower** pages.

The scraping pipeline is implemented using Python and follows these steps:

```text
Global Firepower Pages
        ↓
HTTP Requests
        ↓
HTML Response
        ↓
BeautifulSoup Parsing
        ↓
Metric Extraction
        ↓
Country-wise Data
        ↓
Unified Raw Dataset
```

---


### Scraping Process

1. Source URLs are maintained for the required Global Firepower pages.
2. Python requests is used to retrieve webpage content.
3. BeautifulSoup parses the HTML structure.
4. Required military metrics are extracted from the webpages.
5. Country names are used to merge data collected from different sources.
6. Extracted values are standardized and stored in a unified dataset.
7. The raw dataset is exported for further cleaning and processing.

## Output
``` military_raw_data.csv ```

The raw dataset is then passed to the data-cleaning module before KPI generation and Tableau visualization.

---

## KPI Definitions

The final analytical dataset contains military, economic, manpower, regional, and derived indicators.

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

## How to Open the Tableau Dashboards

The project contains four interactive Tableau dashboards:

1. Quick Stats
2. Nation Overview
3. Compare Powers
4. Coalition Builder

The Tableau workbooks are stored inside the:

```dashboard/```

directory.

## Opening the Workbooks
Using Tableau Desktop

- Install and open Tableau Desktop.
- Navigate to the project's dashboard/ directory.
- Open the required .twbx workbook.
- Allow Tableau to load the packaged data source.
- Open the required dashboard from the workbook.
- Use the available filters, parameters, and dashboard actions.

# Dashboard Usage Guidance

The Unified Military Analytics platform consists of four interactive Tableau dashboards. Each dashboard is designed for a specific analytical purpose and uses filters, parameters, calculated fields, and dashboard actions to support interactive exploration.

---

## 1. Quick Stats Dashboard

### Purpose

The Quick Stats dashboard provides a high-level overview of global military capabilities and economic indicators.

### How to Use

1. Open the Quick Stats dashboard in Tableau Desktop or Tableau Public.
2. Use the available filters to narrow the dataset.
3. Select a specific region, continent, or NATO membership category.
4. Observe the KPI cards update dynamically.
5. Explore the Top 10 Military Powers visualization.
6. Hover over charts and marks to view detailed tooltips.
7. Clear the filters to return to the complete dataset.

### Main Features

- Total Countries
- Average Power Index
- Total Defense Budget
- Average GDP
- Top Military Powers
- Assets per Capita
- NATO Distribution
- Region-wise analysis
- Continent-wise analysis

---

## 2. Nation Overview Dashboard

### Purpose

The Nation Overview dashboard provides a detailed profile of a selected country.

### How to Use

1. Open the Nation Overview dashboard.
2. Select a country using the Country filter.
3. The country profile updates automatically.
4. Review the country's military, economic, manpower, and population indicators.
5. Hover over charts to view detailed values.
6. Change the selected country to compare different country profiles.

### Main Features

- Country Name
- Global Firepower Rank
- Power Index
- GDP
- Defense Budget
- Population
- Military Manpower
- Military Assets
- Aircraft
- Naval Assets
- Economic Indicators

---

## 3. Compare Powers Dashboard

### Purpose

The Compare Powers dashboard enables users to compare two selected countries using common military and economic indicators.

### How to Use

1. Select **Country A** using the Country A parameter.
2. Select **Country B** using the Country B parameter.
3. The comparison automatically updates.
4. Review the KPI cards and comparison charts.
5. Change either country to perform another comparison.
6. Hover over the visualizations to inspect individual values.

### Main Comparison Parameters

- Global Firepower Rank
- Power Index
- Population
- GDP
- Defense Budget
- Military Manpower
- Aircraft
- Naval Fleet
- Economic Strength
- Selected Military Assets

## 4. Coalition Builder Dashboard

### Purpose

The Coalition Builder allows users to select multiple countries and analyze their combined capabilities.

### How to Use

1. Select multiple countries using the Coalition Country selector.
2. The selected countries form the coalition.
3. Tableau automatically calculates aggregated coalition metrics.
4. Select a Reference Country.
5. Compare the coalition against the selected reference country.
6. Review the difference using KPI cards and comparison visualizations.
7. Reference Country Metrics

### Coalition Aggregation

Additive metrics are aggregated using the selected countries.

---

### GitHub Release Structure

The final repository is organized into separate directories for datasets, scripts, dashboards, and documentation.

### Comparison Logic

Each selected country is evaluated independently using the same set of indicators.

```text
Country A Metrics
       │
       ├── Military Indicators
       ├── Economic Indicators
       └── Manpower Indicators

Country B Metrics
       │
       ├── Military Indicators
       ├── Economic Indicators
       └── Manpower Indicators

              ↓

       Side-by-Side Comparison

```

---

## GitHub Release Structure

The final repository is organized into separate directories for datasets, scripts, dashboards, and documentation.

```text
Unified-Military-Analytics/
│
├── data/
│   ├── military_raw_data.csv
│   ├── military_cleaned.csv
│   ├── military_final.xlsx
│   └── military_long.xlsx
│
├── scripts/
│   ├── scrape_military_metrics.ipynb
│   ├── clean_data.ipynb
│   └── generate_kpis.py
│
├── dashboard/
│   ├── Quick Stats.twbx
│   ├── Nation Overview.twbx
│   ├── Compare Powers.twbx
│   ├── Coalition Builder.twbx
│   └── global_military_firepower_2025.twbx
│
├── docs/
│   ├── Storyboard for dashboard layouts.pdf
│   ├── dashboard application prototype with link.pdf
│   ├── Dashboard_Usage_Guide.md
│   └── QA_Checklist.md
│
├── links_for_military_data.txt
├── requirements.txt
├── README.md
└── LICENSE
```

---

## GitHub Release Structure

The final release follows a structured development and version-control workflow.

```text
Development Completed
        │
        ▼
Dashboard Testing
        │
        ▼
Data Validation
        │
        ▼
QA Checklist
        │
        ▼
Documentation
        │
        ▼
Repository Organization
        │
        ▼
README Finalization
        │
        ▼
Git Add
        │
        ▼
Git Commit
        │
        ▼
Git Push
        │
        ▼
GitHub Final Release
```
---

## Optional Tableau Public Release

The completed Tableau workbook can optionally be published on Tableau Public to make the project accessible as an online portfolio demonstration.
Tableau Public Dashboard: <https://public.tableau.com/app/profile/nupur.madaan/viz/UnifiedMilitaryAnalyticsandComparisonDashboard/QuickStats?publish=yes>

```text
Final Tableau Workbook
        │
        ▼
QA Testing
        │
        ▼
Verify Filters & Parameters
        │
        ▼
Verify Dashboard Navigation
        │
        ▼
Verify Data Values
        │
        ▼
Publish to Tableau Public
        │
        ▼
Generate Public Dashboard Link
        │
        ▼
Add Link to GitHub README
```

---
## Technology Stack 
| Area                  | Technology / Tool            |
| --------------------- | ---------------------------- |
| Programming Language  | Python                       |
| Web Scraping          | Requests, BeautifulSoup      |
| Data Processing       | Pandas, NumPy                |
| Development           | Jupyter Notebook             |
| Data Storage          | CSV, Excel                   |
| Data Visualization    | Tableau Desktop              |
| Dashboard Publishing  | Tableau Public               |
| Dashboard Interaction | Parameters, Filters, Actions |
| Data Transformation   | Pandas, Calculated Fields    |
| Documentation         | Markdown                     |
| Version Control       | Git                          |
| Repository            | GitHub                       |
| Data Source           | Global Firepower             |

# Acknowledgements

* Global Firepower
* Python Open Source Community
* Pandas
* BeautifulSoup
* Requests