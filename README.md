# Unified Military Analytics and Comparison Dashboard

## Project Overview

The **Unified Military Analytics and Comparison Dashboard** is an interactive data analytics project developed as part of the **Infosys Springboard Virtual Internship 7.0**.

The project collects, processes, analyzes, and visualizes country-level military and economic data. The final Tableau dashboards allow users to explore military strength, economic indicators, military assets, and comparative country performance through interactive filters, parameters, charts, maps, and navigation.

The project focuses on making complex military datasets easier to explore and compare through an interactive business-intelligence dashboard.

---

## Project Objectives

The main objectives of the project are to:

* Collect country-level military data through web scraping.
* Clean and structure the collected data using Python.
* Prepare a reliable dataset for visualization.
* Engineer meaningful military and economic KPIs.
* Build interactive Tableau dashboards.
* Provide country-level and comparative analysis.
* Enable filtering by geographic and NATO-related attributes.
* Provide navigation between multiple analytical dashboards.
* Package and document the final project for GitHub.

---

## Data Collection and Scraping

Military data was collected from **Global Firepower** country-level pages using Python.

### Technologies Used

* Python
* `requests`
* `BeautifulSoup`
* `pandas`

### Scraping Process

The scraping workflow uses a text file containing the country URLs:

`links_for_military_data.txt`

The Python scraping script:

1. Reads the country URLs.
2. Sends HTTP requests using an appropriate browser User-Agent.
3. Downloads the country webpages.
4. Parses the HTML using BeautifulSoup.
5. Extracts relevant military and personnel metrics.
6. Stores the extracted values in structured records.
7. Combines the records into a pandas DataFrame.
8. Saves the collected data for further processing and analysis.

### Example Data Categories

The dataset contains military and country-level information including:

* Population
* Active Personnel
* Reserve Personnel
* Paramilitary Personnel
* Aircraft
* Helicopters
* Tanks
* Naval Assets
* Defense Budget
* GDP
* Military Power Rank
* Power Index
* Other military asset metrics

The cleaned dataset is used as the primary data source for the Tableau dashboards.

---

## Data Processing

The collected data was processed using Python and pandas.

The processing stage included:

* Cleaning inconsistent values.
* Converting numeric fields into appropriate formats.
* Handling missing values.
* Structuring country-level records.
* Preparing calculated military metrics.
* Creating a final dataset suitable for Tableau visualization.

Missing values were retained where source data was unavailable rather than incorrectly replacing them with zero.

For example, GDP is unavailable for some countries in the source dataset. These values remain NULL in the dataset and may therefore appear blank in the corresponding Tableau KPI.

---

# Dashboard Structure

The final project contains four major Tableau dashboards.

## 1. Quick Stats Dashboard

The Quick Stats Dashboard provides a high-level overview of countries based on the selected filters.

### Interactive Filters

* Region
* Continent
* NATO Member

These filters update the connected KPIs and visualizations together.

### KPIs

The dashboard includes:

* Total Countries
* Power Index Score
* Military Power Rank
* Defense Budget
* Population

### Visualizations

* Top 10 Countries by Power Index
* Top 5 Countries by GDP
* Top 5 Countries by Defense Budget
* Top 5 Countries by Military Assets
* World Military Map

The dashboard provides a quick overview of military and economic strength across different geographic and NATO-based selections.

---

## 2. Nation Overview

The Nation Overview dashboard provides a detailed profile of an individual country.

Users can select a country and examine:

* Military Power Rank
* Power Index Score
* GDP
* Defense Budget
* Population
* Military Assets
* Personnel Distribution
* Military Strength dimensions
* Other country-level military indicators

The dashboard combines KPI cards, charts, and interactive visualizations to provide a country-specific overview.

---

## 3. Compare Powers

The Compare Powers dashboard allows users to select and compare two countries.

The dashboard provides comparative analysis of indicators such as:

* Military strength
* Power Index
* Population
* GDP
* Defense Budget
* Military personnel
* Military dimensions
* Other relevant military indicators

This dashboard helps users identify differences and similarities between selected countries.

---

## 4. Coalition Builder

The Coalition Builder dashboard allows users to evaluate combinations of multiple countries.

Users can work with:

* Two-country combinations
* Three-country combinations
* Four-country combinations
* Reference countries
* Different comparison metrics

