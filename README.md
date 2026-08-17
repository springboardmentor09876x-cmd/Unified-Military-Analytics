# 🛡️ Unified Military Analytics and Comparison Dashboard

## 📖 Project Overview

The **Unified Military Analytics and Comparison Dashboard** is a data analytics project designed to collect, clean, analyze, and visualize global military power data.

The project uses publicly available military information from **GlobalFirepower** and processes country-level military, economic, manpower, aircraft, land-force, and naval indicators.

The project follows a modular data analytics pipeline:

**Web Scraping → Data Cleaning → KPI Engineering → Dashboard Prototyping → Dashboard Development → Testing → Documentation**

The final system provides interactive dashboards for exploring military capabilities, viewing individual country profiles, comparing two countries, and analyzing combined military strength through coalition analysis.

---

# 🎯 Project Objectives

* Collect military data for 140+ countries.
* Build a structured raw military dataset.
* Clean and standardize the collected data.
* Engineer meaningful military and economic KPIs.
* Develop interactive military analytics dashboards.
* Provide country-level military analysis.
* Compare the capabilities of two countries.
* Analyze combined capabilities of multiple countries.
* Validate the dataset and dashboard calculations.
* Package the complete project for GitHub and portfolio use.

---

# 📊 Dataset

## Data Source

The primary military data source is **GlobalFirepower**.

The dataset contains country-level military and economic indicators covering **140+ countries**.

## Major Indicators

The dataset includes indicators such as:

* Country
* Power Index
* Power Index Rank
* GDP
* GDP Rank
* Defense Budget
* Total Population
* Active Personnel
* Reserve Personnel
* Paramilitary
* Total Military Aircraft
* Fighter Aircraft
* Attack Aircraft
* Transport Aircraft
* Trainer Aircraft
* Special Mission Aircraft
* Tanker Aircraft
* Military Helicopters
* Attack Helicopters
* Tanks
* Armored Fighting Vehicles
* Total Naval Fleet
* Total Military Assets
* Region
* Continent
* Alliance
* NATO Flag

---

# 📈 Key Performance Indicators

The project generates several KPIs for military analysis.

## Power Index Rank Gap

The Power Index Rank Gap represents the difference between economic ranking and military power ranking.

```text
Power Index Rank Gap = GDP Rank - Power Index Rank
```

## Assets per Capita

Assets per Capita represents military assets relative to the country's population.

```text
Assets per Capita = Total Military Assets / Total Population
```

## Budget-to-GDP Ratio

Budget-to-GDP Ratio represents defense spending relative to GDP.

```text
Budget-to-GDP Ratio = Defense Budget / GDP
```

Other engineered fields include:

* Total Military Assets
* GDP Rank
* NATO Flag
* Region
* Continent
* Alliance

---

