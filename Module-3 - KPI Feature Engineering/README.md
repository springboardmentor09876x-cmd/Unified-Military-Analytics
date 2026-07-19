# Module 3 – KPI Feature Engineering

## Overview

This module enriches the cleaned military dataset by integrating external lookup data and generating key performance indicators (KPIs) for analytical visualization.

## Features

- Merged Continent and Region information
- Integrated latest available GDP data
- Classified countries as NATO or Non-NATO
- Standardized country names for accurate merging
- Generated analytical KPIs:
  - Power Index Rank Gap
  - Assets Per Capita
  - Budget-to-GDP Ratio

## KPI Formulas

1. Power Index Rank Gap
Measures how far a country is ranked from the top-ranked military.

Formula:
Power Index Rank Gap = Power Index Rank − 1

2. Assets Per Capita
Measures the number of military assets available per person.

Formula:
Assets Per Capita =
(Total Military Aircraft +
Tanks +
Armored Fighting Vehicles +
Self-Propelled Artillery +
Towed Artillery +
Rocket Projectors +
Total Naval Fleet)
/ Total Population

3. Budget-to-GDP Ratio
Measures defence spending as a percentage of GDP.

Formula:
Budget-to-GDP Ratio (%) =
(Defense Budget USD / GDP USD) × 100

## Output Files

military_final.xlsx – Enriched military dataset with KPIs
military_long.xlsx – Tableau-ready long-format dataset

## Run
python3 generate_kpis.py

## Technologies Used

- Python
- Pandas
- NumPy
- OpenPyXL