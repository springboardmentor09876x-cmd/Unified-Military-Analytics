# Module 6: Build Compare Powers and Coalition Builder Dashboards

This module integrates the final components of the Military Analytics project. Given that the dashboard from Module 4 and 5 was built using Web Technologies (HTML/CSS/JS) to allow for complete customization and interactivity (mimicking a Tableau dashboard visually but functioning natively in the browser), we have extended the web version to include **all 4 required views**.

## Deliverables
- Integrated dashboard with 4 views: **Quick Stats**, **Nation Overview**, **Compare Powers**, and **Coalition Builder**.
- Global navigation and integrated filters.
- Recreated the layout from the Sample Image (World Map, Donut Charts, Bubble Chart, Bar Charts) but adapted it to the Neon Dark Theme used in Module 4 & 5.

## Web Dashboard Features
- **Compare Powers**: Select any two countries from dropdowns to see side-by-side metric comparisons (Manpower, Aircraft, Navy, Budget) with visual indicators.
- **Coalition Builder**: Select multiple countries and view aggregated totals, then compare against another country/coalition.
- **Seamless Navigation**: Switch between all 4 dashboards dynamically without page reloads.

## Tableau Implementation Note
If you specifically require a `.twbx` (Tableau Packaged Workbook) file for your portfolio, here are the steps to build the Tableau version:
1. **Connect Data**: Import `military_data.json` into Tableau Desktop.
2. **Calculated Fields (Compare Powers)**:
   - Create Parameters: `Select Country A` and `Select Country B`.
   - Create Calculated Fields: `Metric A` = `IF [Country] = [Select Country A] THEN [Metric] END`.
3. **Calculated Fields (Coalition Builder)**:
   - Create a Set: `Coalition Countries Set`.
   - Add a Filter for this set to sum metrics for the coalition.
4. **Integration**: Create a central Dashboard in Tableau. Add Navigation buttons targeting the other 3 dashboards. Check "Apply to all using this data source" for global filters.
5. **Save**: Save as `global_military_firepower_2025.twbx`.

## Running the Web Version
Simply open `index.html` in your browser. No server setup is required.

The hosted app in Netlify to be opened in pc: "https://infosys-global-military-analysis-gosh.netlify.app/"