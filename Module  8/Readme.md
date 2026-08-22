# Unified Military Analytics

An interactive military data analytics and visualization project for analyzing and comparing military capabilities across countries.

---

## 📌 Project Overview

**Unified Military Analytics** combines country-level **military, economic, demographic, geographic, and alliance information** into a structured analytical dataset and an interactive Tableau dashboard application.

The final dashboard contains four interconnected views:

1. **Quick Stats**
2. **Nation Overview**
3. **Compare Powers**
4. **Coalition Builder**

The complete workflow covers:

**Data Collection → Data Cleaning → KPI Engineering → Dashboard Development → Testing → Documentation → GitHub Release**

---

## 🎯 Project Objectives

The main objectives of this project are to:

* Collect country-level military metrics.
* Clean and standardize the collected data.
* Engineer useful military comparison KPIs.
* Enrich the dataset with region, continent, and alliance information.
* Develop interactive Tableau dashboards.
* Allow users to explore individual countries and compare military powers.
* Support multi-country coalition analysis.
* Provide a clean and shareable GitHub repository.

---

## 📊 Data Collection & Scraping

Military data was collected using the URLs provided for the project.

A Python-based scraping workflow was used to retrieve country-level military metrics from the specified source pages. The collected information was stored in structured data files for further processing.

### Scraping Workflow

1. Use the provided military-data URL list as the source of target URLs.
2. Retrieve the relevant country-level pages.
3. Parse the required military metric blocks.
4. Extract country-level military values.
5. Store the extracted information in CSV format.
6. Retain source HTML when required for debugging or validation.
7. Combine the collected metrics into the raw military dataset.

### Major Data Categories

The dataset includes military and supporting metrics such as:

* Population and manpower
* Active personnel
* Reserve personnel
* Paramilitary personnel
* Military aircraft
* Fighter aircraft
* Attack aircraft
* Transport aircraft
* Helicopters
* Tanks
* Armored fighting vehicles
* Artillery
* Rocket projectors
* Naval fleet
* Aircraft carriers
* Helicopter carriers
* Submarines
* Destroyers
* Frigates
* Corvettes
* Defense budget
* GDP and related economic information
* Region
* Continent
* Alliance information
* Power Index
* Power Index Rank

---

## 🧹 Data Cleaning & Preparation

The raw military dataset was cleaned and prepared for Tableau analysis.

The cleaning process included:

* Removing commas from numeric values
* Removing percentage symbols
* Removing plus signs and unnecessary special characters
* Converting metric fields into numeric formats
* Standardizing column names
* Handling missing and null values
* Standardizing country information
* Integrating region and continent metadata
* Integrating alliance information
* Preparing the final dataset for Tableau

### Prepared Datasets

```text
military_raw_data.csv
military_cleaned.csv
military_final.xlsx
```

---

## 📈 KPI Feature Engineering

The project includes calculated KPIs for military comparison and analysis.

### Power Index Rank Gap

The **Power Index Rank Gap** represents the difference between the Power Index ranks of two selected countries.

### Assets per Capita

Measures military assets relative to population.

**Formula:**

```text
Total Military Assets / Population
```

### Budget-to-GDP Ratio

Measures defense spending relative to national GDP.

**Formula:**

```text
(Defense Budget / GDP) × 100
```

### Additional Comparison KPIs

The project also uses:

* Power Advantage
* Budget Advantage
* Combined Personnel
* Coalition Budget
* Coalition Score

These KPIs support country comparison and coalition analysis.

---

# 📊 Tableau Dashboard

The project contains four interconnected dashboards.

## 1. 🌍 Quick Stats

Provides a high-level overview of military powers.

Key features include:

* Top 10 countries by Power Index
* Dynamic KPI cards
* Region filter
* Continent filter
* Alliance filter
* Interactive charts
* Tooltips for additional information

---

## 2. 🏳️ Nation Overview

Provides a detailed profile of a selected country.

The dashboard includes:

* GDP
* Defense Budget
* Active Personnel
* Military Assets
* Aircraft
* Naval Capabilities
* Power Index
* Power Index Rank

Users can select a country and explore its military and economic profile.

---

## 3. ⚔️ Compare Powers

Allows users to compare two countries side by side.

Users can select:

```text
Country A
Country B
```

The dashboard compares metrics such as:

* Manpower
* Aircraft
* Naval capabilities
* Defense Budget
* Power Index
* Power Index Rank
* Comparison KPIs

Tableau parameters are used for country selection.

---

## 4. 🤝 Coalition Builder

The **Coalition Builder** supports multi-country military analysis.

Users can select multiple countries and examine aggregated coalition metrics such as:

* Combined Personnel
* Combined Defense Budget
* Military Capability
* Coalition-level KPIs
* Coalition Score

This allows users to analyze the combined capabilities of multiple selected countries.

---

# 🎛️ Filters, Parameters & Navigation

The dashboards use interactive controls for analysis.

### Filters

* Region
* Continent
* Alliance
* Country

### Parameters & Selectors

* Country A
* Country B
* Multi-country coalition selection

### Dashboard Navigation

The dashboards are connected through the following navigation flow:

