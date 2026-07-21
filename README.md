# 🛡️ Unified Military Analytics and Comparison Dashboard

## 📖 Project Overview

The **Unified Military Analytics and Comparison Dashboard** is a data analytics project that collects, processes, analyzes, and visualizes global military power data using publicly available information from **GlobalFirepower**.

The project follows a modular pipeline that includes web scraping, data cleaning, KPI engineering, and dashboard prototyping. The processed data is designed to support interactive military analytics dashboards for comparing countries and analyzing defense capabilities.

This repository currently contains:

- ✅ Module 1 – Web Scraping and Data Collection
- ✅ Module 2 – Data Cleaning and Structuring
- ✅ Module 3 – KPI Feature Engineering
- ✅ Module 4 – Dashboard Planning and Prototyping

---

# 🎯 Objectives

- Collect military data for 140+ countries.
- Build a structured raw dataset.
- Clean and standardize military statistics.
- Engineer meaningful KPIs for military analysis.
- Prepare datasets for dashboard development.
- Design an interactive military analytics dashboard prototype.

---

# 📂 Repository Structure

```
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
│   └── dashboard_planning.ipynb
│
└── README.md
```

---

# 🛠️ Technologies Used

## Programming Language

- Python 3.x

## Python Libraries

- Pandas
- NumPy
- Requests
- BeautifulSoup4
- Plotly
- OpenPyXL
- pathlib
- re

## Development Tools

- Jupyter Notebook
- Git
- GitHub

## Visualization Tools

- Plotly
- Streamlit (Prototype)
- Power BI (Future)
- Tableau (Future)

---

# 📊 Dataset Information

## Source

GlobalFirepower

https://www.globalfirepower.com/

## Dataset Includes

- Country
- Power Index
- GDP
- Defense Budget
- Total Population
- Active Personnel
- Reserve Personnel
- Total Military Aircraft
- Tanks
- Armored Fighting Vehicles
- Artillery
- Rocket Projectors
- Naval Fleet
- Total Military Assets
- Labour Force
- Oil Resources
- Natural Gas Resources
- Coal Resources
- Region
- Continent
- Alliance

**Countries Covered:** 140+

---

# 🚀 Module 1 – Web Scraping and Data Collection

## Description

Module 1 focuses on collecting military statistics from GlobalFirepower using Python web scraping techniques.

## Tasks Performed

- Read country URLs
- Extract military statistics
- Scrape country-wise data
- Store raw dataset
- Export dataset to CSV

## Deliverables

- Military_Data_Scraper_Nagashree.ipynb
- military_raw_data.csv

---

# 🧹 Module 2 – Data Cleaning and Structuring

## Description

Module 2 prepares the raw dataset for analysis by cleaning inconsistent values, standardizing columns, handling missing values, and validating the dataset.

## Tasks Performed

- Removed commas and unwanted symbols
- Removed tabs and newline characters
- Standardized column names
- Converted numeric values
- Removed duplicates
- Handled missing values
- Validated cleaned dataset
- Exported cleaned CSV

## Deliverables

- clean_data.ipynb
- military_cleaned.csv

---

# 📈 Module 3 – KPI Feature Engineering

## Description

Module 3 transforms the cleaned dataset into an analytical dataset by generating KPIs required for military comparison dashboards.

## KPIs Created

- Power Index Rank
- Power Index Rank Gap
- Assets per Capita
- Budget-to-GDP Ratio
- Total Military Assets
- GDP Rank
- NATO Flag

## Additional Processing

- Added Region
- Added Continent
- Added Alliance Information
- Generated Wide Format
- Generated Long Format
- Created KPI Definition Sheet

## Deliverables

- generate_kpis.ipynb
- military_final.xlsx

---

# 📊 Module 4 – Dashboard Planning and Prototyping

## Description

Module 4 focuses on designing and prototyping an interactive military analytics dashboard using the KPI dataset.

## Dashboard Components

- Dashboard Header
- KPI Cards
- Top 10 Countries by Power Index
- Top 10 Defense Budget
- Military Assets by Continent
- Defense Budget vs GDP
- Global Military Power Map
- Active Personnel Analysis

## Deliverables

- dashboard_planning.ipynb

---

# 🔄 Data Processing Workflow

```
GlobalFirepower
        │
        ▼
Web Scraping
        │
        ▼
Raw Dataset
        │
        ▼
Data Cleaning
        │
        ▼
KPI Feature Engineering
        │
        ▼
Dashboard Planning
        │
        ▼
Interactive Military Analytics Dashboard
```

---

# 📈 Features Implemented

## Module 1

- Web scraping
- Automated data extraction
- Structured CSV generation

## Module 2

- Data cleaning
- Standardization
- Numeric conversion
- Missing value handling
- Duplicate removal
- Data validation

## Module 3

- KPI Engineering
- Rank Calculations
- Assets per Capita
- Budget-to-GDP Ratio
- Metadata Enrichment
- Excel Dashboard Dataset

## Module 4

- Dashboard Prototype
- KPI Cards
- Interactive Charts
- Military Analytics Visualization
- Plotly Visualizations

---

# ▶️ Getting Started

## Clone Repository

```bash
git clone https://github.com/springboardmentor09876x-cmd/Unified-Military-Analytics.git
```

## Navigate to Repository

```bash
cd Unified-Military-Analytics
```

## Install Dependencies

```bash
pip install pandas numpy requests beautifulsoup4 plotly openpyxl
```

---

# ▶️ Running the Project

## Module 1

Run:

```
Military_Data_Scraper_Nagashree.ipynb
```

Output

```
military_raw_data.csv
```

---

## Module 2

Run:

```
clean_data.ipynb
```

Output

```
military_cleaned.csv
```

---

## Module 3

Run

```
generate_kpis.ipynb
```

Output

```
military_final.xlsx
```

---

## Module 4

Run

```
dashboard_planning.ipynb
```

Output

Interactive Dashboard Prototype

---

# 📋 Outputs

- military_raw_data.csv
- military_cleaned.csv
- military_final.xlsx
- Dashboard Planning Prototype

---

# 📌 Future Scope

Upcoming modules include:

- Quick Stats Dashboard
- Nation Overview Dashboard
- Compare Powers Dashboard
- Coalition Builder Dashboard
- Dashboard Integration
- Testing and Validation
- Documentation
- GitHub Release

---

# 👩‍💻 Author

**Nagashree K S**

Computer Science and Engineering Student

GitHub:

https://github.com/Nagashreemurthy21

---

# 🙏 Acknowledgements

- GlobalFirepower
- Python Community
- Pandas
- NumPy
- BeautifulSoup
- Plotly
- GitHub

---

# 📄 License

This project is developed for educational and academic purposes as part of the Unified Military Analytics internship project.
