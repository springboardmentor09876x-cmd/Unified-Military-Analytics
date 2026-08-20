# Unified Military Analytics and Comparison Dashboard

## Project Overview

**Unified Military Analytics and Comparison Dashboard** is a data analytics and visualization project focused on analyzing global military capabilities for 2025.

The project follows a complete analytics workflow from data collection and web scraping to data cleaning, KPI engineering, interactive Power BI dashboard development, testing, documentation, and GitHub release.

The final Power BI dashboard suite contains four interactive dashboards:

1. **Quick Stats**
2. **Nation Overview**
3. **Compare Powers**
4. **Coalition Builder**

These dashboards allow users to explore global military statistics, analyze an individual country's profile, compare two countries, and evaluate a hypothetical multi-country coalition against a reference country.

---

## Project Objectives

The main objectives of this project are:

- Collect country-level military information from the required source.
- Clean and structure the collected military dataset.
- Create meaningful derived KPIs for military analysis.
- Build interactive dashboards for different levels of analysis.
- Provide filtering and country-selection capabilities.
- Compare military capabilities between two countries.
- Build a hypothetical multi-country coalition and compare it with a reference country.
- Test dashboards for functionality, accuracy, usability, and navigation.
- Maintain complete project documentation and GitHub-ready deliverables.

---

## Project Workflow

```text
Data Collection & Web Scraping
              ↓
Data Cleaning & Structuring
              ↓
KPI / Feature Engineering
              ↓
Dashboard Planning & Prototyping
              ↓
Quick Stats + Nation Overview
              ↓
Compare Powers + Coalition Builder
              ↓
Testing & QA
              ↓
Documentation & GitHub Release
```

---

# Module 1: Data Collection and Web Scraping

## Objective

The first module focuses on collecting country-level military information from the **Global Firepower 2025** source.

The objective is to create a raw dataset containing the military metrics required for further processing, KPI engineering, and dashboard development.

## Data Source

The project uses military information from **Global Firepower 2025**.

The country URLs used for data collection are maintained in the project URL list.

## Scraping Method

The data collection workflow uses Python-based web scraping:

1. Read the predefined country URLs.
2. Send requests to the required Global Firepower pages.
3. Retrieve the HTML content.
4. Parse the HTML using BeautifulSoup.
5. Extract the required country-level military metrics.
6. Organize the extracted information into a structured dataset.
7. Save the collected information as the raw military dataset.

## Technologies Used

- Python
- Requests
- BeautifulSoup
- Pandas

## Main Output

The raw collected dataset is stored as:

```text
military_raw_data.csv
```

This dataset is used as the input for the data cleaning and preparation stage.

---

# Module 2: Data Cleaning and Structuring

## Objective

The second module converts the raw scraped data into a clean and consistent dataset suitable for analysis and visualization.

## Cleaning Process

### Column Standardization

- Standardize column names.
- Remove unnecessary spaces.
- Maintain consistent naming conventions.

### Numeric Data Cleaning

- Remove commas from numerical values.
- Remove currency symbols where required.
- Remove percentage symbols.
- Remove unnecessary units and special characters.
- Convert values into appropriate numeric data types.

### Missing and Invalid Values

- Identify missing values.
- Handle invalid numeric values.
- Check duplicate records.
- Validate the consistency of country-level records.

### Dataset Preparation

After cleaning, the dataset is structured so that each country can be analyzed consistently across military, economic, demographic, and geographical metrics.

---

# Module 3: KPI Feature Engineering

## Objective

The third module focuses on creating derived metrics that provide additional analytical insight beyond the original dataset values.

The project includes the following engineered KPIs.

## 3.1 Power Index Rank Gap

The **Power Index Rank Gap** is calculated from the country's Power Index rank.

```text
Power Index Rank Gap = Rank - 1
```

For example, if a country's Power Index rank is 5, its Power Index Rank Gap is 4.

This derived metric is used in dashboard analysis to represent the adjusted position based on the country's Power Index rank.

## 3.2 Assets per Capita

**Assets per Capita** measures military assets relative to population.

```text
Assets per Capita = Total Military Assets / Population
```

This provides a population-normalized view of military assets.

## 3.3 Budget-to-GDP Ratio

**Budget-to-GDP Ratio** measures defense expenditure relative to the size of the country's economy.

```text
Budget-to-GDP Ratio = (Defense Budget / GDP) × 100
```

