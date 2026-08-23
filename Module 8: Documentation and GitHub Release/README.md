# 🌍 Unified Military Analytics and Comparison Dashboard

An interactive, multi-page **Streamlit** analytics suite for exploring and comparing global military capabilities across **140+ countries**, built on open-source data scraped from [GlobalFirepower.com](https://www.globalfirepower.com).

---

## 📌 Project Overview

**Unified Military Analytics** is an end-to-end data project — from web scraping to a fully interactive dashboard — designed to analyze and compare global military power using military, economic, manpower, aircraft, naval, and infrastructure-related indicators.

Unlike a single static report, the project unifies **50+ defense and economic indicators** across **four interconnected dashboard modules**, giving users the ability to explore rankings, drill into a single nation's profile, compare two countries head-to-head, or simulate the combined strength of a custom military coalition.

The project follows a complete data pipeline:

```
Data Collection → Data Cleaning → KPI Feature Engineering
→ Dashboard Development → Testing & Debugging → Documentation & GitHub Release
```

---

## 🎯 Objectives

- Analyze global military power using multiple weighted indicators.
- Provide detailed, country-level military profiles.
- Compare the military capabilities of any two countries side-by-side.
- Analyze the combined military capability of a custom multi-country coalition.
- Engineer meaningful KPIs that blend military and economic data.
- Present all findings through a clean, interactive, and professional dashboard suite.

---

## 📊 Dataset

The dashboards run on the cleaned and processed **`military_final.xlsx`** dataset (with a companion **`military_long.xlsx`** for long-format/tidy queries).

### Data Source
Military data was collected from **GlobalFirepower.com** using a pre-defined list of country-specific source links (`links_for_military_data.txt`), scraped with **Requests** and **BeautifulSoup**.

### Indicators Covered
The dataset contains country-level military and economic indicators, including:

| Category | Indicators |
|---|---|
| **Power & Ranking** | Power Index, Power Index Rank |
| **Economy** | GDP, Defense Budget, Total Population |
| **Manpower** | Active Personnel, Reserve Personnel, Paramilitary |
| **Air Power** | Total Military Aircraft, Fighter Aircraft, Attack Aircraft, Transport Aircraft, Trainer Aircraft, Special Mission Aircraft, Tanker Aircraft, Military Helicopters, Attack Helicopters |
| **Land Power** | Tanks, Armored Fighting Vehicles |
| **Naval Power** | Total Naval Fleet |
| **Metadata** | Region, Continent, Alliance (e.g., NATO) |

### Data Pipeline
1. **Data Collection** — Scrape country-level military metrics via `requests` + `BeautifulSoup`.
2. **Data Cleaning** — Strip symbols (`,`, `%`, `+`), convert to numeric types, standardize column names, handle missing values.
3. **Data Structuring** — Export clean wide-format and long-format datasets for downstream use.
4. **KPI Engineering** — Compute derived KPIs and enrich with Region/Continent/Alliance metadata.
5. **Dashboard Development** — Build the four-module Streamlit dashboard suite.
6. **Testing & Debugging** — Validate filters, KPIs, and navigation end-to-end.
7. **Documentation & GitHub Release** — Package scripts, data, and docs for public/portfolio use.

---

## 🧮 KPI Definitions

### 1. Power Index Rank Gap
```
Power Index Rank Gap = GDP Rank − Power Index Rank
```
Identifies the gap between a country's **economic** ranking and its **military power** ranking — a positive gap suggests military strength outpaces economic size, and vice versa.

### 2. Assets per Capita
```
Assets per Capita = Total Assets / Total Population
```
Represents the number of military assets relative to a country's population, normalizing raw asset counts by population size.

### 3. Budget-to-GDP Ratio
```
Budget-to-GDP Ratio = Defense Budget / GDP
```
Represents the proportion of a country's GDP allocated to defense spending.

---

## 🖥️ Dashboard Modules

The dashboard suite consists of **four major sections**, each a dedicated Streamlit page.

### 1️⃣ Quick Stats
A global overview of military capabilities at a glance.
- Top-ranked countries by Power Index, Defense Budget, and military assets
- KPI cards with dynamic, filter-aware values
- World map view of military rank by country
- Filters: **Country, Region, Continent, Alliance**
- Searchable, sortable country data table

### 2️⃣ Nation Overview
A detailed, single-country military and economic profile.
- Power Index & Power Index Rank
- Defense Budget, Active & Reserve Personnel
- Military Aircraft, Helicopters, Tanks, Naval Fleet
- Bar/radar visualizations of key capability metrics
- Contextual tooltips with rank and comparison detail

### 3️⃣ Compare Powers
A side-by-side comparison of any two selected countries.
- Manpower, Aircraft, Naval Fleet, Defense Budget
- Power Index Rank comparison
- Derived KPI comparison (Budget-to-GDP, Assets per Capita, etc.)

### 4️⃣ Coalition Builder
An interactive simulation of combined alliance strength.
- Multi-country selector to build custom coalitions
- Aggregated totals for combined coalition metrics (manpower, aircraft, naval fleet, defense budget)
- Coalition-vs-Coalition and Coalition-vs-Reference-Country comparisons
- Auto-generated coalition strength summary

---

## 🛠️ Technology Stack

| Area | Tools / Libraries |
|---|---|
| **Programming** | Python |
| **Data Collection** | Requests, BeautifulSoup |
| **Data Processing** | Pandas, NumPy, Excel |
| **Dashboard / Visualization** | Streamlit, Plotly |
| **Development & Version Control** | Jupyter Notebook, Git, GitHub |

---

## 🗂️ Project Structure

```
Unified-Military-Analytics/
│
├── Module1-Scrapping and Execution/
│   ├── scrape_military_metrics.py
│   ├── scrape_all_metrics.py
│   ├── links_for_military_data.txt
│   ├── html/                          # raw per-country HTML (debugging)
│   └── data/
│       └── military_raw_data.csv
│
├── Module2-Data Cleaning/
│   ├── clean_data.ipynb
│   ├── README.md
│   └── data/
│       └── military_cleaned.csv
│
├── Module3-KPI Feature Engineering/
│   ├── generate_kpis.py
│   ├── military_final.xlsx
│   ├── military_long.xlsx
│   └── README.md
│
├── Module4-Dashboard Planning and Prototyping/
│   ├── Quick Stats Dashboard.twb
│   ├── Storyboard for Dashboard Layout.pdf
│   └── README.md
│
├── Module5&6-Full Dashboard Development/
│   ├── app.py                         # Quick Stats (entry point)
│   ├── charts.py                      # shared Plotly chart builders
│   ├── utils.py                       # data loading, filtering, KPI helpers
│   ├── requirements.txt
│   ├── pages/
│   │   ├── Nation_Overview.py
│   │   ├── compare_powers.py
│   │   └── coalition_builder.py
│   ├── data/
│   │   ├── military_final.xlsx
│   │   └── military_long.xlsx
│   └── README.md
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
├── .gitignore
└── README.md
```

> **Note:** As part of Module 8 (Documentation & GitHub Release), the final repository is reorganized into four top-level folders — `/scripts`, `/data`, `/dashboard`, and `/docs` — for a clean, portfolio-ready public release, per the project's packaging requirements.

---

## 🧭 Development Milestones

| Milestone | Focus Area | Modules | Metric | Target |
|---|---|---|---|---|
| **1** | Scraping & Cleaning | Module 1–2 | Raw & clean data coverage | ≥ 140 countries, < 2% missing data |
| **2** | KPI Engineering | Module 3–4 | KPI accuracy & format | 5+ KPIs correctly computed |
| **3** | Dashboard Development | Module 5–6 | 4 dashboards built & connected | Full integration, navigation OK |
| **4** | Delivery & QA | Module 7–8 | Final packaging & usability | No bugs, GitHub ready |

### Milestone 1: Data Collection and Preparation (Weeks 1–2)
- **Module 1 — Scraping Setup and Execution:** Scrape 140+ countries' military metrics from GlobalFirepower.com; ≥ 95% URL success rate.
- **Module 2 — Data Cleaning and Structuring:** Clean and standardize the dataset to < 2% missing/null values with no structural errors.

### Milestone 2: KPI Engineering and Dashboard Prep (Weeks 3–4)
- **Module 3 — KPI Feature Engineering:** Compute Power Index Rank Gap, Assets per Capita, and Budget-to-GDP Ratio; enrich with region/continent/alliance metadata.
- **Module 4 — Dashboard Planning and Prototyping:** Wireframe all four dashboards; define filters, buttons, and navigation logic; build an initial working prototype.

### Milestone 3: Full Dashboard Development (Weeks 5–6)
- **Module 5 — Build Quick Stats and Nation Overview:** Top-10 rankings, dynamic KPI cards, region/continent/alliance filters, full country profile visualizations.
- **Module 6 — Build Compare Powers and Coalition Builder:** Two-country side-by-side comparison; multi-country coalition aggregation vs. a reference country; cross-dashboard navigation.

### Milestone 4: Final Review and Delivery (Weeks 7–8)
- **Module 7 — Testing and Debugging:** End-to-end validation of all filters, KPIs, and navigation; manual spot checks of displayed values; layout/tooltip bug fixes.
- **Module 8 — Documentation and GitHub Release:** Final README covering the scraping method, KPI definitions, and usage instructions; clean `/scripts`, `/data`, `/dashboard`, `/docs` project organization; public GitHub release.

---

## ⚙️ How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/springboardmentor09876x-cmd/Unified-Military-Analytics.git
cd Unified-Military-Analytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the dashboard
streamlit run app.py
```

The **Quick Stats** dashboard opens by default; use the sidebar navigation to switch to **Nation Overview**, **Compare Powers**, or **Coalition Builder**.

---

## ✅ Evaluation Criteria Summary

| Focus Area | Metric | Target |
|---|---|---|
| Scraping & Cleaning | Country & data coverage | ≥ 140 countries, < 2% missing data |
| KPI Engineering | KPI accuracy & format | 5+ KPIs correctly computed, loads without transformation |
| Dashboard Development | Integration & navigation | 4 dashboards built and fully connected |
| Delivery & QA | Final packaging & usability | No functional bugs, GitHub-ready repository |

---

## 👩‍💻 Author
Sahana N
Developed as part of the **Infosys Virtual Internship** program.

---

## 📄 License

This project is released for educational and portfolio purposes. Data sourced from [GlobalFirepower.com](https://www.globalfirepower.com) is used under fair-use, open-source research conventions.