# 🪖 Global Military Power Dashboard (`military.pbix`)

A Power BI report analyzing and comparing the military strength, defense spending, and strategic capabilities of countries worldwide.
It combines raw military asset data (aircraft, tanks, naval fleets, personnel) with economic indicators (GDP, defense budget) to surface rankings, 
ratios, and "what-if" coalition comparisons.

## 📊 Overview

| | |
|---|---|
| **File** | `military.pbix` |
| **Tool** | Microsoft Power BI Desktop |
| **Pages** | 7 |
| **Visuals** | ~79 across all pages |
| **File size** | ~1.4 MB |

## 📑 Report Pages

1. **Executive Overview** – High-level KPI cards, a world map colored by power rank, and top-5 charts for military aircraft and defense budgets.
2. **Military Assets** – Country rankings (top 15) for aircraft, tanks, and naval fleet size, plus a fighter-vs-attack aircraft breakdown. Filterable by country, alliance, and continent.
3. **Economics Analysis** – Defense budget vs. GDP scatter plot, budget-as-%-of-GDP KPIs, and budget distribution by continent.
4. **Strategic Insights** – A detailed power-ranking table alongside per-capita metrics (assets, aircraft, tanks, naval fleet per million population) and personnel ratios.
5. **Quick Stats** – Condensed KPI cards and top-10 rankings for a fast, at-a-glance summary.
6. **Compare Powers** – Side-by-side comparison of two selected countries across personnel, aircraft, budget, navy, tanks, and power index.
7. **Coalition Builder** – Interactive "what-if" tool to select multiple countries and see combined coalition manpower, aircraft, tanks, and defense budget vs. a reference country.

## 🗂️ Data Model

The report is built around one primary fact table plus supporting comparison tables generated for the interactive pages:

- **Main country data** — includes fields such as:
  - `Country`, `Continent`, `Region`, `Alliance`
  - `active_personnel`, `total_population`
  - `total_military_aircraft`, `fighter_aircraft`, `attack_aircraft`
  - `tanks`, `total_naval_fleet`
  - `defense_budget_usd`, `GDP`
  - `Power Index`, `Power_Rank`
- **Calculated / derived measures**:
  - `Budget_to_GDP_Ratio`
  - `Aircraft_per_Million`, `Tanks_per_Million`, `Naval_per_Million`
  - `Military_Personnel_Ratio`
  - `Assets_Per_Capita`, `Total_Assets`
  - `Average Power Index`
- **Comparison tables** (used on the *Compare Powers* page): `Country 1`, `Country 2` — mirrored metrics (Active Personnel, Aircraft, Navy, Tanks, Defense Budget, Power Index) per selected country.
- **Coalition table** (used on the *Coalition Builder* page): `Wide_Format`, `Reference Country` — aggregated coalition metrics (Active Personnel, Aircraft, Tanks, Naval Fleet, Defense Budget, Countries) vs. a reference country.

> Exact table names, relationships, and DAX formulas live inside the compressed Power BI data model and are best viewed directly in Power BI Desktop (see below) or with **Tabular Editor** / **DAX Studio** for a full schema dump.

## 🖥️ Requirements

- [Power BI Desktop](https://powerbi.microsoft.com/desktop/) (free) — Windows only.
- No external data source connections are required to view the report; data is embedded in the file (import mode).

## 🚀 How to Use

1. Download this repository.
2. Open `military.pbix` in Power BI Desktop.
3. Use the slicers (Country, Alliance, Continent, Region) on each page to filter the view.
4. On **Compare Powers**, pick two countries to generate a side-by-side breakdown.
5. On **Coalition Builder**, select multiple countries to simulate a combined coalition's strength against a reference country.

## 📌 Notes

- This is a data-visualization/analysis project intended for educational and illustrative purposes. Military capability figures are simplified indicators and should not be used for real-world strategic or policy decisions.
- Data sources for military/defense statistics are not documented within the file itself — add a `data-sources.md` here if you want to credit the original dataset(s) used.

