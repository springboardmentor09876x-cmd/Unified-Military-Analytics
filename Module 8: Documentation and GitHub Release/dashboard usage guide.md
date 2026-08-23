# 📖 Dashboard Usage Guide

**Unified Military Analytics and Comparison Dashboard**
A Streamlit-based dashboard suite for exploring global military capability data.

This guide explains how to launch the dashboard and how to use each of its four modules: **Quick Stats**, **Nation Overview**, **Compare Powers**, and **Coalition Builder**.

---

## 🚀 Getting Started

### Requirements
- Python 3.9+
- Streamlit
- Pandas, NumPy
- Plotly
- openpyxl (for reading `.xlsx` data files)

### Installation

```bash
# Clone the repository
git clone https://github.com/springboardmentor09876x-cmd/Unified-Military-Analytics.git
cd Unified-Military-Analytics

# Install dependencies
pip install -r requirements.txt
```

### Launching the Dashboard

```bash
streamlit run app.py
```

This opens the dashboard in your default browser at `http://localhost:8501`. Streamlit automatically detects the additional dashboards inside the `pages/` folder and lists them in the **sidebar navigation**, so all four modules are reachable from a single running app — no separate launch commands needed.

### Data Requirements

The dashboard expects the cleaned dataset inside a `data/` folder at the project root:

```
data/
├── military_final.xlsx     # main wide-format dataset (used by all dashboards)
└── military_long.xlsx      # long-format dataset (used for detailed per-country metric lookups)
```

If these files are missing or misplaced, the dashboard will show a clear on-screen error explaining the expected file path — it will not crash silently.

---

## 🧭 Navigating the Dashboard

Use the **sidebar** on the left to switch between the four dashboard pages at any time:

| Sidebar Label | Page | File |
|---|---|---|
| Quick Stats Dashboard | Global overview | `app.py` |
| Nation Overview | Single-country deep dive | `pages/Nation_Overview.py` |
| Compare Powers | Two-country comparison | `pages/compare_powers.py` |
| Coalition Builder | Multi-country coalition simulator | `pages/coalition_builder.py` |

Each page loads and filters data independently — switching pages does **not** carry your filter selections from one page to another, so you can explore each module without one affecting the other.

---

## 1️⃣ Quick Stats Dashboard

**Purpose:** A global, filterable overview of military capability across all 140+ countries in the dataset.

### Sidebar Filters
Located under **🔎 Filters** in the sidebar:

| Filter | Type | Behavior |
|---|---|---|
| Country | Multi-select | Restricts the dashboard to one or more specific countries |
| Region | Multi-select | Restricts to one or more geographic regions |
| Continent | Multi-select | Restricts to one or more continents |
| Alliance | Multi-select | Restricts to one or more alliances (e.g., NATO) |

