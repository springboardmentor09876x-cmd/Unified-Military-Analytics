# Project Structure

## Unified Military Analytics and Comparison Dashboard

This document describes the organization of the Unified Military Analytics project and the purpose of each module and major file.

The project follows a modular workflow covering data collection, data cleaning, KPI engineering, dashboard prototyping, dashboard development, testing, and final documentation.

---

## Repository Structure

```text
Unified-Military-Analytics/
│
├── Module1-Scrapping and execution/
│   ├── Military_Data_Scraper_Nagashree.ipynb
│   └── military_raw_data.csv
│
├── Module2-Data cleaning/
│   ├── clean_data.ipynb
│   └── military_cleaned.csv
│
├── Module3-KPI Feature Engineering/
│   ├── generate_kpis.ipynb
│   └── military_final.xlsx
│
├── Module4-Dashboard Planning and Prototyping/
│   ├── .streamlit/
│   ├── assets/
│   ├── README.md
│   ├── Screenshot 2026-07-27 203153.png
│   ├── Screenshot 2026-07-27 203202.png
│   ├── Screenshot 2026-07-27 203210.png
│   ├── Screenshot 2026-07-27 203220.png
│   ├── app.py
│   ├── military_final.xlsx
│   └── requirements.txt
│
├── Module5-Build Quick Stats and Nation Overview Dashboards/
│   ├── README.md
│   ├── dashboard_application.py
│   ├── military_final.xlsx
│   └── requirements.txt
│
├── Module6-Build Compare Powers and Coalition Builder/
│   ├── data/
│   │   └── military_final.xlsx
│   ├── README.md
│   └── app.py
│
├── Module7-Testing and Debugging/
│   ├── Testing_and_Debugging.ipynb
│   └── QA_Test_Results.xlsx
│
└── Module8-Documentation and GitHub Release/
    ├── README.md
    ├── Dashboard_Usage_Guide.md
    └── Project_Structure.md
```

---

# Module 1 – Scrapping and Execution

### Purpose

Module 1 focuses on collecting country-level military information from GlobalFirepower using Python web-scraping techniques.

### Files

#### `Military_Data_Scraper_Nagashree.ipynb`

Jupyter Notebook containing the web-scraping implementation.

It collects military statistics for the countries included in the project.

#### `military_raw_data.csv`

Raw dataset generated from the scraping process.

The repository documentation identifies Module 1 as the web-scraping and data-collection stage and lists these two files as its deliverables.

---

# Module 2 – Data Cleaning

### Purpose

Module 2 prepares the raw military dataset for further analysis.

The cleaning process includes:

* Removing unwanted symbols
* Removing commas and formatting characters
* Standardizing column names
* Converting numeric values
* Removing duplicates
* Handling missing values
* Validating the cleaned dataset

### Files

#### `clean_data.ipynb`

Jupyter Notebook containing the data-cleaning and validation operations.

#### `military_cleaned.csv`

Cleaned and structured military dataset produced from the raw data.

These are the files currently present in the Module 2 folder.

---

# Module 3 – KPI Feature Engineering

### Purpose

Module 3 converts the cleaned dataset into an analytical dataset by generating KPIs and additional metadata required for military comparison.

### KPIs

The project generates:

* Power Index Rank
* Power Index Rank Gap
* Assets per Capita
* Budget-to-GDP Ratio
* Total Military Assets
* GDP Rank
* NATO Flag

Additional metadata includes:

* Region
* Continent
* Alliance information

The module also generates Wide Format and Long Format data and includes KPI definitions.

### Files

#### `generate_kpis.ipynb`

Notebook containing the KPI feature-engineering process.

#### `military_final.xlsx`

Final analytical dataset used by the dashboard modules.

---

# Module 4 – Dashboard Planning and Prototyping

### Purpose

Module 4 focuses on designing and prototyping the interactive military analytics dashboard.

The prototype includes dashboard elements such as:

* KPI cards
* Top countries by Power Index
* Defense Budget analysis
* Military asset analysis
* Interactive visualizations
* Country/region exploration

### Files and Folders

#### `.streamlit/`

Contains Streamlit configuration used by the dashboard prototype.

#### `assets/`

Contains dashboard assets used by the application.

#### `app.py`

Main Streamlit application for the dashboard prototype.

#### `military_final.xlsx`

Dataset used by the prototype.

#### `requirements.txt`

Python dependencies required to run the prototype.

#### `README.md`

Documentation for the Module 4 dashboard.

#### Screenshot files

```text
Screenshot 2026-07-27 203153.png
Screenshot 2026-07-27 203202.png
Screenshot 2026-07-27 203210.png
Screenshot 2026-07-27 203220.png
```

These provide visual references for the dashboard prototype.

The current GitHub folder contains these files and folders.

---

# Module 5 – Quick Stats and Nation Overview

### Purpose

Module 5 develops an interactive Streamlit dashboard for exploring global military capabilities and detailed country-level information.

The dashboard includes:

