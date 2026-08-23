# 🎯 Unified Military Analytics — Milestone 3: Full Dashboard Development

## 📌 Project Overview

**Milestone 3: Full Dashboard Development** delivers the complete, interactive Streamlit dashboard suite for analyzing and comparing global military capabilities across 140+ countries.

This milestone combines:
- **Module 5 — Quick Stats & Nation Overview**
- **Module 6 — Compare Powers & Coalition Builder**

Together, these four dashboards let users explore country-level military capabilities, compare any two nations head-to-head, simulate the combined strength of custom military coalitions, and gain insight through interactive filters and visualizations — all built on the cleaned, KPI-enriched dataset produced in Milestone 2.

---

## 🚀 Live Deployment

🔗 **Streamlit Dashboard (Live Demo):** [Open Dashboard](https://unified-military-analytics-d9psbq9jmnxwj7qknig9gf.streamlit.app/)

> Click the link above to explore the live Quick Stats, Nation Overview, Compare Powers, and Coalition Builder dashboards directly in your browser — no setup required.
> > ⚠️ **Note:** This app is hosted on Streamlit Community Cloud's free tier, which puts apps to sleep after a period of inactivity. If you see a **"This app has gone to sleep due to inactivity"** screen when you open the link, simply click the **"Yes, get this app back up!"** button — the app will restart in under a minute. This is normal free-tier behaviour, not a bug.

---

## 🖥️ Dashboard Modules

### 1️⃣ Quick Stats (`app.py`)
A global overview of military capability across the entire dataset.
- Dynamic KPI cards (Total Countries, Avg Power Index, Total Defense Budget, Total Aircraft, Tanks, Naval Fleet, Manpower, Best Ranked Country)
- Top-10 rankings by Power Index, Defense Budget, Military Aircraft, and Purchasing Power Parity
- Interactive world map of military rank by country
- Asset breakdown charts (Aircraft, Tanks, Naval Fleet) and a Defense Budget vs. Power Index bubble chart
- Continent and Alliance distribution donut charts
- Cascading filters: Country, Region, Continent, Alliance — with a working Reset Filters control
- Searchable country data table and a full per-country profile lookup

### 2️⃣ Nation Overview (`pages/Nation_Overview.py`)
A detailed, single-country military and economic profile.
- Power Index, Defense Budget, Personnel, Aircraft, Tanks, and Naval Fleet KPI cards
- Full country profile (Continent, Region, Alliance, GDP, Population, Land Area, Coastline, Border Coverage)
- Manpower, Air Power, Land Power, and Naval Power breakdown charts
- A normalized Strategic Capability Profile radar chart
- Economic & Strategic Metrics, Infrastructure, and Natural Resources sections
- Selected country vs. global average comparison
- Rank information across every major capability metric

### 3️⃣ Compare Powers (`pages/compare_powers.py`)
A side-by-side comparison of any two selected countries.
- Power Index Rank, Defense Budget, Manpower, Aircraft, and Naval Fleet compared directly
- Derived KPI comparison (e.g. Budget-to-GDP Ratio)

### 4️⃣ Coalition Builder (`pages/coalition_builder.py`)
An interactive simulator for combined coalition strength.
- Build two custom coalitions (Coalition A / Coalition B) plus a Reference country
- Aggregated KPI comparison across Manpower, Aircraft, Tanks, Naval Fleet, Defense Budget, GDP, and Population
- Power Index Analysis (correctly *averaged*, not summed, across members)
- Military Manpower / Air / Land / Naval Power comparison charts
- Defense Economics with a group-level Budget-to-GDP ratio
- Per-country contribution breakdown within each coalition
- Coalition vs. Reference percentage comparison
- Auto-generated, fully data-driven coalition strength summary
- Full coalition country table

---

## 🛠️ Technology Stack

| Area | Tools / Libraries |
|---|---|
| **Dashboard Framework** | Streamlit |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly |
| **File I/O** | openpyxl (Excel) |
| **Language** | Python |

---

## 🗂️ Project Structure

```
Milestone_3_Full_Dashboard_Development/
│
├── app.py                     # Quick Stats dashboard (entry point)
├── charts.py                  # Shared Plotly chart-building functions
├── utils.py                   # Data loading, filtering, and KPI helper functions
├── requirements.txt           # Python dependencies
│
├── pages/
│   ├── Nation_Overview.py     # Single-country profile dashboard
│   ├── compare_powers.py      # Two-country comparison dashboard
│   └── coalition_builder.py   # Coalition simulator dashboard
│
├── data/
│   ├── military_final.xlsx    # Cleaned, KPI-enriched wide-format dataset
│   └── military_long.xlsx     # Long-format dataset for detailed metric lookups
│
└── README.md                  # This file
```


---

## ⚙️ How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/springboardmentor09876x-cmd/Unified-Military-Analytics.git
cd Unified-Military-Analytics/Milestone_3_Full_Dashboard_Development

# 2. (Recommended) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the dashboard
streamlit run app.py
```

The **Quick Stats** dashboard opens by default at `http://localhost:8501`; use the sidebar to navigate to **Nation Overview**, **Compare Powers**, and **Coalition Builder**.

---

## ✅ Status

- [x] Module 5 — Quick Stats & Nation Overview dashboards built
- [x] Module 6 — Compare Powers & Coalition Builder dashboards built
- [x] All four dashboards cross-navigable via sidebar
- [x] Filters, KPIs, and charts validated against the dataset
- [x] Deployed live on Streamlit Community Cloud

---

## 📎 Related Documentation

- Root `README.md` — full project overview, dataset description, KPI definitions
- `Module 7: Testing and Debugging/` — QA notebook and test results
- `Module 8: Documentation and GitHub Release/` — Dashboard Usage Guide and Project Structure
