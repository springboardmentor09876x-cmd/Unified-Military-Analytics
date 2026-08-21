
# Unified Military Analytics


---

## 📌 Project Overview

Unified Military Analytics is a data-driven analytics and visualization project developed to collect, process, analyze, and visualize global military capabilities using country-level military, defence, economic, demographic, and geographic data.

The project follows an end-to-end analytics workflow, beginning with automated web scraping and data collection, followed by data cleaning, KPI and feature engineering, dashboard development, country comparison, coalition analysis, and final dashboard integration.

The final solution is implemented using **Microsoft Power BI** and consists of four integrated dashboards:

- 📊 **Quick Stats**
- 🌍 **Nation Overview**
- ⚔️ **Compare Powers**
- 🤝 **Coalition Builder**

The dashboard allows users to explore global military statistics, examine individual countries, compare two countries, and evaluate the combined capabilities of multiple countries as a coalition.

---

## 🎯 Project Objectives

- Analyze military capabilities across **140+ countries**.
- Work with a large collection of military, economic, demographic, and geographic indicators.
- Collect country-level information from publicly available sources.
- Automate the data collection process using **Python**.
- Clean, standardize, validate, and structure the collected data.
- Develop meaningful military and economic KPIs.
- Build interactive dashboards using **Power BI**.
- Provide global military statistics through the **Quick Stats** dashboard.
- Provide detailed country-level analysis through **Nation Overview**.
- Enable side-by-side comparison through **Compare Powers**.
- Enable multi-country analysis through **Coalition Builder**.
- Provide interactive filtering using **Region, Continent, Alliance, and country selections**.
- Calculate **Population, GDP, and Land Area Coverage** for selected coalitions.
- Integrate all dashboards through a common navigation system.
- Maintain and document the complete project using **Git and GitHub**.

---

## 🛠️ Technologies and Tools Used

### Programming & Data Processing

- **Python** – Web scraping, data extraction, transformation, and preprocessing
- **Pandas** – Data manipulation and cleaning
- **NumPy** – Numerical processing
- **Requests** – HTTP requests and webpage retrieval
- **BeautifulSoup** – HTML parsing and data extraction
- **Regular Expressions** – Extraction and cleaning of structured values

### Data Preparation

- **Microsoft Excel** – Dataset validation and supplementary data preparation

### Business Intelligence & Visualization

- **Microsoft Power BI** – Dashboard development and interactive visualization
- **DAX** – KPI calculations and analytical measures

### Development & Version Control

- **Google Colab** – Cloud-based Python development and execution
- **Git** – Version control
- **GitHub** – Repository management and documentation

---

## 🔄 Project Workflow

