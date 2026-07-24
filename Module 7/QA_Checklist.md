# QA Checklist - Military Analytics Dashboard (Modules 6-8)

## 1. UI and Layout
- [ ] Dashboard scales correctly on different screen sizes.
- [ ] Dark neon cyber theme is consistent across all views.
- [ ] Navigation sidebar toggles properly (collapses and expands).
- [ ] Switching between the 4 views (Quick Stats, Nation Overview, Compare Powers, Coalition Builder) works without page reload.
- [ ] Hover effects and tooltip styling match the aesthetic.

## 2. Functional Requirements
- **Quick Stats:**
  - [ ] Continent, Region, and Alliance filters apply correctly.
  - [ ] KPIs (Total Budget, Manpower, Assets, Top Ranked) update when filters change.
  - [ ] Top 10 Power Index bar chart updates dynamically.
  - [ ] World Map displays the Power Index gradient and handles filtering.
  - [ ] Donut charts (Top 5 PPP, Military Assets, Naval Fleet, Air Fleet, Land Fleet, Defence Budget) display and update correctly.
  - [ ] KPI Chart (Budget to GDP Ratio) updates correctly.
- **Nation Overview:**
  - [ ] Dropdown/search successfully selects a single country.
  - [ ] Military Balance Radar chart draws accurately.
  - [ ] Hardware Breakdown bar chart displays correct values.
- **Compare Powers:**
  - [ ] Two country selectors work independently.
  - [ ] Metrics for both countries display properly.
  - [ ] Radar and Bar charts compare the selected countries accurately.
- **Coalition Builder:**
  - [ ] Multi-select tag system allows adding and removing countries.
  - [ ] Aggregated totals for the coalition sum correctly (Budget, Manpower).
  - [ ] Comparison bar chart against the "Adversary" works correctly.

## 3. Data Accuracy
- [ ] Spot-check: USA budget and manpower metrics.
- [ ] Spot-check: China vs USA comparison stats in "Compare Powers".
- [ ] Spot-check: Coalition (USA + UK + France) vs Russia.

## 4. Known Issues / Bug Fixes
- Fixed layout responsiveness on resize.
- Prevented errors when selecting non-existent countries in search.
- Added color gradient scale reversal to World Map to ensure visual clarity.