This KPI provides an indication of defense spending intensity relative to GDP.

## Purpose of Feature Engineering

The engineered KPIs make the dataset more useful for:

- Country ranking analysis.
- Military capability comparisons.
- Economic comparison.
- Population-normalized analysis.
- Dashboard visualization.

---

# Module 4: Dashboard Planning and Prototyping

## Objective

The fourth module focuses on planning the dashboard structure before final implementation.

The planning stage defines:

- Dashboard layout.
- Navigation flow.
- KPI placement.
- Filter requirements.
- Country selection requirements.
- Comparison requirements.
- Coalition analysis requirements.
- Overall user interaction.

## Dashboard Plan

The final dashboard suite is divided into four analytical areas:

### Quick Stats

Provides a global overview of military capabilities.

### Nation Overview

Provides a detailed profile of a selected country.

### Compare Powers

Provides a side-by-side comparison between two countries.

### Coalition Builder

Provides multi-country coalition analysis against a reference country.

---

# Module 5: Quick Stats and Nation Overview Dashboards

## Objective

Module 5 focuses on building the first two interactive Power BI dashboards:

- Quick Stats
- Nation Overview

## 5.1 Quick Stats Dashboard

The **Quick Stats** dashboard provides a high-level view of global military power.

### KPI Cards

The dashboard contains KPI cards for:

- Total Military Assets
- Total Defense Budget
- Average Superiority Index
- Total Countries

### Top 10 Analysis

The dashboard provides Top 10 visualizations for:

- Countries by Superiority / Power Index.
- Countries by Defense Budget.

### Filters

Interactive filters are provided for:

- Region
- Continent
- Alliance

### Other Visualizations

The dashboard also includes:

- Global military map.
- Alliance distribution.
- Interactive chart selections.
- Dashboard navigation controls.

### Purpose

Quick Stats is designed for fast exploration of global military strength and identification of leading countries by military power and defense spending.

---

## 5.2 Nation Overview Dashboard

The **Nation Overview** dashboard provides detailed analysis of a selected country.

### Country Selection

Users can select a country and view its corresponding military profile.

### KPI Information

The dashboard displays:

- Defense Budget
- Population
- Active Personnel
- Total Military Assets
- Superiority / Power Index
- Military Strength Index

### Analytical Visuals

The dashboard includes visualizations for:

- Military strength.
- Defense budget comparison.
- Power Index Rank Gap.
- Country-level military metrics.

### Country Profile

A country profile section provides detailed information for the selected nation.

### Purpose

Nation Overview allows users to move from a global view to detailed country-level analysis.

---

# Module 6: Compare Powers and Coalition Builder

## Objective

Module 6 focuses on advanced comparison and coalition analysis.

The module contains:

1. Compare Powers
2. Coalition Builder

## 6.1 Compare Powers Dashboard

The **Compare Powers** dashboard allows users to compare two countries side-by-side.

### Country Selection

Users select:

- Country A
- Country B

The comparison updates based on the selected countries.

### Metrics Compared

The dashboard compares:

- Manpower
- Aircraft
- Navy
- Defense Budget
- Superiority / Power Index
- Other relevant KPIs

### Comparison Table

A comparison table provides detailed values for the selected countries.

### Purpose

The dashboard makes it easier to understand the relative military capabilities of two selected countries.

---

## 6.2 Coalition Builder Dashboard

The **Coalition Builder** dashboard allows users to select multiple countries and analyze their combined military capabilities.

### Coalition Selection

Users can select multiple countries to form a hypothetical coalition.

### Coalition Metrics

The dashboard calculates and displays aggregated values such as:

- Coalition Defense Budget
- Coalition Manpower
- Coalition Aircraft
- Coalition Navy

### Reference Country

A reference country can be selected as a comparison point.

The dashboard displays the relevant reference metric and compares it against the coalition.

### Purpose

Coalition Builder demonstrates how combined country-level military metrics can be analyzed as a hypothetical group.

---

# Module 7: Testing and Debugging

## Objective

Module 7 focuses on validating the functionality, accuracy, and usability of the completed dashboards.

A structured QA process was performed across the four dashboards.

## Functional Testing

The following areas were checked:

- Dashboard navigation.
- Region filters.
- Continent filters.
- Alliance filters.
- Country selection.
- Country A and Country B selection.
- Coalition country selection.
- Reference country selection.
- KPI updates.
- Chart updates.

