# Military Dashboard

A Tableau dashboard project covering data scraping, cleaning, KPI generation, and interactive visualization of military-related data.

---

## 📌 Project Overview
This project scrapes raw military data, cleans and processes it, calculates key performance indicators (KPIs), and presents the results in an interactive Tableau dashboard.

---

## 🗂️ Project Structure

```
MILITARY_DASHBOARD_FIN/
│
├── scripts/
│   ├── scrape_military_metrics.py     # Data scraping script (Module 1)
│   ├── clean_data.ipynb               # Data cleaning notebook (Module 2)
│   └── generate_kpis.py               # KPI generation script (Module 3)
│
├── data/
│   ├── military_raw_data.csv          # Raw scraped data (Module 1)
│   ├── military_cleaned.csv           # Cleaned dataset (Module 2)
│   └── military_final.xlsx            # Final dataset with KPIs (Module 3)
│
├── dashboard/
│   ├── Military_Dashboard_MODULE_5.pbix          # Dashboard build (Module 5)
│   └── Military_Dashboard_ALL_4_Integrated.pbix  # Fully integrated dashboard (Module 6)
│
├── docs/
│   ├── storyboard.pdf                 # Dashboard storyboard (Module 4)
│   ├── Prototype_Link.txt             # Link to prototype
│   ├── SAMPLE_IMAGES/                 # Sample reference images (Module 4)
│   ├── QA_Checklist_Module7.xlsx      # QA test log (Module 7)
│   ├── Module7_Testing_Summary.pdf    # Testing summary (Module 7)
│   └── Final_Delivery_Checklist.pdf   # Final delivery sign-off (Module 7)
│
├── README.md                          # This file
├── LICENSE                            # MIT License
└── GitHub_Repository_Link.md          # Link to the published GitHub repository
```

---

## 🔎 Scraping Method

Military data is collected using the `scrape_military_metrics.py` script, which pulls raw records from the project's source data feed and writes them to `data/military_raw_data.csv`. The script handles the data pull and initial capture of fields needed for downstream cleaning and KPI generation.

To run the scraper:
```bash
python scripts/scrape_military_metrics.py
```

---

## 🧹 Data Cleaning

Data cleaning is performed in `scripts/clean_data.ipynb`, which processes the raw scraped data — standardizing formats, handling missing or invalid records, and preparing the dataset for KPI generation. The cleaned output is saved to `data/military_cleaned.csv`.

---

## 📊 KPI Generation

Key performance indicators are calculated using `scripts/generate_kpis.py`, which processes the cleaned dataset and outputs the final KPI-enriched dataset used by the dashboard: `data/military_final.xlsx`.

---

## 📈 How to Open/Use the Dashboard

1. Download or clone this repository.
2. Open the dashboard file (`dashboard/Military_Dashboard_ALL_4_Integrated.pbix`) in Tableau Desktop or Tableau Public.
3. If prompted, point the data source to `data/military_final.xlsx`.
4. Use the filters and parameters on each dashboard page to explore the data.
5. Navigate between dashboard pages using the on-screen navigation buttons.
6. Hover over any chart element to view detailed tooltips.

See `docs/Prototype_Link.txt` and `GitHub_Repository_Link.md` for the prototype and published dashboard links.

---

## ✅ Testing & QA

All dashboard functionality — filters, parameters, navigation, data accuracy, tooltips, labels, layout, and performance — was tested and verified in Module 7. See:
- `docs/QA_Checklist_Module7.xlsx`
- `docs/Module7_Testing_Summary.pdf`
- `docs/Final_Delivery_Checklist.pdf`

**Status:** ✅ Testing completed — No functional issues remaining — Ready for delivery

---

## 🚀 Project Status

| Module | Description | Status |
|---|---|---|
| Module 1 | Data Scraping | ✅ Complete |
| Module 2 | Data Cleaning | ✅ Complete |
| Module 3 | KPI Generation | ✅ Complete |
| Module 4 | Storyboarding | ✅ Complete |
| Module 5 | Dashboard Build | ✅ Complete |
| Module 6 | Dashboard Integration | ✅ Complete |
| Module 7 | Testing & Debugging | ✅ Complete |
| Module 8 | Documentation & GitHub Release | ✅ Complete |

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
