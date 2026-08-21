# Unified Military Analytics and Comparison Dashboard

An interactive Tableau dashboard suite analyzing global military power in 2026, built with
Python (scraping, cleaning, KPI engineering) and Tableau Public (visualization), using
open-source defense data from [GlobalFirepower.com](https://www.globalfirepower.com)
(145 countries, 68+ indicators).

## What it does

Four connected dashboards, linked by navigation buttons:

- **Quick Stats** — Top 10 countries by Power Index and Defense Budget, KPI cards
  (countries shown, total budget, total personnel, total aircraft), filterable by
  continent, region, and NATO membership.
- **Nation Overview** — full profile for any single country (dropdown selector):
  headline KPIs (Power Index Rank, Score, GDP Rank, Rank Gap) plus a capability
  bar chart across manpower, air, land, naval, and budget metrics.
- **Compare Powers** — side-by-side comparison of any two countries (Country A /
  Country B dropdowns), a full metrics table, and a grouped bar chart.
- **Coalition Builder** — build a custom coalition by ticking countries in an
  interactive set, see combined totals in a table and grouped bar chart.

## Data pipeline

1. **Scraping** (`scrape_military_metrics.py`) — pulls raw metrics from
   GlobalFirepower.com country pages using `requests` and `BeautifulSoup`.
   URL list: `links_for_military_data.txt`.
2. **Cleaning** (`clean_data.py`) — strips currency symbols, commas, and unit
   suffixes (km, bbl, etc.) from the raw scrape, converts every column to a
   proper numeric type, standardizes column names to snake_case.
3. **KPI Engineering** (`generate_kpis.py`) — merges in continent/region, GDP,
   and NATO-alliance lookup data and computes the KPIs below.
4. **Currency refresh** (`update_population.py`, `update_gdp.py`) — see note below.
5. **Dashboard** (`global_military_firepower_2025.twbx`) — the final Tableau
   Packaged Workbook, built on `military_final.xlsx`, containing all 12
   worksheets across the 4 dashboards above.

## KPI definitions

| KPI | Definition |
|---|---|
| **Power Index Rank** | GlobalFirepower's own overall military strength ranking (1 = strongest; lower is stronger) |
| **Assets per Capita** | (Aircraft + Tanks + Naval Fleet) ÷ Total Population |
| **Budget-to-GDP Ratio** | Defense Budget (USD) ÷ GDP (USD) |
| **Power Index Rank Gap** | GDP Rank − Power Index Rank. Positive = a country's military rank is stronger than its economic size alone would predict ("punching above its weight"); negative = the opposite. *(Working definition — not precisely specified in the original brief.)* |

## A note on data currency

GlobalFirepower publishes one annual edition (each entry marked "last reviewed" in
January). All hardware, personnel, and budget figures here are GFP's current 2026
edition — there is nothing more recent to pull until their 2027 release.

Two fields come from **outside** GlobalFirepower and were refreshed separately,
since GFP's own figures lagged real-world data:

- **Population** — current UN Population Division mid-2026 estimates (source:
  Worldometer). India's original GFP figure undercounted by roughly 70 million.
- **GDP** — IMF World Economic Outlook (April 2026) 2025 nominal estimates,
  replacing the original 2022 World Bank figures.

`Assets per Capita`, `Budget-to-GDP Ratio`, and `Power Index Rank Gap` were
recalculated after each refresh to stay internally consistent.

**Kosovo** could not be refreshed on population or GDP — it isn't tracked
separately by the UN or IMF datasets used here, due to its disputed
international status. It remains on GlobalFirepower's original estimate.

## How to open the dashboard

1. Install [Tableau Public](https://public.tableau.com) (free).
2. Open `global_military_firepower_2025.twbx` — the data is packaged inside
   the file, so no separate Excel file is needed.
3. Use the navigation buttons on each dashboard to move between Quick Stats,
   Nation Overview, Compare Powers, and Coalition Builder.

## Folder structure (as submitted)

```
Milestone 1 - soniya/
├── Module-1/
│   ├── scrape_military_metrics.py
│   └── military_raw_data.csv
└── Module-2/
    ├── clean_data.py
    └── military_cleaned.csv

Milestone 2 - soniya/
├── Module-3/
│   ├── generate_kpis.py
│   └── military_final.xlsx
└── Module-4/
    └── Dashboard_Storyboards.pdf

Milestone 3 - soniya/
├── global_military_firepower_2025.twbx
└── README.md
```

## Tech stack

| Area | Tools |
|---|---|
| Scraping | Python, `requests`, `BeautifulSoup` |
| Processing | `pandas`, `openpyxl` |
| Visualization | Tableau Public |
| Data sources | GlobalFirepower.com, UN Population Division, IMF World Economic Outlook |

## Limitations

- Population and GDP reflect current 2025/2026 external estimates; all other
  metrics reflect GlobalFirepower's most recent (2026) annual review.
- Kosovo's population and GDP figures could not be independently verified/updated.
- `Power Index Rank Gap` uses a working definition (see KPI table above) not
  precisely specified in the original project brief.
- Coalition Builder currently supports comparing a custom coalition against a
  single reference country; comparing two custom coalitions against each
  other would require an additional Set and parameter, not included here.
