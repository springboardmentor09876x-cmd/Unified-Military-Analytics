# ✅ QA Checklist — Module 7: Testing and Debugging

**Unified Military Analytics and Comparison Dashboard**

This checklist accompanies `Testing_and_Debugging.ipynb`. The notebook automates the checks marked **Automated**; the rest require a manual pass through the running Streamlit app (`streamlit run app.py`).  and log full detail in `QA_Test_Results.xlsx`.

**Legend:** ✅ Pass · ❌ Fail

---

## 1. Data Pipeline

| ID | Check | Type | Target | Result |
|---|---|---|---|---|
| D1 | Dataset loads without error (`military_final.xlsx`, `military_long.xlsx`) | Automated | No exception | ✅ |
| D2 | Country coverage | Automated | ≥ 140 countries | ✅ |
| D3 | Missing/null values across core columns | Automated | < 2% | ✅ |
| D4 | No duplicate country rows | Automated | 0 duplicates | ✅ |
| D5 | Power Index Rank values are unique and positive | Automated | 100% valid | ✅ |
| D6 | Required columns present (Power Index, GDP, Budget, Manpower, Aircraft, Tanks, Naval Fleet, Region, Continent, Alliance) | Automated | All present | ✅ |

---

## 2. Filters (Quick Stats Sidebar)

| ID | Check | Type | Target | Result |
|---|---|---|---|---|
| F1 | Empty filter selection shows the full, unfiltered dataset | Automated + Manual | Matches | ✅ |
| F2 | Single Country filter returns exactly that country | Automated | Exact match | ✅ |
| F3 | Single Region / Continent / Alliance filter matches a manual pandas filter | Automated | Exact match | ✅ |
| F4 | Selecting a Country narrows Region/Continent options to values consistent with that country | Automated + Manual | Consistent | ✅ |
| F5 | An impossible combination (e.g. Country = Algeria, Continent = Europe) cannot be created via the cascading filters | Manual | Impossible to select | ✅ |
| F6 | A combination with zero matches shows a clear warning, not a blank/broken page | Manual | Warning shown | ✅ |
| F7 | **🔄 Reset Filters** clears Country, Region, Continent, and Alliance simultaneously, with no stale selections and no full browser refresh | Manual | All 4 cleared | ✅ |
| F8 | Filters remain independent per dashboard page (switching pages does not carry over selections) | Manual | Independent | ✅ |

---

## 3. KPIs

| ID | Check | Type | Target | Result |
|---|---|---|---|---|
| K1 | `total_countries` KPI matches the number of unique countries in the current filter | Automated | Exact match | ✅ |
| K2 | `best_country` KPI matches the country with the lowest (strongest) Power Index Rank | Automated | Exact match | ✅ |
| K3 | KPI totals for a filtered subset never exceed the full-dataset totals | Automated | Always ≤ | ✅ |
| K4 | All 8 Quick Stats KPI cards render with correctly formatted values (no `NaN`, no raw floats where currency/large-number formatting is expected) | Manual | Correct formatting | ✅ |

---

## 4. Quick Stats Charts

| ID | Check | Type | Target | Result |
|---|---|---|---|---|
| C1 | Every Quick Stats chart function renders a valid Plotly figure on the full dataset | Automated | No exceptions | ✅ |
| C2 | Every Quick Stats chart function falls back to a clean "no data" figure on an empty dataset | Automated | No exceptions | ✅ |
| C3 | Military Rank world map renders as a choropleth on valid data | Automated + Manual | Choropleth shown | ✅ |
| C4 | Military Rank map falls back to a ranked bar chart (with caption) when country names can't be matched | Manual | Fallback + caption shown | ✅ |
| C5 | Charts visually update immediately when filters change | Manual | Updates correctly | ✅ |
| C6 | Hover tooltips show correctly formatted values on every chart | Manual | Correct on all charts | ✅ |
| C7 | An all-NaN metric column does not crash chart rendering | Automated | No exceptions | ✅ |
| C8 | Defense Budget bubble chart degrades gracefully when optional hover columns (`tanks`, `total_naval_fleet`) are missing | Automated | No exceptions | ✅ |

---

## 5. Nation Overview

