# Unified Military Analytics Dashboard

A complete data analytics and visualization project that collects, processes, analyzes, and visualizes global military data for 145 countries.

The project was developed as part of the **Infosys Internship** and covers the complete data workflow, from web scraping and data cleaning to KPI engineering and interactive dashboard development.

---

# Project Overview

The **Unified Military Analytics Dashboard** provides an interactive view of global military capabilities using military, economic, demographic, infrastructure, and geographical data.

The project analyzes **145 countries** and includes metrics related to:

- Military power
- Personnel and manpower
- Air power
- Land power
- Naval power
- Defense budgets
- Economic indicators
- Natural resources
- Infrastructure
- Geography

The final solution is presented through an interactive **Power BI dashboard** consisting of four main dashboard pages.

---

# Project Workflow

The project was completed across four milestones.

```text
Data Collection
       ↓
Data Cleaning
       ↓
KPI Engineering
       ↓
Dashboard Planning
       ↓
Power BI Dashboard Development
       ↓
Testing and Debugging
       ↓
Documentation and GitHub Release
````

---

# Milestone 1: Data Collection and Preparation

## Module 1: Scraping Setup and Execution

Military data was collected from publicly available Global Firepower data pages.

A Python web scraping script was developed to extract military metrics for **145 countries**.

### Technologies Used

* Python
* Requests
* BeautifulSoup
* Pandas

### Output

```text
military_raw_data.csv
```

The scraping process collected multiple military metrics including:

* Power Index
* Military Personnel
* Aircraft
* Tanks
* Armored Fighting Vehicles
* Artillery
* Naval Fleet
* Defense Budget
* Natural Resources
* Infrastructure
* Geographic Data

---

## Module 2: Data Cleaning and Structuring

The raw dataset was cleaned and structured using Python.

The data cleaning process included:

* Handling missing values
* Converting numeric columns
* Cleaning country names
* Removing unnecessary values
* Standardizing data formats
* Preparing the dataset for analysis

### Files

```text
clean_data.ipynb
military_cleaned.csv
```

---

# Milestone 2: KPI Engineering and Dashboard Preparation

## Module 3: KPI Feature Engineering

Additional KPIs were created from the cleaned dataset.

Examples include:

### Power Index Rank Gap

Measures the difference between a country's Power Index rank and GDP rank.

### Assets Per Capita

Represents military assets relative to the country's population.

### Budget to GDP Ratio

Measures defense spending relative to the country's GDP.

### Total Assets

A combined military asset metric used for high-level comparison.

### Final Dataset

The processed dataset used for dashboard development is:

```text
military_final.xlsx
```

The dataset contains military, economic, demographic, infrastructure, and geographic metrics for **145 countries**.

---

## Module 4: Dashboard Planning and Prototyping

Before developing the final dashboards, wireframes and prototypes were created.

The dashboard designs included:

* Quick Stats
* Nation Overview
* Compare Powers
* Coalition Builder

Wireframes were used to plan the dashboard layout and visual structure before implementation.

---

# Milestone 3: Full Dashboard Development

The final interactive dashboards were developed using **Microsoft Power BI**.

The report contains four main dashboards.

---

# 1. Quick Stats

The Quick Stats dashboard provides a high-level overview of global military power.

### Features

* Top 10 countries by Power Index
* Region filter
* Continent filter
* Alliance filter
* Dynamic KPI cards
* Interactive filtering

Users can quickly explore how military rankings and statistics change based on geographical and alliance-based selections.

---

# 2. Nation Overview

The Nation Overview dashboard provides a detailed profile of an individual country.

Users can select a country and view its major military metrics.

### Features

* Country selector
* Global Power Rank
* Power Index
* GDP
* Defense Budget
* Active Personnel
* Total Military Assets
* Air Power visualization
* Land Power visualization
* Naval Power visualization
* Overall Military Strength Profile

The dashboard dynamically updates based on the selected country.

---

# 3. Compare Powers

The Compare Powers dashboard allows users to compare any two countries side by side.

### Features

* Independent Country 1 selector
* Independent Country 2 selector
* Power Index comparison
* Global Rank comparison
* Active Personnel comparison
* Military Aircraft comparison
* Naval Fleet comparison
* Defense Budget comparison
* Normalized military capability comparison chart

The normalized comparison chart allows metrics with significantly different scales to be compared visually.

---

# 4. Coalition Builder

The Coalition Builder allows users to select multiple countries and treat them as a combined coalition.

### Features

* Multi-country coalition selection
* Aggregated Active Personnel
* Aggregated Aircraft
* Aggregated Naval Fleet
* Aggregated Defense Budget
* Reference country selection
* Coalition vs Reference Country comparison
* Visual comparison chart

This allows users to analyze the combined military capabilities of multiple countries and compare them against another country.

---

# Dashboard Navigation

All four dashboard pages are connected using Power BI Page Navigation.

Users can move seamlessly between:

```text
Quick Stats
     ↓
Nation Overview
     ↓
Compare Powers
     ↓