* Quick statistics
* Nation Overview
* KPI cards
* Global Power Index analysis
* Military aircraft analysis
* Military capability radar
* Defense Budget analysis
* Active Personnel analysis
* Continent-wise military distribution
* Interactive filters
* Filtered dataset download

### Files

#### `dashboard_application.py`

Main Streamlit dashboard application.

#### `military_final.xlsx`

Analytical military dataset used by the dashboard.

#### `requirements.txt`

Required Python dependencies.

#### `README.md`

Module 5 documentation and usage instructions.

The current repository contains exactly these four files in Module 5.

---

# Module 6 – Compare Powers and Coalition Builder

### Purpose

Module 6 extends the dashboard with interactive military comparison and coalition analysis.

It is implemented using Python, Streamlit, Pandas and Plotly.

### Dashboard Sections

#### Quick Stats

Provides:

* Region filter
* Continent filter
* Alliance filter
* Country filter
* Power Index Rank
* Defense Budget
* Budget-to-GDP Ratio
* Power Index Rank Gap
* Defense budget analysis
* Power Index ranking

#### Nation Overview

Provides detailed country information including:

* Region
* Continent
* Alliance
* NATO status
* Power Index
* Power Index Rank
* Defense Budget
* Budget-to-GDP Ratio
* Assets per Capita
* Major military assets
* Air power
* Military personnel
* Economic strength

#### Compare Power

Allows two countries to be compared using:

* Power Index Rank
* Defense Budget
* Active Personnel
* Military Aircraft
* Naval Fleet

#### Coalition Builder

Allows multiple countries to be selected and combined into a military coalition.

Coalition metrics include:

* Total Defense Budget
* Total Active Personnel
* Total Aircraft
* Total Naval Fleet

The coalition can also be compared with a selected reference country.

### Files

```text
Module6-Build Compare Powers and Coalition Builder/
│
├── app.py
├── README.md
└── data/
    └── military_final.xlsx
```

---

# Module 7 – Testing and Debugging

### Purpose

Module 7 validates the quality and functionality of the developed dashboard and analytical dataset.

Testing covers:

* Dataset size
* Duplicate countries
* Missing values
* Required columns
* Numeric values
* KPI calculations
* Region filtering
* Continent filtering
* Alliance filtering
* Country selection
* Nation Overview
* Compare Powers
* Coalition Builder
* Aircraft data
* Personnel data

### Files

#### `Testing_and_Debugging.ipynb`

Notebook containing automated testing and validation procedures.

#### `QA_Test_Results.xlsx`

Excel file containing the final QA test results generated by the testing notebook.

The project specification defines Module 7 as the testing/debugging stage and requires a debugged/polished deliverable and QA checklist.

---

# Module 8 – Documentation and GitHub Release

### Purpose

Module 8 provides final documentation and prepares the project for GitHub sharing and portfolio use.

### Files

#### `README.md`

Final documentation describing:

* Project overview
* Dataset
* Data source
* Data-processing workflow
* KPI definitions
* Dashboard modules
* Technologies
* Installation
* Usage
* Testing
* Project structure
* GitHub repository

#### `Dashboard_Usage_Guide.md`

Provides instructions for using:

* Quick Stats
* Nation Overview
* Compare Powers
* Coalition Builder
* Filters
* Country selection
* Coalition selection
* KPI interpretation

#### `Project_Structure.md`

This document.

It explains the purpose and organization of all project modules and major files.

---

# Overall Data Workflow

```text
GlobalFirepower
       │
       ▼
Module 1
Web Scraping
       │
       ▼
military_raw_data.csv
       │
       ▼
Module 2
Data Cleaning
       │
       ▼
military_cleaned.csv
       │
       ▼
Module 3
KPI Feature Engineering
       │
       ▼
military_final.xlsx
       │
       ▼
Module 4
Dashboard Planning & Prototype
       │
       ▼
Module 5
Quick Stats & Nation Overview
       │
       ▼
Module 6
Compare Powers & Coalition Builder
       │
       ▼
Module 7
Testing & Debugging
       │
       ▼
Module 8
Documentation & GitHub Release
```

---

# Technology Stack

### Programming

* Python

### Data Collection

* Requests
* BeautifulSoup4

### Data Processing

* Pandas
* NumPy
* OpenPyXL

### Visualization

* Plotly
* Streamlit
* Matplotlib
* Seaborn

### Development

* Jupyter Notebook
* Git
* GitHub

---

# Dataset

The project uses military data sourced from GlobalFirepower.

The dataset covers 140+ countries and includes military, economic, manpower, aircraft, land-force and naval indicators.

The final analytical dataset is:

```text
military_final.xlsx
```

---

# Final Project Status

Modules 1–6 contain the data pipeline and dashboard development work currently present in the NAGASHREE branch.

Module 7 contains testing and quality assurance.

Module 8 contains final documentation and GitHub-release documentation.

The project therefore follows the complete workflow:

```text
Data Collection
      ↓
Data Cleaning
      ↓
KPI Engineering
      ↓
Dashboard Prototype
      ↓
Dashboard Development
      ↓
Testing
      ↓
Documentation
      ↓
GitHub Release
```