| ID | Check | Type | Target | Result |
|---|---|---|---|---|
| N1 | `get_country_profile()` returns data for a known, valid country | Automated | Data returned | ✅ |
| N2 | `get_country_profile()` handles an unknown country name gracefully (no crash) | Automated | Empty/None, no crash | ✅ |
| N3 | `get_country_long_metrics()` returns raw metric rows for a known country | Automated | Data returned | ✅ |
| N4 | Selecting a new country from the dropdown updates every section of the page (KPIs, profile, manpower, air/land/naval power, radar chart, economics, infrastructure, resources, rank comparison) | Manual | All sections update | ✅ |
| N5 | Strategic Capability Profile radar chart correctly normalizes each axis 0–100 relative to the dataset maximum | Manual (spot-check 1–2 countries) | Values plausible | ✅ |
| N6 | Missing metrics for a given country are shown as "N/A" or simply omitted, never as an error or `NaN` | Manual | Handled cleanly | ✅ |
| N7 | Rank Information pills show correct rank / total-country counts | Manual (spot-check) | Matches manual calc | ✅ |

---

## 6. Compare Powers

| ID | Check | Type | Target | Result |
|---|---|---|---|---|
| CP1 | Selecting two different countries renders a correct side-by-side comparison | Manual | Correct values | ✅ |
| CP2 | Selecting the same country in both dropdowns does not crash (shows identical values on both sides) | Manual | No crash | ✅ |
| CP3 | All compared metrics (Power Index Rank, Defense Budget, Manpower, Aircraft, Naval Fleet, derived KPIs) match the raw dataset values for each selected country | Manual (spot-check) | Matches dataset | ✅ |

---

## 7. Coalition Builder

| ID | Check | Type | Target | Result |
|---|---|---|---|---|
| CB1 | Additive metrics (manpower, aircraft, tanks, naval fleet, budget, GDP, population) are **summed** across coalition members | Automated | Sum matches | ✅ |
| CB2 | Power Index Score is **averaged**, never summed, across coalition members | Automated | Mean matches, ≠ sum | ✅ |
| CB3 | "Best ranked member" of a coalition matches the country with the lowest Power Index Rank in that group | Automated | Exact match | ✅ |
| CB4 | Budget-to-GDP ratio is computed as (total budget ÷ total GDP), not averaged per-country | Automated | Group-level ratio | ✅ |
| CB5 | An empty coalition (no countries selected) is handled safely — a warning is shown, no crash | Automated + Manual | Warning shown | ✅ |
| CB6 | A zero-GDP coalition reports Budget-to-GDP as "N/A", never a divide-by-zero error | Automated | "N/A" shown | ✅ |
| CB7 | `pct_delta()` returns `None`/"N/A" instead of raising when the Reference value is 0 | Automated | "N/A" shown | ✅ |
| CB8 | A country selected in more than one group (e.g. also the Reference country) appears once in the Coalition Country Table with a combined tag, not as a duplicate row | Manual | Single combined row | ✅ |
| CB9 | Coalition Summary text is fully data-driven and updates correctly when selections change (no stale/hard-coded text) | Manual | Updates correctly | ✅ |
| CB10 | Country Contribution chart correctly reflects each member's share of the selected metric within its coalition | Manual (spot-check) | Matches manual calc | ✅ |

---

## 8. Cross-Cutting / General

| ID | Check | Type | Target | Result |
|---|---|---|---|---|
| G1 | Sidebar navigation correctly switches between all 4 dashboard pages | Manual | Works | ✅ |
| G2 | Every numeric display uses consistent formatting (K/M/B/T suffixes, `$` for currency, signed `%` for deltas) | Manual | Consistent | ✅ |
| G3 | No dashboard page throws an unhandled exception under normal use | Manual | No crashes | ✅ |
| G4 | Missing/malformed data files show a clear on-screen error message, not a stack trace | Manual | Clear error shown | ✅ |
| G5 | Dashboard loads within a reasonable time on first run and on subsequent filter changes (cached data reused) | Manual | Acceptable performance | ✅ |

---

**Notes:**
All 54 checks across data pipeline, filters, KPIs, charts, Nation Overview, Compare Powers, Coalition Builder, and cross-cutting behavior passed on both automated testing (`Testing_and_Debugging.ipynb`) and manual review of the running dashboard.