```text
                    Public Data Sources
                           ↓
                    URL Identification
                           ↓
                    Web Scraping
                           ↓
                   Raw Military Data
                           ↓
                Data Cleaning & Validation
                           ↓
               Data Integration & Structuring
                           ↓
                 KPI Feature Engineering
                           ↓
                    Power BI Data Model
                           ↓
                  Dashboard Development
                           ↓
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
   Quick Stats      Nation Overview     Compare Powers
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ↓
                  Coalition Builder
                           ↓
                  Dashboard Integration
                           ↓
                  Testing & Documentation
                           ↓
                     Final Release
````

---

# 📚 Project Modules

## Module 1 — Data Scraping & Collection

The first module focuses on collecting country-level military information from publicly available sources, primarily **Global Firepower**.

Python-based web scraping was implemented using **Requests** and **BeautifulSoup** to retrieve and extract military metrics from predefined URLs.

The collected information was stored as raw structured data and used as the foundation for the subsequent processing stages.

### Main Activities

* Identifying required data sources and URLs
* Sending HTTP requests
* Retrieving webpage content
* Parsing HTML structures
* Extracting required military metrics
* Validating collected information
* Creating the raw military dataset

### Main Deliverables

* Military data source URL list
* Python scraping script
* Raw military dataset
* Supporting scraping and validation resources

---

## Module 2 — Data Cleaning & Preparation

The second module transforms the raw scraped information into a clean and standardized dataset suitable for analysis.

### Main Activities

* Removing unwanted characters and formatting
* Converting textual values into numeric formats
* Standardizing column names
* Handling missing and inconsistent values
* Validating country-level records
* Structuring military metrics
* Preparing the dataset for KPI development

The cleaned dataset serves as the primary analytical dataset for the dashboard development stages.

### Main Deliverables

* Cleaned military dataset
* Data cleaning notebook/script
* Structured analysis-ready dataset

---

## Module 3 — KPI & Feature Engineering

The third module focuses on enriching the cleaned dataset with additional analytical features and calculated indicators.

### Major KPIs

* **Power Index Rank Gap**
* **Assets per Capita**
* **Budget-to-GDP Ratio**

### Additional Metadata

The dataset was enriched with additional country-level information such as:

* **Region**
* **Continent**
* **Alliance**

These fields are used for categorization, filtering, and comparative analysis within the dashboards.

### Main Deliverables

* Final analytical dataset
* KPI generation resources
* Additional metadata and feature fields

---

## Module 4 — Dashboard Planning & Prototyping

The fourth module focuses on designing the structure and user experience of the final dashboard environment.

The dashboard solution was planned around four major analytical views:

1. **Quick Stats**
2. **Nation Overview**
3. **Compare Powers**
4. **Coalition Builder**

### Planning Covered

* Dashboard layout
* KPI placement
* Visualization selection
* Filter requirements
* Country selection
* Comparison logic
* Coalition analysis
* Navigation
* User interactions
* Visual consistency

A prototype was developed to establish the structure and interaction flow before final dashboard integration.

---

## Module 5 — Quick Stats & Nation Overview

### 📊 Quick Stats

Quick Stats provides a high-level overview of global military capabilities and defence-related information.

### Key Features

* Top countries by Power Index
* Dynamic KPI cards
* Defence budget analysis
* Military comparisons
* Regional analysis
* Country-level statistics
* Interactive filters
* Ranking visualizations

The dashboard provides a quick overview of global military capabilities before users move to detailed analytical views.

### 🌍 Nation Overview

Nation Overview provides a detailed profile of a selected country.

### Key Areas

* Military manpower
* Aircraft
* Naval assets
* Defence budget
* Power Index
* Population
* GDP
* Geographic information
* Military rankings
* Supporting charts and visualizations

The dashboard dynamically updates according to the selected country.

---

## Module 6 — Compare Powers & Coalition Builder

### ⚔️ Compare Powers

Compare Powers allows users to select two countries and compare their military capabilities side by side.

### Major Comparison Areas

* Manpower
* Aircraft
* Naval assets
* Defence budget
* Power Score
* Military KPIs
* Other relevant military indicators

The two country selections operate independently, allowing users to create different comparison combinations.

---

### 🤝 Coalition Builder

Coalition Builder extends the comparison concept from individual countries to multiple countries.

Users can select multiple countries as a **coalition** and select a separate **reference country**.

### Key Features

* Multi-country selection
* Reference country selection
* Coalition Power Score
* Combined manpower
* Combined aircraft
* Combined naval assets
* Combined defence budget
* Coalition Strength Distribution
* Coalition vs Reference Country comparison
* Population Coverage
* GDP Coverage
* Land Area Coverage

The coalition metrics respond to the countries selected in the coalition slicer, while the reference-side metrics respond independently to the selected reference country.

This allows users to evaluate different coalition configurations against different reference countries.

---

## 🔗 Dashboard Integration

The completed dashboard environment connects all four analytical views through a common navigation system.

### Integrated Dashboards

1. 📊 **Quick Stats**
2. 🌍 **Nation Overview**
3. ⚔️ **Compare Powers**
4. 🤝 **Coalition Builder**

The navigation bar is consistently placed across the dashboards, allowing users to move between different analytical views easily.

---

## Module 7 — Dashboard Finalization & Integration

The final development stage focuses on bringing all dashboard components together into a unified Power BI environment.

### Major Activities

* Finalizing dashboard layouts
* Adding dashboard titles
* Adding KPI cards
* Finalizing charts and visualizations
* Adding Region and Alliance filters
* Implementing dashboard navigation
* Configuring interactive slicers
* Verifying dashboard interactions
* Validating coalition calculations
* Adding Population and GDP Coverage
* Finalizing Coalition Builder analysis
* Testing visual consistency across dashboards

The completed dashboards were reviewed to ensure that filters and selections correctly affect their respective visualizations.

---

## Module 8 — Documentation & GitHub Release

The final module focuses on preparing the project for submission, sharing, and portfolio presentation.

### Major Activities

* Preparing the final project README
* Documenting the scraping methodology
* Documenting KPI definitions
* Documenting dashboard functionality
* Explaining filters and dashboard interactions
* Organizing project resources
* Finalizing the GitHub repository
* Preparing the final project release

The repository contains the project resources and documentation required to understand the complete development workflow.

---

# 📊 Dashboard Features

## 🔍 Interactive Filters

The dashboards use Power BI slicers and interactive selections to allow users to explore the dataset.

### Available Filters

* 🌎 **Region**
* 🌐 **Continent**
* 🤝 **Alliance**
* 🏳️ **Country Selection** where applicable
* 👥 **Coalition Countries** in Coalition Builder
* 🎯 **Reference Country** in Coalition Builder

Selections dynamically update the relevant KPIs and visualizations.

---

## 📌 Dynamic KPI Cards

KPI cards display values based on the current dashboard selections.

Examples include:

* Military Personnel
* Aircraft
* Naval Assets
* Defence Budget
* Population
* GDP
* Power Score
* Coverage percentages

DAX measures are used to calculate and dynamically update these values.

---

## ⚖️ Country Comparison

The **Compare Powers** dashboard allows users to independently select two countries.

Changing one selected country updates its corresponding metrics while maintaining the comparison with the other selected country.

---

## 🤝 Coalition Analysis

The **Coalition Builder** supports multi-country selection and calculates aggregated values for the selected coalition.

Users can change the coalition countries without changing the independently selected reference country.

This allows different coalition scenarios to be analyzed dynamically.

---

## 🌍 Coverage Analysis

Coalition Builder evaluates the broader demographic, economic, and geographic representation of the selected coalition.

Coverage indicators include:

* 👥 **Population Coverage**
* 💰 **GDP Coverage**
* 🗺️ **Land Area Coverage**

These values represent the proportion of the total dataset represented by the selected coalition.

---

## 💡 Tooltips

Interactive charts provide additional information when users hover over visual elements.

Depending on the visualization, tooltips may display:

* Country name
* Metric value
* Ranking
* Comparative value
* Coalition contribution
* Percentage contribution
* Other relevant information

---

# 📐 KPI Definitions

## Power Index Rank Gap

Represents the difference between the Power Index rankings of selected countries and helps identify their relative military ranking position.

---

## Assets per Capita

Represents the relationship between available military assets and population.

This provides additional context when comparing countries with significantly different population sizes.

---

## Budget-to-GDP Ratio

Represents defence expenditure relative to GDP.

It provides an economic perspective on the level of resources allocated toward defence.

---

## Coalition Power Score

Represents the calculated overall military strength of the selected coalition according to the project's defined methodology.

---

## Population Coverage

Represents the percentage of the total population contained within the project's dataset that is represented by the selected coalition.

---

## GDP Coverage

Represents the percentage of the total GDP contained within the project's dataset that is represented by the selected coalition.

---

## Land Area Coverage

Represents the percentage of the total land area contained within the project's dataset that is represented by the selected coalition.

---

## Coalition Strength Distribution

Represents the relative contribution of each selected country toward the overall military strength of the coalition.

---

# 🖥️ Power BI Dashboard Usage Guide

## How to Open the Power BI Dashboard

### Requirements

To use the dashboard locally, users should have:

* **Microsoft Power BI Desktop**
* Access to the project repository
* The final `.pbix` dashboard file

### Steps

1. Download the final `.pbix` file from the repository.
2. Install Microsoft Power BI Desktop if required.
3. Open the `.pbix` file.
4. Allow the report and visuals to load.
5. Use the navigation bar to move between dashboards.
6. Use the available slicers to filter the data.
7. Select countries for individual analysis or comparison.
8. Use Coalition Builder to select multiple countries.
9. Select a reference country for comparison.
10. Hover over charts and visuals to explore additional information.

---

## How to Navigate the Dashboard

The dashboard contains a common navigation bar that allows users to access all four analytical pages.

```text
Quick Stats
     ↓