## Visual Testing

The dashboards were checked for:

- Visual loading errors.
- Missing visuals.
- Incorrect labels.
- Incorrect titles.
- Tooltip behavior.
- Number formatting.
- Layout alignment.
- Readability.
- Overlapping objects.
- Unexpected blank areas.

## Data Validation

Manual spot checks were performed to verify that displayed values behaved correctly with the underlying dataset and filters.

Dashboard values were reviewed during the QA process.

## QA Result

The completed dashboard passed the functional and visual QA checks performed during the final review.

---

# Module 8: Documentation and GitHub Release

## Objective

The final module focuses on preparing the project for submission and sharing through GitHub.

## Documentation

The project documentation covers:

- Project overview.
- Data collection method.
- Data preparation.
- KPI definitions.
- Dashboard functionality.
- Dashboard usage instructions.
- Testing and QA.

## README

This README provides a module-wise explanation of the complete project workflow from data collection to final dashboard delivery.

## QA Checklist

The QA checklist records the testing performed on the dashboards and confirms the functionality of filters, navigation, visuals, KPIs, and other dashboard components.

## GitHub Release

The final project files are maintained in the GitHub repository along with:

- Source/data files.
- Dashboard file.
- Documentation.
- README.

The repository provides a central location for accessing the final project deliverables.

---

# Dashboard Usage Guide

## Quick Stats

1. Open the Quick Stats dashboard.
2. Use the Region, Continent, or Alliance filters.
3. Observe the KPI cards and visualizations update.
4. Explore the Top 10 Power Index visualization.
5. Explore the Top 10 Defense Budget visualization.
6. Use the map and alliance distribution for additional analysis.

## Nation Overview

1. Open the Nation Overview dashboard.
2. Select a country.
3. Review the KPI cards.
4. Examine the military strength and defense budget visuals.
5. Review the Power Index Rank Gap.
6. Review the country profile information.

## Compare Powers

1. Open the Compare Powers dashboard.
2. Select Country A.
3. Select Country B.
4. Review the side-by-side military comparison.
5. Compare manpower, aircraft, navy, budget, and relevant KPIs.

## Coalition Builder

1. Open the Coalition Builder dashboard.
2. Select multiple countries.
3. Review the aggregated coalition metrics.
4. Select a reference country.
5. Compare the coalition against the reference country.

---

# How to Open the Power BI Dashboard

## Requirement

Install **Microsoft Power BI Desktop**.

## Steps

1. Download or clone the GitHub repository.
2. Locate the final Power BI `.pbix` file.
3. Open the `.pbix` file using Power BI Desktop.
4. Wait for the report to load.
5. Use the navigation buttons to move between dashboards.

---

# Final Dashboard Suite

| Dashboard | Main Purpose |
|---|---|
| **Quick Stats** | Global military overview |
| **Nation Overview** | Individual country analysis |
| **Compare Powers** | Two-country comparison |
| **Coalition Builder** | Multi-country coalition analysis |

---

# Project Files

Important project files include:

```text
military_raw_data.csv
scrape_military_metrics.py
```

Additional milestone deliverables include the cleaned/processed data, KPI work, Power BI dashboard, documentation, and QA checklist.

---

# Tools and Technologies

### Data Collection

- Python
- Requests
- BeautifulSoup
- Pandas

### Data Processing

- Python
- Pandas
- NumPy

### Dashboard Development

- Microsoft Power BI
- Power Query
- DAX

### Documentation and Version Control

- Markdown
- Git
- GitHub

---

# Conclusion

The **Unified Military Analytics and Comparison Dashboard** provides an interactive platform for analyzing global military capabilities.

The project follows a complete analytics workflow:

**Data Collection → Data Cleaning → KPI Engineering → Dashboard Planning → Dashboard Development → Testing → Documentation**

The four Power BI dashboards provide complementary levels of analysis:

- **Quick Stats** for global military overview.
- **Nation Overview** for detailed country analysis.
- **Compare Powers** for two-country comparison.
- **Coalition Builder** for multi-country coalition analysis.

The project demonstrates the application of web scraping, data preparation, feature engineering, interactive visualization, dashboard design, testing, and documentation to create a complete military analytics solution.

---

# Author

**Taniya**

**Project:** Unified Military Analytics and Comparison Dashboard

**Data Year:** 2025

**Dashboard Platform:** Microsoft Power BI