```text
Quick Stats
     ↓
Nation Overview
     ↓
Compare Powers
     ↓
Coalition Builder
```

---

# 🚀 How to Open the Tableau Dashboard

### Prerequisites

* Tableau Desktop
* Project repository
* Final dataset

### Steps

1. Open **Tableau Desktop**.
2. Navigate to the project's `dashboard` folder.
3. Open:

```text
global_military_firepower_2025.twbx
```

4. Allow Tableau to load the workbook and associated data.
5. If Tableau requests a data source, reconnect it to the project's final dataset.
6. Open the dashboard tabs.
7. Test filters, selectors, parameters, tooltips, and navigation.

The workbook can also be prepared for **Tableau Public** publication if required.

---

# 🧭 How to Use the Dashboards

## Quick Stats

1. Open **Quick Stats**.
2. Review the Top 10 military powers.
3. Use Region, Continent, or Alliance filters.
4. Observe how KPI cards and charts update.
5. Hover over visuals for additional information.

## Nation Overview

1. Select a country.
2. Review the country profile.
3. Examine military, economic, personnel, aircraft, and naval metrics.
4. Review Power Index and Power Index Rank.
5. Use tooltips for additional information.

## Compare Powers

1. Select **Country A**.
2. Select **Country B**.
3. Review side-by-side metrics.
4. Compare manpower, aircraft, naval capabilities, budget, Power Index, and KPIs.
5. Use tooltips to inspect detailed values.

## Coalition Builder

1. Select the required countries.
2. Review aggregated coalition metrics.
3. Examine combined personnel and defense budget.
4. Compare the coalition with another coalition or reference country where available.
5. Use dashboard controls and tooltips to explore results.

---

# 📁 Project Structure

```text
Unified-Military-Analytics/
│
├── scripts/
│   ├── scrape_military_metrics.py
│   ├── clean_data.py
│   └── generate_kpis.py
│
├── data/
│   ├── military_raw_data.csv
│   ├── military_cleaned.csv
│   └── military_final.xlsx
│
├── dashboard/
│   └── global_military_firepower_2025.twbx
│
├── docs/
│   ├── QA_Checklist.md
│   └── Dashboard_Usage_Guide.md
│
├── notebooks/
│   └── clean_data.ipynb
│
└── README.md
```

---

# 🛠️ Technologies Used

| Technology           | Purpose                                      |
| -------------------- | -------------------------------------------- |
| **Python**           | Data scraping, cleaning, and KPI preparation |
| **Pandas**           | Data processing                              |
| **BeautifulSoup**    | Web-page parsing                             |
| **Jupyter Notebook** | Data cleaning workflow                       |
| **Microsoft Excel**  | Structured data delivery                     |
| **Tableau Desktop**  | Interactive dashboard development            |
| **GitHub**           | Version control and final release            |

---

# 🧪 Testing & Quality Assurance

The dashboards were reviewed during the Module 7 testing phase.

The QA process covered:

* Dashboard functionality
* Filters
* Parameters and country selectors
* Navigation
* Manual data spot checks
* KPI values
* Tooltips
* Axis labels and values
* Dashboard layout
* Workbook operation

The final QA checklist is available at:

```text
docs/QA_Checklist.md
```

---

# 📦 Final Deliverables

The final project includes:

```text
military_raw_data.csv
military_cleaned.csv
military_final.xlsx
scrape_military_metrics.py
generate_kpis.py
clean_data.ipynb
global_military_firepower_2025.twbx
QA_Checklist.md
Dashboard_Usage_Guide.md
README.md
```

---

# 🔄 Complete Project Workflow

```text
┌──────────────────────┐
│  Data Collection     │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│   Data Cleaning      │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│  KPI Engineering     │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Dashboard Development│
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│      Testing         │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│   Documentation      │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│    GitHub Release    │
└──────────────────────┘
```

---

# 📊 Dashboard Perspectives

The final solution provides four analytical perspectives:

```text
Quick Stats
     ↓
Nation Overview
     ↓
Compare Powers
     ↓
Coalition Builder
```

### Quick Stats

High-level overview of military powers.

### Nation Overview

Detailed country-level military and economic profile.

### Compare Powers

Side-by-side comparison of two selected countries.

### Coalition Builder

Aggregated analysis of multiple selected countries.

---

# 📌 Final Release

The final project is organized for **GitHub sharing and portfolio use**.

The repository separates:

* Source and processed data
* Python scripts
* Tableau dashboard files
* Documentation
* Testing resources

Publishing the dashboard to Tableau Public is optional under the project requirements.

---

# 🏁 Conclusion

**Unified Military Analytics** provides an end-to-end workflow for collecting, preparing, analyzing, and visualizing military data.

The completed workflow is:

```text
Data Collection
      ↓
Data Cleaning
      ↓
KPI Engineering
      ↓
Dashboard Development
      ↓
Testing
      ↓
Documentation
      ↓
GitHub Release
```

The final dashboard provides four complementary analytical views:

```text
Quick Stats → Nation Overview → Compare Powers → Coalition Builder
```

This structure makes the project suitable for **evaluation, GitHub sharing, and portfolio presentation**.
