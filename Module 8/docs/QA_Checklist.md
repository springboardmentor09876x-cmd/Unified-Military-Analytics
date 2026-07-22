# Module 7: Testing and Debugging

## QA Checklist & Test Execution Log

### 1. Navigation & UI Testing
- [x] **Verify Sidebar Navigation**: Toggle between Quick Stats, Nation Overview, Compare Powers, and Coalition Builder.
  - *Result*: All views switch seamlessly without page reload. Animations trigger properly.
- [x] **Verify Sidebar Collapse**: Click the hamburger menu to collapse and expand the sidebar.
  - *Result*: The layout adjusts correctly and the Plotly charts resize dynamically to fill the available space.
- [x] **Theme Consistency**: Ensure neon-red, dark background, and glowing effects are applied consistently across all 4 dashboards.
  - *Result*: Verified. Colors align with `style.css` variables (`--neon-red`, `--bg-dark`).

### 2. Data Accuracy & Parameter Testing
- [x] **Quick Stats (Global View)**: 
  - *Spot Check*: Top 5 PPP charts load correctly.
  - *Spot Check*: Rank map colors scale correctly (Rank 1 is brightest).
  - *Spot Check*: Bubble chart tooltips display formatted USD properly (e.g., "$895.0B").
- [x] **Nation Overview Filters**:
  - *Test*: Select "United States" from the dropdown. 
  - *Result*: Power Index shows ~0.0699 (varies by year, correctly fetched), Budget displays correctly.
  - *Test*: Select "China".
  - *Result*: Hardware charts update seamlessly.
- [x] **Compare Powers Selectors**:
  - *Test*: Select "Russia" for Country A and "Ukraine" for Country B.
  - *Result*: Green highlights correctly identify the winner in each metric row. Power Index highlights correctly since a *lower* score is better.
- [x] **Coalition Builder Selection**:
  - *Test*: Select multiple countries (e.g., France, Germany, UK) holding Ctrl/Cmd.
  - *Result*: Aggregated stats correctly sum the Active Personnel, Defense Budget, and average the Power Index.
  - *Test*: Compare against Russia.
  - *Result*: Side-by-side grouped bar chart successfully renders comparing the Coalition total vs Russia's total.

### 3. Layout & Tooltip Bug Fixes Applied
- **Fix Applied**: Adjusted chart margins in `script.js` so that axis labels are not cut off.
- **Fix Applied**: Added text formatting function `formatNumber()` to prevent excessively long numbers (e.g., 895000000000 -> 895.0B).
- **Fix Applied**: Set `responsive: true` on all Plotly charts so they re-render correctly upon window resize or sidebar toggle.

### 4. Tableau Compatibility Check
- The data source (`military_data.json`) has been verified to be completely flat and tabular, ensuring 100% compatibility when imported into Tableau Desktop or Tableau Public.
- Missing values (if any) are encoded as `0` or null, ensuring Tableau handles them correctly during aggregation (SUM/AVG).

## Status
**PASSED**. No functional bugs remaining. Navigation and data display verified end-to-end.