# 📂 Project Structure

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
├── Module8-Documentation and GitHub Release/
│   ├── README.md
│   ├── Dashboard_Usage_Guide.md
│   └── Project_Structure.md
│
└── README.md
```

---

# 🔹 Module 1 – Scraping and Execution

Module 1 focuses on collecting country-level military statistics using Python web-scraping techniques.

### Tasks

* Read country-specific URLs.
* Access military data pages.
* Extract country-level military metrics.
* Parse metric values.
* Store the collected information.
* Generate the raw dataset.

### Files

```text
Military_Data_Scraper_Nagashree.ipynb
military_raw_data.csv
```

---

# 🔹 Module 2 – Data Cleaning

Module 2 prepares the scraped dataset for analysis.

### Tasks

* Remove commas and unwanted symbols.
* Remove tabs and newline characters.
* Standardize column names.
* Convert numerical fields.
* Handle missing values.
* Remove duplicate records.
* Validate the cleaned dataset.
* Export the cleaned data.

### Files

```text
clean_data.ipynb
military_cleaned.csv
```

---

# 🔹 Module 3 – KPI Feature Engineering

Module 3 transforms the cleaned dataset into an analytical dataset.

### KPIs Created

* Power Index Rank
* Power Index Rank Gap
* Assets per Capita
* Budget-to-GDP Ratio
* Total Military Assets
* GDP Rank
* NATO Flag

### Additional Processing

* Region enrichment
* Continent enrichment
* Alliance information
* Wide-format dataset
* Long-format dataset
* KPI definition sheet

### Files

```text
generate_kpis.ipynb
military_final.xlsx
```

---

# 🔹 Module 4 – Dashboard Planning and Prototyping

Module 4 focuses on dashboard design and prototyping using the KPI dataset.

### Dashboard Components

* Dashboard header
* KPI cards
* Top 10 countries by Power Index
* Top 10 countries by Defense Budget
* Military assets by continent
* Defense Budget vs GDP
* Global military power visualization
* Active Personnel analysis

The module contains the Streamlit prototype, supporting assets, screenshots, requirements, and dataset.

### Main Files

```text
app.py
military_final.xlsx
requirements.txt
README.md
```

---

# 🔹 Module 5 – Quick Stats and Nation Overview

Module 5 develops the first major interactive dashboard components.

## Quick Stats

Provides an overview of global military capabilities using:

* Power Index
* Defense Budget
* Military Personnel
* Military Aircraft
* Naval Fleet
* Country rankings
* Interactive filters

## Nation Overview

Provides detailed country-level analysis including:

* Power Index
* Power Index Rank
* Defense Budget
* Active Personnel
* Reserve Personnel
* Aircraft
* Helicopters
* Tanks
* Naval capabilities
* Economic indicators

### Files

```text
dashboard_application.py
military_final.xlsx
requirements.txt
README.md
```

---

# 🔹 Module 6 – Compare Powers and Coalition Builder

Module 6 extends the dashboard with advanced comparison features.

## Quick Stats

Users can explore military statistics using filters such as:

* Region
* Continent
* Alliance
* Country

## Nation Overview

Users can select an individual country and examine its:

* Military ranking
* Defense budget
* Personnel
* Aircraft
* Naval fleet
* Military assets
* Economic indicators

## Compare Powers

Allows users to compare two countries side-by-side.

### Comparison Metrics

* Power Index Rank
* Defense Budget
* Active Personnel
* Military Aircraft
* Naval Fleet

## Coalition Builder

Allows users to select multiple countries and calculate combined military capabilities.

### Coalition Metrics

* Combined Defense Budget
* Combined Active Personnel
* Combined Military Aircraft
* Combined Naval Fleet

The coalition can also be compared against a selected reference country.

### Files

```text
app.py
README.md
data/
└── military_final.xlsx
```

---

# 🔹 Module 7 – Testing and Debugging

Module 7 validates the quality of the dataset, KPIs, and dashboard-related calculations.

### Testing Includes

* Dataset size validation
* Duplicate country validation
* Missing-value validation
* Required-column validation
* Numeric data validation
* Power Index Rank Gap validation
* Assets per Capita validation
* Budget-to-GDP Ratio validation
* Region filter testing
* Continent filter testing
* Alliance filter testing
* Country selection testing
* Nation Overview testing
* Compare Powers testing
* Coalition Builder testing
* Aircraft data validation
* Personnel data validation

### Files

```text
Testing_and_Debugging.ipynb
QA_Test_Results.xlsx
```

The QA Excel file is generated from the testing notebook and records the final testing status.

---

# 🔹 Module 8 – Documentation and GitHub Release

Module 8 contains the final project documentation and release materials.

### Documentation Includes

* Project overview
* Data source
* Data processing workflow
* KPI definitions
* Dashboard descriptions
* Dashboard usage instructions
* Project structure
* Testing information
* Setup and execution instructions

### Files

```text
README.md
Dashboard_Usage_Guide.md
Project_Structure.md
```

---

# 🔄 Complete Data Processing Workflow

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
Dashboard Planning & Prototyping
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

# 🛠️ Technology Stack

## Programming

* Python 3.x

## Data Collection

* Requests
* BeautifulSoup4

## Data Processing

* Pandas
* NumPy
* OpenPyXL
* Regular Expressions
* pathlib

## Visualization

* Plotly
* Streamlit
* Matplotlib
* Seaborn

## Development

* Jupyter Notebook
* Git
* GitHub

---

# ▶️ Getting Started

## Clone the Repository

```bash
git clone https://github.com/springboardmentor09876x-cmd/Unified-Military-Analytics.git
```

## Navigate to the Repository

```bash
cd Unified-Military-Analytics
```

## Install Dependencies

```bash
pip install pandas numpy requests beautifulsoup4 plotly openpyxl streamlit
```

Additional dependencies can be installed using the `requirements.txt` file available in the dashboard modules.

---

# ▶️ Running the Project

## Module 1

Open:

```text
Module1-Scrapping and execution/
Military_Data_Scraper_Nagashree.ipynb
```

Output:

```text
military_raw_data.csv
```

## Module 2

Open:

```text
Module2-Data cleaning/
clean_data.ipynb
```

Output:

```text
military_cleaned.csv
```

## Module 3

Open:

```text
Module3-KPI Feature Engineering/
generate_kpis.ipynb
```

Output:

```text
military_final.xlsx
```

## Module 4

Navigate to:

```text
Module4-Dashboard Planning and Prototyping/
```

Run:

```bash
streamlit run app.py
```

## Module 5

Navigate to:

```text
Module5-Build Quick Stats and Nation Overview Dashboards/
```

Run:

```bash
streamlit run dashboard_application.py
```

## Module 6

Navigate to:

```text
Module6-Build Compare Powers and Coalition Builder/
```

Run:

```bash
streamlit run app.py
```

---

# 🧪 Testing

The project includes a dedicated testing stage in Module 7.

The testing notebook validates:

* Dataset quality
* Data structure
* KPI calculations
* Dashboard filters
* Country selection
* Comparison functionality
* Coalition calculations
* Military data consistency

The final test results are exported to:

```text
QA_Test_Results.xlsx
```

---

# 📊 Dashboard Features

The complete dashboard suite provides:

* Global military statistics
* Country-level military profiles
* Power Index rankings
* Defense Budget analysis
* Personnel analysis
* Aircraft analysis
* Naval capability analysis
* Country filtering
* Region filtering
* Continent filtering
* Alliance filtering
* Two-country comparison
* Multi-country coalition analysis
* Reference-country comparison
* Interactive visualizations

---

# 📌 Project Outputs

The main project outputs include:

```text
military_raw_data.csv
military_cleaned.csv
military_final.xlsx
Testing_and_Debugging.ipynb
QA_Test_Results.xlsx
Dashboard Applications
Dashboard Documentation
```

---

# 🚀 Future Enhancements

Possible future improvements include:

* Automated data refresh
* Additional years of military data
* Historical military trend analysis
* Predictive analytics
* Advanced country comparison
* Additional military KPIs
* Interactive geographical maps
* More detailed coalition analysis
* Automated dashboard deployment
* Real-time or scheduled data updates

---

# 👩‍💻 Author

**Nagashree K S**

Computer Science and Engineering Student

---

# 🙏 Acknowledgements

* GlobalFirepower
* Python Community
* Pandas
* NumPy
* BeautifulSoup
* Plotly
* Streamlit
* GitHub

---

# 📄 License

This project is developed for educational and academic purposes as part of the Unified Military Analytics internship project.
