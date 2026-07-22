# Module 3: KPI Feature Engineering

This module focuses on calculating key performance indicators (KPIs) from the cleaned military dataset generated in Module 2 and structuring the final data into formats optimal for Tableau visualization.

## Tasks Performed
- **Computed KPIs**:
  - `power_index_rank_gap`: Calculated the ranking based on the Power Index (lower is better) and determined the gap in the Power Index score compared to the next rank.
  - `assets_per_capita`: Calculated total tactical assets (sum of aircraft, helicopters, tanks, naval fleet, artillery, etc.) per capita for each nation.
  - `budget_to_gdp_ratio`: Calculated the ratio of defense budget to the country's effective GDP or Purchasing Power Parity (PPP).
- **Metadata Enrichment**:
  - Ensured metadata fields from Module 2 (`continent`, `region`, `alliance`) are retained.
  - Added an explicit `is_nato` boolean flag for quick filtering of NATO members in BI tools.
- **Data Formatting**:
  - Transformed the final data into both **Wide** and **Long** formats. The long form "melts" all metric values into `metric_name` and `metric_value` columns alongside identifier variables, ensuring the data loads effortlessly in Tableau without requiring further transformation.

## Deliverables
- `generate_kpis.py`: A Python script that seamlessly ingests data from Module 1 and Module 2 to compute these KPIs and outputs the Excel file.
- `military_final.xlsx`: The finalized dataset containing:
  - **Wide_Format sheet**: The standard columnar data structure.
  - **Long_Format sheet**: The structural "melted" variant optimized for Tableau ingestion.

## Evaluation Criteria Met
- All specified KPIs are present and verified.
- The `military_final.xlsx` file structure is immediately compatible with Tableau.