Coalition Builder
```

The active dashboard page is highlighted in the navigation bar.

---

# Dataset

The final dataset contains data for **145 countries**.

Major categories include:

## Military Personnel

* Total Population
* Total Military Manpower
* Fit for Service
* Population Reaching Military Age
* Active Personnel
* Reserve Personnel
* Paramilitary Personnel

## Air Power

* Total Military Aircraft
* Fighter Aircraft
* Attack Aircraft
* Transport Aircraft
* Trainer Aircraft
* Special Mission Aircraft
* Tanker Aircraft
* Military Helicopters
* Attack Helicopters

## Land Power

* Tanks
* Armored Fighting Vehicles
* Self-Propelled Artillery
* Towed Artillery
* Rocket Projectors

## Naval Power

* Total Naval Fleet
* Naval Fleet Tonnage
* Aircraft Carriers
* Helicopter Carriers
* Submarines
* Destroyers
* Frigates
* Corvettes
* Coastal Patrol Craft
* Mine Warfare Craft

## Economy

* GDP
* Defense Budget
* External Debt
* Purchasing Power Parity
* Foreign Exchange and Gold Reserves

## Infrastructure

* Serviceable Airports
* Labour Force
* Major Ports and Terminals
* Merchant Marine Fleet
* Railway Coverage
* Roadway Coverage

## Natural Resources

* Oil Production
* Oil Consumption
* Proven Oil Reserves
* Natural Gas Production
* Natural Gas Consumption
* Natural Gas Reserves
* Coal Production
* Coal Consumption
* Proven Coal Reserves

## Geography

* Total Land Area
* Coastline Coverage
* Border Coverage
* Waterway Coverage

---

# Tools and Technologies

## Programming and Data Processing

* Python
* Pandas
* Requests
* BeautifulSoup

## Data Analysis

* Microsoft Excel
* Python

## Dashboard Development

* Microsoft Power BI
* DAX
* Power Query

## Version Control

* Git
* GitHub

---

# Project Structure

```text
Unified-Military-Analytics
│
├───Milestone 1 - Data Collection and Preparation
│   ├───Module-1 - Scraping Setup and Execution
│   │       military_raw_data.csv
│   │       scrape_military_metrics.py
│   │
│   └───Module-2 - Data Cleaning and Structuring
│           clean_data.ipynb
│           military_cleaned.csv
│
├───Milestone 2 - KPI Engineering and Tableau Prep
│   ├───Module 3 - KPI Feature Engineering
│   │       generate_kpis.py
│   │       military_final.xlsx
│   │
│   └───Module 4 - Dashboard Planning and Prototyping
│           Coalition builder Wireframe.png
│           Compare powers Wireframe.png
│           Nation overview Wireframe.png
│           Quick stats Wireframe.png
│           quick_stats_prototype.html
│
├───Milestone-3 - Full Dashboard Development
│   ├───Module 5 - Build Quick Stats and Nation Overview Dashboards
│   │       Global_Military_Analytics_Dashboard.pbix
│   │       military_final.xlsx
│   │
│   └───Module 6 - Build Compare Powers and Coalition Builder Dashboards
│           Global_Military_Analytics_Dashboard.pbix
│           military_final.xlsx
│
└───Milestone 4 - Final Review and Delivery
    ├───Module 7 - Testing and Debugging
    │       QA_Checklist.md
    │
    └───Module 8 - Documentation and GitHub Release
            README.md
```

---

# How to Use the Dashboard

## Requirements

To open the dashboard, install:

* Microsoft Power BI Desktop

## Steps

1. Download or clone this repository.
2. Navigate to:

```text
Milestone-3 - Full Dashboard Development
```

3. Open:

```text
Global_Military_Analytics_Dashboard.pbix
```

4. If required, update the dataset source path to the available `military_final.xlsx` file.

5. Use the navigation buttons to move between dashboard pages.

---

# Dashboard Usage

### Quick Stats

Use the Region, Continent, and Alliance filters to explore global military statistics.

### Nation Overview

Select a country to view its complete military profile.

### Compare Powers

Select Country 1 and Country 2 to compare their military capabilities.

### Coalition Builder

Select multiple countries to create a coalition and compare their combined military capabilities against a selected reference country.

---

# Testing and Quality Assurance

The dashboard was tested for:

* Filter functionality
* Country selection
* KPI calculations
* Coalition aggregation
* Country comparison
* Chart responsiveness
* Dashboard navigation
* Data accuracy through manual spot checks
* Layout and labeling issues

All major dashboard functionality passed the final QA testing.

Detailed testing information is available in:

```text
QA_Checklist.md
```

---

# Future Improvements

Possible future improvements include:

* Publishing the Power BI dashboard online
* Adding map-based military visualizations
* Adding historical military ranking trends
* Adding more advanced coalition analysis
* Including additional global economic and geopolitical indicators
* Automated data refresh
* More interactive drill-through functionality

---

# Conclusion

The Unified Military Analytics Dashboard demonstrates a complete end-to-end data analytics workflow.

The project covers:

```text
Web Scraping
→ Data Cleaning
→ Data Structuring
→ KPI Engineering
→ Dashboard Planning
→ Interactive Dashboard Development
→ Testing and Debugging
→ Documentation
```

The final Power BI dashboard provides an interactive platform for exploring, comparing, and analyzing the military capabilities of 145 countries.

---

# Author

**Yaswanth Gunda**

B.Tech Computer Science and Engineering
Data Science Enthusiast

GitHub: [https://github.com/yaswanth0068](https://github.com/yaswanth0068)