- All four filters are **cascading** — selecting a value in one filter automatically narrows the available options in the others, so you cannot create an impossible combination (e.g., a country paired with a continent it doesn't belong to).
- Filters can be combined freely (e.g., Continent = Asia **and** Alliance = NATO).
- Click **🔄 Reset Filters** at any time to instantly clear all four filters and return to the full, unfiltered dataset.
- If a filter combination matches zero countries, the dashboard shows a clear warning message instead of an empty or broken page.

### KPI Cards
Eight summary cards update live based on your current filter selection:

- Total Countries
- Avg Power Index
- Total Defense Budget
- Total Military Aircraft
- Total Tanks
- Total Naval Fleet
- Total Military Manpower
- Best Ranked Country

### Charts
Organized into four sections:

1. **Power & Budget Overview** — Top 10 by Power Index, Top 10 by Defense Budget, Top 10 by Military Aircraft, Top 10 by Purchasing Power Parity.
2. **Military Rank by Country** — an interactive world map, shaded by Power Index (lower score = stronger military = darker shading). Falls back to a ranked bar chart automatically if any country name can't be matched to the map.
3. **Asset Breakdown** — Top 10 by Aircraft, Top 10 by Tanks, Top 10 by Naval Fleet, and a Defense Budget vs. Power Index bubble chart (bubble size = aircraft count).
4. **Distribution** — Continent and Alliance donut charts showing how many countries fall into each category under the current filters.
5. **Military Capability Comparison** — a faceted small-multiples chart comparing Aircraft, Tanks, Naval Fleet, and Manpower for the top-ranked countries, each on its own scale (these metrics have very different magnitudes, so they're never plotted on one shared axis).

All charts respect the current filter selection and update automatically.

### Country Search
Use the **🔍 Country Search** section to select any single country (from the currently filtered list) and view:
- Its full profile card grid (Continent, Region, Alliance, Power Index Rank/Score, GDP, Population, etc.)
- An expandable **raw metrics** table pulling every recorded metric for that country from the long-format dataset.

### Country Military Overview Table
A searchable, scrollable data table at the bottom lists every country matching the current filters, with key columns: Continent, Region, Alliance, Power Index Rank/Score, Defense Budget, Aircraft, Tanks, Naval Fleet, Manpower, and GDP — sorted by Power Index Rank by default. Use the search box above the table to filter rows by country name.

---

## 2️⃣ Nation Overview

**Purpose:** A detailed, single-country military and economic profile.

### How to Use
1. Use the **🌎 Select Country** dropdown at the top of the page to choose any country in the dataset.
2. The entire page updates instantly to reflect the selected country — no separate "Apply" step needed.

### What You'll See

| Section | Contents |
|---|---|
| **Country Summary** | KPI cards for Power Rank, Power Index, Defense Budget, and Active Personnel |
| **Country Profile** | Continent, Region, Alliance, Power Index Rank/Score, GDP, Population, Land Area, Coastline, Border Coverage |
| **Military Manpower** | Active, Reserve, and Paramilitary personnel, plus Total Military Manpower |
| **Air Power** | Total Aircraft, Fighters, Attack, Transport, Trainer, Special Mission, Tanker Aircraft, plus Helicopters and Attack Helicopters |
| **Land Power** | Tanks, Armored Fighting Vehicles, Self-Propelled & Towed Artillery, Rocket Projectors |
| **Naval Power** | Total Naval Fleet, Carriers, Submarines, Destroyers, Frigates, Corvettes, plus Naval Fleet Tonnage |
| **Strategic Capability Profile** | A radar chart normalizing Air Power, Land Power, Naval Power, Manpower, Defense Budget, and Infrastructure (each scaled 0–100 relative to the strongest country in the dataset for that metric), so very different units can be compared fairly on one chart |
| **Economic & Strategic Metrics** | GDP, Defense Budget, Budget/GDP ratio, External Debt, Purchasing Power Parity, Forex & Gold Reserves |
| **Strategic Infrastructure** | Airports, Ports, Merchant Marine Fleet, Railway/Roadway/Waterway/Coastline/Border coverage |
| **Natural Resources** | Oil, Natural Gas, and Coal production, consumption, and proven reserves |
| **Selected Country vs. Global Average** | A bar chart showing each key metric as a % of the global average (100% = exactly average) |
| **Rank Information** | The country's rank (out of all countries with valid data) for Power Index, Aircraft, Tanks, Naval Fleet, and Defense Budget |

Any metric missing for a given country is simply omitted from its chart or shown as **N/A** rather than causing an error.

---

## 3️⃣ Compare Powers

**Purpose:** A side-by-side comparison of any two countries.

### How to Use
1. Select **Country A** and **Country B** from the two dropdown selectors.
2. The dashboard immediately renders a side-by-side comparison across:
   - Power Index Rank and Score
   - Defense Budget
   - Active Personnel
   - Military Aircraft
   - Naval Fleet
   - Derived KPIs (e.g., Budget-to-GDP Ratio)

Use this module to quickly answer questions like *"How does India's military compare to Japan's?"* without needing to cross-reference two separate Nation Overview pages.

> **Tip:** If both dropdowns are set to the same country, the comparison will simply show identical values on both sides — pick two different countries for a meaningful comparison.

---

## 4️⃣ Coalition Builder

**Purpose:** Simulate the combined military strength of a custom multi-country coalition, and compare it against a second coalition and/or a reference country.

### Sidebar Configuration
Under **⚙️ Coalition Configuration**:

| Control | Type | Purpose |
|---|---|---|
| 🟢 Coalition A | Multi-select | Choose one or more countries to form Coalition A |
| 🟡 Coalition B | Multi-select | Choose one or more countries to form Coalition B |
| 🔵 Reference Country | Single-select | Choose one baseline country to measure both coalitions against |

If either Coalition A or Coalition B is left empty, the dashboard shows a clear warning and pauses until at least one country is selected in each — it will not attempt to render broken or misleading charts with no data.

### What You'll See

| Section | Contents |
|---|---|
| **Coalition Overview** | The selected member countries for A, B, and the Reference country |
| **Key Metric Comparison** | KPI cards for Manpower, Personnel, Aircraft, Tanks, Naval Fleet, Submarines, Defense Budget, GDP, and Population — Coalition A and B are each shown with a % delta vs. the Reference baseline |
| **Power Index Analysis** | The *average* Power Index Score per group (never summed, since it's a relative ranking metric, not an additive quantity) and each group's single best-ranked member |
| **Military Manpower / Air Power / Land Power / Naval Power** | Grouped bar charts comparing Coalition A, Coalition B, and the Reference country across every relevant metric in that category |
| **Defense Economics** | Combined Defense Budget and GDP (summed across all members), plus an aggregate Budget-to-GDP ratio computed as *total budget ÷ total GDP* (not averaged per-country, for a mathematically sound result) |
| **Country Contribution** | Pick any metric from the dropdown to see, per coalition, how much each individual member country contributes to that coalition's total |
| **Coalition vs. Reference** | Percentage advantage/disadvantage of each coalition relative to the Reference country, metric by metric |
| **Coalition Summary** | An auto-generated, plain-English summary stating which coalition is stronger on each metric — this text is fully data-driven and updates automatically with your selections, never hard-coded |
| **Coalition Country Table** | A full table of every selected country (tagged by which coalition/reference group it belongs to) with all key comparison metrics. If a country is selected in more than one group, it's shown once with a combined tag (e.g., "Coalition A & Reference") rather than as a duplicate row |

### Notes on Aggregation Logic
- **Additive metrics** (manpower, aircraft, tanks, naval fleet, budget, GDP, population) are **summed** across all members of a coalition.
- **Power Index Score** is **averaged**, never summed, because it's a relative ranking metric.
- **Budget-to-GDP** is computed at the *group* level (total budget ÷ total GDP), not as an average of each country's individual ratio — this avoids skewing the result toward small economies with disproportionately high ratios.

---

## 🧾 General Behavior Across All Dashboards

- **No page ever crashes on missing or zero data** — every chart and KPI has a graceful fallback (an "N/A" value, a "no data available" chart annotation, or a warning message) instead of an error.
- **Numbers are always formatted for readability**: large values use K / M / B / T suffixes, currency values are prefixed with `$`, and percentages are shown with a sign (`+12.3%` / `−4.1%`).
- **Every chart is interactive** (Plotly): hover for exact values, use the legend to toggle series on/off, and use the built-in zoom/pan/download-as-PNG controls in the top-right of each chart.
- **Data is cached** on first load for performance — subsequent filter changes and page switches do not re-read the Excel files from disk.

---

## 🛠️ Troubleshooting

| Issue | Likely Cause | Fix |
|---|---|---|
| "Dataset not found" error on launch | `data/military_final.xlsx` (and/or `military_long.xlsx`) missing or in the wrong folder | Confirm the `data/` folder sits at the project root, alongside `app.py` |
| "No countries match the selected filters" | An overly narrow or contradictory filter combination | Click **🔄 Reset Filters**, then reapply filters one at a time |
| A chart shows "No data available for this selection" | The selected country/coalition/filter has no recorded value for that specific metric | This is expected — not every country has data for every field; check the Country Profile section for what is available |
| Sidebar shows "app" instead of "Quick Stats Dashboard" | Cosmetic label only — Streamlit derives this from the filename `app.py` | Does not affect functionality; can be renamed in a future release if desired |

---

## 📎 Related Documentation

- **README.md** — project overview, dataset description, KPI definitions, and project structure.
- **Project_Structure.md** — full repository folder/file breakdown.