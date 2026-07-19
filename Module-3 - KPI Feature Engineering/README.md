# Module 3: KPI Feature Engineering

## Project Overview

This project was developed as part of the Infosys Springboard Virtual Internship – Module 3: KPI Feature Engineering.

The objective of this module is to calculate important military KPIs, enrich the cleaned military dataset with geographical and alliance metadata, and prepare Tableau-ready data in wide and long formats.

## Tasks Completed

- Computed Power Index Rank Gap
- Computed Assets per Capita
- Computed Budget-to-GDP Ratio
- Added region and continent metadata
- Added alliance and NATO membership information
- Created wide and long data formats for Tableau

## KPI Calculations

### 1. Power Index Rank Gap

Compares a country's GDP rank with its military power rank.

**Formula:**

Power Index Rank Gap = GDP Rank - Power Index Rank

### 2. Assets per Capita

Represents the number of military assets available per person.

**Formula:**

Assets per Capita = Total Military Assets / Total Population

Total Military Assets include aircraft, tanks, armored fighting vehicles, artillery, rocket projectors, and naval fleet.

### 3. Budget-to-GDP Ratio

Measures the proportion of nominal GDP allocated to the defense budget.

**Formula:**

Budget-to-GDP Ratio = Defense Budget / Nominal GDP

## Metadata Enrichment

The final dataset includes:

- ISO3 Code
- Region
- Continent
- Alliance
- NATO Flag
- Power Index
- Power Index Rank
- Nominal GDP
- GDP Rank

The NATO flag is represented as:

- 1 = NATO Member
- 0 = Non-NATO Member

## Excel Workbook Structure

The `military_final.xlsx` workbook contains three sheets:

### Wide_Format

Contains one row per country with military data, metadata, and calculated KPIs.

### Long_Format

Contains KPI names and values in separate rows. It is ready to load directly into Tableau without additional transformation.

### KPI_Definitions

Contains the names and formulas of all calculated KPIs.

## Technologies Used

- Python
- Pandas
- NumPy
- OpenPyXL
- Jupyter Notebook
- Microsoft Excel
- Tableau

## Project Structure

    Module-3 - KPI Feature Engineering/
    │
    ├── generate_kpis.py
    ├── military_final.xlsx
    └── README.md

## How to Run

Keep `generate_kpis.py`, `military_cleaned.csv`, and `military_final.xlsx` in the same folder.

Run the following command:

    python generate_kpis.py

The script calculates the KPIs and creates the Tableau-ready Excel workbook.

## Deliverables

- ✅ `military_final.xlsx`
- ✅ `generate_kpis.py`
  
## Evaluation Criteria Covered

- All required KPIs are present and correctly calculated
- Region, continent, and alliance metadata are included
- NATO membership flag is included
- Wide and long formats are available
- Data can be loaded into Tableau without transformation

## Author

**Taniya Chaudhary**

Infosys Springboard Virtual Internship  
Module 3 – KPI Feature Engineering