The dashboard is intended to support analysis of combined military capabilities and comparative coalition strength.

---

# KPI Definitions

## Total Countries

The number of countries remaining after applying the selected dashboard filters.

## Military Power Rank

The military ranking of a country based on the source dataset.

## Power Index Score

A numerical indicator representing the military power of a country. Lower values indicate stronger military capability according to the Global Firepower methodology.

## GDP

Gross Domestic Product, representing the economic size of a country.

GDP values are displayed when source data is available. Missing source values remain NULL rather than being represented as zero.

## Defense Budget

The country's reported defense expenditure/budget from the source dataset.

## Population

The total population associated with the selected country or filtered group.

---

# Dashboard Interactivity

The dashboards use Tableau filters, parameters, calculated fields, and navigation actions.

### Quick Stats Filters

The Quick Stats Dashboard uses:

* Region
* Continent
* NATO Member

Changing these filters updates the connected KPIs and visualizations.

### Country Selection

Nation Overview uses country selection to dynamically update the country profile.

### Country Comparison

Compare Powers provides Country A and Country B selections for comparative analysis.

### Coalition Selection

Coalition Builder allows multiple country selections and comparison configurations.

### Circular Navigation

The project uses a **circular navigation system** connecting all four dashboards:

**Quick Stats → Nation Overview → Compare Powers → Coalition Builder → Quick Stats**

This allows users to continuously move between the four analytical dashboards without leaving the Tableau workbook.

---

# Project Structure

The GitHub repository is organized into logical project sections.

```text
Unified-Military-Analytics/
│
├── scripts/
│   └── Python scraping and data-processing scripts
│
├── data/
│   ├── Raw data
│   └── Cleaned/final datasets
│
├── dashboard/
│   └── Tableau workbook
│
├── docs/
│   └── Supporting project documentation
│
└── README.md
```

The exact filenames may vary depending on the final repository organization.

---

# How to Open the Tableau Dashboard

## Tableau Desktop

1. Download or clone the GitHub repository.
2. Navigate to the dashboard/workbook folder.
3. Open the `.twbx` Tableau packaged workbook.
4. Allow Tableau to load the embedded data and workbook resources.
5. Use the navigation controls to move between the dashboards.

## Tableau Public

If the workbook is published to Tableau Public, users can open the published dashboard through the Tableau Public link provided in the repository.

---

# How to Use the Quick Stats Dashboard

1. Open the Quick Stats Dashboard.
2. Select a **Region**.
3. Select a **Continent**.
4. Select a **NATO Member** value.
5. Observe the KPI cards and visualizations update.
6. Review the Top 10 Power Index chart.
7. Review the Top 5 GDP chart.
8. Review the Top 5 Defense Budget chart.
9. Review the Top 5 Military Assets chart.
10. Explore the World Military Map.
11. Use the circular navigation controls to move to other dashboards.

---

# Testing and Quality Assurance

The dashboards were tested for:

* Filter functionality
* Parameter functionality
* KPI updates
* Chart updates
* Country selection
* Country comparison
* Coalition selections
* Circular navigation between dashboards
* Tooltip behavior
* Data display
* Missing-value behavior
* Dashboard layout
* Tableau workbook functionality

Manual spot checks were performed using different countries and filter combinations to verify that dashboard values and visualizations responded as expected.

---

# Technology Stack

| Area            | Technology                       |
| --------------- | -------------------------------- |
| Web Scraping    | Python                           |
| HTTP Requests   | requests                         |
| HTML Parsing    | BeautifulSoup                    |
| Data Processing | pandas, NumPy                    |
| Visualization   | Tableau Public / Tableau Desktop |
| Version Control | Git / GitHub                     |

---

# Final Deliverables

The final project includes:

* Python scraping scripts
* Raw and processed data
* Cleaned dataset
* Tableau packaged workbook
* README documentation
* GitHub repository

---

# Project Status

**Status: Final Review and Delivery**

The major scraping, data-processing, KPI engineering, dashboard development, testing, documentation, and GitHub release activities have been completed.

The final workbook is intended to be a clean, interactive, and shareable military analytics dashboard suitable for portfolio and internship-project presentation.

---

## Author

**Yasmin Shaik**

**Infosys Springboard Virtual Internship 7.0**

**Project: Unified Military Analytics and Comparison Dashboard**