Nation Overview
     ↓
Compare Powers
     ↓
Coalition Builder
```

The selected dashboard is visually highlighted.

---

# 📋 Dashboard Suite

| Dashboard             | Purpose                                                                      |
| --------------------- | ---------------------------------------------------------------------------- |
| **Quick Stats**       | Global overview of military strength, rankings, KPIs, and defence statistics |
| **Nation Overview**   | Detailed profile and analysis of an individual country                       |
| **Compare Powers**    | Side-by-side comparison between two selected countries                       |
| **Coalition Builder** | Combined analysis of selected countries compared against a reference country |

---

# 📁 Project Structure

```text
Unified-Military-Analytics/
│
├── Module 1/
│   ├── Data Collection & Scraping
│   └── Raw Dataset
│
├── Module 2/
│   ├── Data Cleaning
│   └── Cleaned Dataset
│
├── Module 3/
│   ├── KPI & Feature Engineering
│   └── Final Analytical Dataset
│
├── Module 4/
│   └── Dashboard Planning & Prototype
│
├── Module 5/
│   ├── Quick Stats
│   └── Nation Overview
│
├── Module 6/
│   ├── Compare Powers
│   └── Coalition Builder
│
├── Module 7/
│   └── Dashboard Finalization & Integration
│
├── Module 8/
│   └── Documentation & GitHub Release
│
└── README.md
```

---

# 🚀 Final Release

The final release represents the completed Unified Military Analytics solution.

### Final Dashboard Environment

* 📊 **Quick Stats**
* 🌍 **Nation Overview**
* ⚔️ **Compare Powers**
* 🤝 **Coalition Builder**

### Final Release Includes

* Processed military dataset
* Data collection resources
* Data cleaning resources
* KPI and feature engineering resources
* Power BI dashboard
* Interactive slicers
* Dynamic KPI cards
* Country comparison functionality
* Coalition analysis
* Population Coverage
* GDP Coverage
* Land Area Coverage
* Coalition Strength Distribution
* Dashboard navigation
* Project documentation

The final Power BI report represents the integrated dashboard solution developed throughout the project milestones.

---

# 📚 GitHub Repository

The GitHub repository contains the resources required to understand the complete project workflow.

It includes the relevant:

* Data files
* Python scripts
* Processing resources
* Dashboard files
* Documentation

Git and GitHub are used to maintain project versions and organize the final release.

---

# 🏁 Conclusion

Unified Military Analytics provides an end-to-end data analytics and business intelligence solution for exploring global military capabilities.

The project combines **web scraping, data cleaning, data integration, KPI engineering, DAX-based calculations, and interactive Power BI visualization** into a unified analytical platform.

The completed dashboard suite allows users to move from global-level statistics to detailed country analysis, two-country comparison, and multi-country coalition analysis.

The project demonstrates practical implementation of:

* Data collection
* Web scraping
* Data preprocessing
* Data integration
* Feature engineering
* KPI development
* DAX
* Business intelligence
* Interactive dashboard development
* Data visualization
* Git and GitHub-based project management

The final solution provides a structured and interactive platform for analyzing and comparing global military capabilities.

```


