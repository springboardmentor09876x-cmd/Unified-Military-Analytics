# 🛡️ Unified Military Analytics and Comparison Dashboard

## 📖 Project Overview

The **Unified Military Analytics and Comparison Dashboard** is a data analytics project designed to collect, process, and prepare global military data for visualization and comparison. The project uses publicly available data from **GlobalFirepower** to build a structured dataset that will later be used for KPI engineering and interactive dashboards.

This repository currently contains the implementation of:

- ✅ Module 1 – Web Scraping and Data Collection
- ✅ Module 2 – Data Cleaning and Structuring

---

# 🎯 Objectives

- Collect military data for 140+ countries.
- Build a structured raw dataset.
- Clean and standardize the collected data.
- Prepare the dataset for KPI engineering.
- Enable future dashboard development using Power BI/Tableau.

---

# 📂 Repository Structure

```
Unified-Military-Analytics/
│
├── scrape_military_metrics.ipynb
├── military_raw_data.csv
├── clean_data.ipynb
├── military_cleaned.csv
├── README.md
└── requirements.txt
```

---

# 🛠️ Technologies Used

### Programming Language
- Python 3.x

### Libraries
- Pandas
- NumPy
- Requests
- BeautifulSoup4
- Regular Expressions (re)
- pathlib

### Development Tools
- Jupyter Notebook
- Git
- GitHub

### Visualization (Upcoming Modules)
- Power BI
- Tableau

---

# 📊 Dataset Information

### Source
GlobalFirepower (https://www.globalfirepower.com/)

### Dataset Includes

- Country
- Power Index
- Population
- Military Manpower
- Active Personnel
- Reserve Personnel
- Aircraft
- Tanks
- Armored Fighting Vehicles
- Naval Fleet
- Defense Budget
- GDP
- Labour Force
- Oil Resources
- Natural Gas Resources
- Coal Resources
- Geographic Information
- Continent
- Region
- Alliance

**Countries Covered:** 140+

---

# 🚀 Module 1 – Web Scraping and Data Collection

## Description

Module 1 focuses on collecting military statistics from GlobalFirepower using Python web scraping techniques. The extracted information is stored in a structured CSV file for further processing.

### Tasks Performed

- Read country URLs
- Scrape military statistics
- Extract country-wise metrics
- Store raw dataset
- Export to CSV

### Deliverables

- `scrape_military_metrics.ipynb`
- `military_raw_data.csv`

---

# 🧹 Module 2 – Data Cleaning and Structuring

## Description

Module 2 prepares the raw dataset for analysis by cleaning inconsistent values, standardizing column names, handling missing values, and validating the final dataset.

### Tasks Performed

- Removed commas, percentage symbols, currency symbols, and unwanted characters
- Removed tabs, newline characters, and extra spaces
- Standardized column names
- Converted numeric values into appropriate data types
- Handled missing values
- Removed duplicate records
- Validated the cleaned dataset
- Generated a cleaned CSV file

### Deliverables

- `clean_data.ipynb`
- `military_cleaned.csv`

---

# 🔄 Data Processing Workflow

```
GlobalFirepower
        │
        ▼
Web Scraping
        │
        ▼
military_raw_data.csv
        │
        ▼
Data Cleaning
        │
        ▼
Column Standardization
        │
        ▼
Missing Value Handling
        │
        ▼
Data Validation
        │
        ▼
military_cleaned.csv
```

---

# 📈 Features Implemented

### Module 1

- Web scraping using Python
- Automatic data extraction
- Structured CSV generation

### Module 2

- Data cleaning
- Column standardization
- Numeric conversion
- Missing value handling
- Duplicate removal
- Dataset validation

---

# ▶️ Getting Started

## Clone the Repository

```bash
git clone https://github.com/<your-username>/Unified-Military-Analytics.git
```

## Navigate to the Project Folder

```bash
cd Unified-Military-Analytics
```

## Install Required Libraries

```bash
pip install pandas numpy requests beautifulsoup4
```

---

# ▶️ Running the Project

## Module 1 – Web Scraping

Open and run:

```
scrape_military_metrics.ipynb
```

Output:

```
military_raw_data.csv
```

---

## Module 2 – Data Cleaning

Open and run:

```
clean_data.ipynb
```

Output:

```
military_cleaned.csv
```

---

# 📋 Outputs

After running the notebooks, the following files are generated:

- `military_raw_data.csv`
- `military_cleaned.csv`

---

# 📌 Future Scope

The upcoming modules of this project include:

- KPI Feature Engineering
- Dashboard Planning
- Quick Stats Dashboard
- Nation Overview Dashboard
- Compare Powers Dashboard
- Coalition Builder Dashboard
- Testing and Validation
- Documentation and GitHub Packaging

---

# 👩‍💻 Author

**Nagashree K S**

Computer Science and Engineering Student

GitHub: https://github.com/Nagashreemurthy21

---

# 🙏 Acknowledgements

- GlobalFirepower
- Python Community
- Pandas
- NumPy
- BeautifulSoup
- GitHub

---

# 📄 License

This project is created for educational and academic purposes.
