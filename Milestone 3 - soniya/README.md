# Unified Military Analytics and Comparison Dashboard

An interactive dashboard suite for analyzing global military power in 2026, built with
Python and Streamlit, using open-source defense data from
[GlobalFirepower.com](https://www.globalfirepower.com) (145 countries, 60+ indicators).

## What it does

Four cross-linked modules let you explore, compare, and simulate military strength:

- **Quick Stats** — global overview: top 10 rankings, filters by continent/region/alliance, KPI cards
- **Nation Overview** — full profile for any single country, with a capability radar chart and
  category breakdowns (manpower, air, land, navy, finance)
- **Compare Powers** — side-by-side comparison of any two countries across every major metric
- **Coalition Builder** — build a custom coalition of countries and compare its combined
  strength against a reference country or another coalition

## Data pipeline

1. **Scraping** (`scrape_military_metrics.py`) — pulls raw metrics from GlobalFirepower.com
   country pages using `requests` and `BeautifulSoup`. URL list: `links_for_military_data.txt`.
2. **Enrichment** (`generate_kpis.py`) — merges in continent/region, GDP, and NATO-alliance
   lookup data (`Military_Dataset_Lookups.xlsx`) and computes the KPIs below.
3. **Currency refresh** (`update_population.py`, `update_gdp.py`) — see note below.
4. **Dashboard** (`app.py`) — reads the final enriched dataset and renders all 4 modules.

## KPI definitions

| KPI | Definition |
|---|---|
| **Power Index Rank** | GlobalFirepower's own overall military strength ranking (1 = strongest; lower is stronger) |
| **Assets per Capita** | (Aircraft + Tanks + Naval Fleet) ÷ Total Population |
| **Budget-to-GDP Ratio** | Defense Budget (USD) ÷ GDP (USD) |
| **Power Index Rank Gap** | GDP Rank − Power Index Rank. Positive = a country's military rank is stronger than its economic size alone would predict ("punching above its weight"); negative = the opposite. *(This KPI wasn't precisely defined in the original project brief — this is the working definition used throughout the dashboard.)* |

## A note on data currency

GlobalFirepower publishes one annual edition (each entry is marked "last reviewed" in
January). All hardware, personnel, and budget figures in this dataset are already GFP's
current 2026 edition — there is nothing more recent to pull until their 2027 release.

Two fields, however, come from **outside** GlobalFirepower and were refreshed separately
because GFP's own figures lagged real-world data:

- **Population** — updated to current UN Population Division mid-2026 estimates (source:
  Worldometer). India's original GFP figure undercounted by roughly 70 million.
- **GDP** — updated to IMF World Economic Outlook (April 2026) 2025 nominal estimates,
  replacing the original 2022 World Bank figures.

`Assets per Capita`, `Budget-to-GDP Ratio`, and `Power Index Rank Gap` were recalculated
after each refresh so they stay internally consistent with the corrected figures.

One country, **Kosovo**, could not be refreshed on either metric — it isn't tracked
separately by the UN or IMF datasets used here, due to its disputed international status.
It remains on GlobalFirepower's original estimate.

## How to run the dashboard

```bash
pip install streamlit pandas openpyxl plotly
streamlit run app.py
```

This opens the dashboard in your browser at `http://localhost:8501`. Use the sidebar to
navigate between the four modules.

## Folder structure

```
military_dashboard/
├── scripts/
│   ├── scrape_military_metrics.py
│   ├── generate_kpis.py
│   ├── update_population.py
│   └── update_gdp.py
├── data/
│   ├── links_for_military_data.txt
│   ├── GFP_Military_Dashboard.xlsx
│   ├── Military_Dataset_Lookups.xlsx
│   └── military_final.xlsx          ← final dataset the dashboard reads
├── dashboard/
│   └── app.py
└── docs/
    └── README.md
```

## Tech stack

| Area | Tools |
|---|---|
| Scraping | Python, `requests`, `BeautifulSoup` |
| Processing | `pandas`, `openpyxl` |
| Visualization | Streamlit, `plotly` |
| Data sources | GlobalFirepower.com, UN Population Division, IMF World Economic Outlook |

## Limitations

- Population and GDP reflect current 2025/2026 external estimates; all other metrics
  reflect GlobalFirepower's most recent (2026) annual review.
- Kosovo's population and GDP figures could not be independently verified/updated.
- `power_index_rank_gap` uses a working definition (see KPI table above) not specified in
  the original project brief.
