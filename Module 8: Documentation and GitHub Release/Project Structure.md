# 🗂️ Project Structure

**Unified Military Analytics and Comparison Dashboard**

This document describes the full repository layout, organized by development milestone/module.

---

## Repository Tree

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

---

## Folder-by-Folder Summary

| Folder | Milestone | Purpose |
|---|---|---|
| `Module1-Scrapping and Execution/` | 1 | Web scraping scripts (`requests` + `BeautifulSoup`), the source URL list, saved raw per-country HTML, and the raw scraped dataset |
| `Module2-Data Cleaning/` | 1 | Data-cleaning notebook and the cleaned output dataset |
| `Module3-KPI Feature Engineering/` | 2 | KPI computation script and the final cleaned + KPI-enriched dataset (`military_final.xlsx`, `military_long.xlsx`) |
| `Module4-Dashboard Planning and Prototyping/` | 2 | Wireframes, storyboard, and the initial Tableau prototype |
| `Module5&6-Full Dashboard Development/` | 3 | The complete, working Streamlit dashboard suite — all 4 dashboards (`app.py` + `pages/`) |
| `Module7-Testing and Debugging/` | 4 | QA notebook and test-results log validating filters, KPIs, and navigation |
| `Module8-Documentation and GitHub Release/` | 4 | Final documentation set: README, usage guide, and this structure doc |
| `.gitignore` | — | Excludes local/environment files from version control |
| `README.md` (root) | — | Top-level project overview, dataset description, KPI definitions, tech stack |

