# Unified Military Analytics and Comparison Dashboard

## Project Overview

Unified Military Analytics is an interactive dashboard project designed to analyze and compare global military capabilities using military, economic, manpower, aircraft, naval and infrastructure-related indicators.

The project uses military data for 140+ countries and provides an interactive platform for exploring military strength, comparing countries and analyzing coalition capabilities.

## Objectives

- Analyze global military power using multiple indicators.
- Provide country-level military profiles.
- Compare the military capabilities of two countries.
- Analyze combined military capabilities of multiple countries.
- Provide meaningful KPIs for military and economic analysis.
- Present the results through interactive dashboards.

## Dataset

The project uses the cleaned and processed `military_final.xlsx` dataset.

The dataset contains country-level military and economic indicators including:

- Power Index
- Power Index Rank
- GDP
- Defense Budget
- Total Population
- Active Personnel
- Reserve Personnel
- Paramilitary
- Total Military Aircraft
- Military Helicopters
- Tanks
- Armored Fighting Vehicles
- Total Naval Fleet
- Fighter Aircraft
- Attack Aircraft
- Transport Aircraft
- Trainer Aircraft
- Special Mission Aircraft
- Tanker Aircraft
- Attack Helicopters
- Region
- Continent
- Alliance

## Data Source

The military data was collected from GlobalFirepower.com using country-specific source links.

The project follows a data pipeline consisting of:

1. Data collection
2. Data cleaning
3. Data structuring
4. KPI engineering
5. Dashboard development
6. Testing and debugging
7. Documentation and GitHub release

## KPI Definitions

### Power Index Rank Gap

Power Index Rank Gap is calculated using:

Power Index Rank Gap = GDP Rank - Power Index Rank

This KPI helps identify the difference between a country's economic ranking and its military power ranking.

### Assets per Capita

Assets per Capita is calculated using:

Assets per Capita = Total Assets / Total Population

This represents the number of military assets relative to the country's population.

### Budget-to-GDP Ratio

Budget-to-GDP Ratio is calculated using:

Budget-to-GDP Ratio = Defense Budget / GDP

This represents the proportion of GDP allocated to defense spending.

## Dashboard Modules

The dashboard consists of four major sections.

### 1. Quick Stats

Quick Stats provides a global overview of military capabilities.

It allows users to explore:

- Military power rankings
- Defense budget
- Personnel
- Aircraft
- Naval capabilities
- Country-level statistics

Filters can be used to explore the dataset by:

- Country
- Region
- Continent
- Alliance

### 2. Nation Overview

Nation Overview provides a detailed profile of a selected country.

Users can view:

- Power Index
- Power Index Rank
- Defense Budget
- Active Personnel
- Reserve Personnel
- Military Aircraft
- Military Helicopters
- Tanks
- Naval Fleet
- Other military indicators

### 3. Compare Powers

Compare Powers allows users to compare two countries side-by-side.

The comparison includes:

- Power Index Rank
- Defense Budget
- Active Personnel
- Military Aircraft
- Naval Fleet

This allows users to identify differences in military and economic capabilities.

### 4. Coalition Builder

Coalition Builder allows users to select multiple countries and calculate their combined military capabilities.

The coalition can be compared with a reference country using:

- Defense Budget
- Active Personnel
- Military Aircraft
- Naval Fleet

## Technology Stack

### Programming

- Python

### Data Processing

- Pandas
- NumPy
- Excel

### Dashboard

- Streamlit

### Data Collection

- Requests
- BeautifulSoup

### Development and Version Control

- Jupyter Notebook
- Git
- GitHub

## Project Structure

```text
Unified-Military-Analytics/
│
├── Module1-Scrapping and execution/
├── Module2-Data cleaning/
├── Module3-KPI Feature Engineering/
├── Module4-Dashboard Planning and Prototyping/
├── Module5-Build Quick Stats and Nation Overview/
├── Module6-Build Compare Powers and Coalition Builder/
├── Module7-Testing and Debugging/
│   ├── Testing_and_Debugging.ipynb
│   └── QA_Test_Results.xlsx
│
├── Module8-Documentation and GitHub Release/
│   ├── README.md
│   ├── Dashboard_Usage_Guide.md
│   └── Project_Structure.md
│
└── README.md