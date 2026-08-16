# Unified Military Analytics

## Project Overview

Unified Military Analytics is a data analytics and visualization project that analyzes military strength and economic indicators for countries around the world.

The project collects military data, cleans and prepares the dataset, engineers key performance indicators (KPIs), and presents the results through interactive Tableau dashboards.

The final Tableau workbook contains four integrated dashboards:

- Quick Stats Dashboard
- Nation Overview Dashboard
- Compare Powers Dashboard
- Coalition Builder Dashboard

---

## Project Objectives

- Collect military and country-level data.
- Clean and standardize the collected data.
- Create meaningful military and economic KPIs.
- Analyze military strength across countries.
- Provide interactive filtering and country selection.
- Compare the military capabilities of two countries.
- Analyze selected groups of countries as a coalition.
- Present insights through interactive Tableau dashboards.

---

## Data Collection / Scraping Method

Military data was collected from publicly available Global Firepower information using Python-based web scraping.

The scraping process used:

- Python
- Requests
- BeautifulSoup
- Pandas

The collected information includes military and economic indicators such as:

- Power Index
- Defense Budget
- Active Military Personnel
- Reserve Personnel
- Military Aircraft
- Tanks
- Naval assets
- Submarines
- Purchasing Power
- Population
- GDP and other related indicators

The scraped data was initially stored as raw CSV data and subsequently cleaned and transformed for analysis.

---

## Data Cleaning and Preparation

The raw dataset was cleaned and prepared using Python and Pandas.

The cleaning process included:

- Standardizing country names.
- Cleaning numeric values.
- Removing unnecessary characters from numeric fields.
- Handling missing values.
- Converting columns to appropriate data types.
- Standardizing column names.
- Preparing the dataset for KPI calculations and visualization.

The cleaned dataset was then used to create the final analytical dataset.

---

## KPI Definitions

### Power Index Score

The Power Index Score represents the military strength of a country.

A lower Power Index Score indicates a stronger military position.

### Power Rank

Power Rank represents the country's ranking based on its Power Index Score.

### Defense Budget

The total amount allocated to defense and military expenditure.

### Total Military Assets

Represents the combined military equipment and assets available to a country.

### Active Military Personnel

The number of active-duty military personnel.

### Reserve Personnel

The number of military personnel available in reserve forces.

### Total Military Aircraft

The total number of military aircraft available.

### Attack Aircraft

The number of aircraft primarily intended for attack missions.

### Fighter Aircraft

The number of fighter aircraft available.

### Submarines

The number of submarines operated by a country.

### Purchasing Power

Represents the purchasing power measure used in the dataset to support economic and military analysis.

### GDP Rank

The country's ranking based on its GDP.

### Power Rank Gap

Power Rank Gap compares the military power ranking with the GDP ranking.

It is calculated as:

`Power Rank Gap = Power Rank - GDP Rank`

---

# Tableau Dashboards

The final Tableau workbook contains four integrated dashboards.

## 1. Quick Stats Dashboard

The Quick Stats Dashboard provides a high-level view of military strength across countries.

It includes:

- Total Defense Budget
- Average Power Index
- Total Active Personnel
- Number of Countries Selected
- World Map
- Top 10 Countries by Power Index

### Filters

The dashboard provides filters such as:

- Country
- Region
- Continent
- Alliance

These filters dynamically update the relevant dashboard visuals and KPI values.

---

## 2. Nation Overview Dashboard

The Nation Overview Dashboard provides a detailed profile of a selected country.

It includes:

- Power Rank
- Power Score
- Defense Budget
- GDP Rank
- Power Rank Gap
- Purchasing Power
- Attack Aircraft
- Fighter Aircraft
- Military Power Map
- Air Power Metrics

### Country Selection

Select a country using the country filter to display its corresponding military and economic profile.

Tooltips provide additional information and comparisons where applicable.

---

## 3. Compare Powers Dashboard

The Compare Powers Dashboard provides a side-by-side comparison of any two selected countries.

The dashboard compares:

- Power Index Score
- Defense Budget
- Total Military Assets
- Submarines
- Total Military Aircraft
- Available Manpower

The country selections allow users to analyze differences between two countries.

---

## 4. Coalition Builder Dashboard

The Coalition Builder Dashboard allows users to select multiple countries and analyze their combined military strength.

It includes aggregated metrics such as:

- Defense Budget
- Total Military Assets
- Total Military Aircraft
- Total Submarines
- Average Power Index Score

The dashboard also provides a reference-country comparison and a coalition military-strength visualization.

---

# How to Open the Tableau Dashboard

1. Download the final Tableau packaged workbook:

   `global_military_firepower_2025.twbx`

2. Open Tableau Desktop or Tableau Public.

3. Open the `.twbx` workbook.

4. Allow Tableau to load the packaged data sources.

5. Navigate between the four dashboards using the navigation buttons.

---

# How to Use the Dashboards

### Quick Stats

1. Select a Region, Continent, Alliance, or Country.
2. Observe the KPI cards.
3. Analyze the world map.
4. Examine the Top 10 Countries by Power Index chart.

### Nation Overview

1. Select a country.
2. Review its military profile.
3. Examine the KPI cards.
4. Use the charts and map for detailed analysis.
5. Hover over visual elements to view tooltips.

### Compare Powers

1. Select Country 1.
2. Select Country 2.
3. Compare the displayed military and economic metrics.
4. Use the charts to identify differences between the countries.

### Coalition Builder

1. Select multiple countries.
2. Review the aggregated coalition metrics.
3. Compare the coalition against the reference country.
4. Analyze the coalition military-strength chart.

---

# Dashboard Navigation

Navigation buttons are provided across the dashboards to allow seamless movement between:

- Quick Stats
- Nation Overview
- Compare Powers
- Coalition Builder

This allows users to move between high-level analysis, individual country analysis, country comparison, and coalition analysis.

---

# Testing and Validation

The dashboards were tested during the final testing phase.

The following were verified:

- Country filters work correctly.
- Region filters work correctly.
- Continent filters work correctly.
- Alliance filters work correctly.
- Country selection updates the Nation Overview.
- Country comparison works correctly.
- Coalition selection works correctly.
- Dashboard navigation works correctly.
- KPI values were manually checked.
- Active personnel values were corrected and verified.
- Charts and tooltips were checked.
- Dashboard layouts were reviewed.
- The final Tableau workbook was tested in Tableau.

---

# Technologies Used

- Python
- Pandas
- BeautifulSoup
- Requests
- Tableau
- Microsoft Excel
- Git
- GitHub

---

# Project Structure

```text
Unified-Military-Analytics/
│
├── Module 1/
├── Module 2/
├── Module 3/
├── Module 4/
├── Module 5/
├── Module 6/
├── Module 7/
├── Module 8/
│   └── README.md
│
└── README.md
