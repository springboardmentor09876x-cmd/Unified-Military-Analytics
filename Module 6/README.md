# Module 6: Compare Powers and Coalition Builder Dashboards

## Overview
This module expands the Military Analytics dashboard by integrating two advanced analytical views: **Compare Powers** and **Coalition Builder**. It successfully unifies all four dashboard components into a single, cohesive web application that maintains a consistent dark neon cyberpunk aesthetic. 

## Features

### 1. Quick Stats & Global Heatmap
- **Global Overview**: Filters metrics by Continent, Region, and Alliance.
- **Top 10 by Power Index**: A horizontal bar chart of the top military powers.
- **Global Heatmap**: A Plotly Choropleth world map visualizing the Power Index globally. 
  - *Interactive Feature*: Scroll zoom is disabled by default to allow smooth page scrolling. Click anywhere on the map to enable zoom and pan functionality.

### 2. Nation Overview
- **Deep Dive**: Select any individual nation to view its military balance radar and a detailed hardware breakdown (Tanks, Aircraft, Navy, etc.).

### 3. Compare Powers
- **Head-to-Head Analysis**: Select any two countries for a side-by-side comparison.
- **Metrics**: Compares manpower, aircraft, naval fleet, budget, and Power Index.
- **Visualizations**: Features a dual-trace scatterpolar (radar) chart and a logarithmic bar chart to account for vast differences in scale between nations.

### 4. Coalition Builder
- **Multi-Country Selector**: Build a custom alliance by searching and adding multiple countries to a tag list.
- **Aggregated Totals**: Automatically sums the defense budget and manpower for the entire coalition.
- **Adversary Comparison**: Compare your custom coalition's combined metrics against a chosen adversary (e.g., Russia or China) via an interactive bar chart.

## Technologies Used
- **HTML5 & CSS3**: Custom grid layouts, flexbox, and linear gradient styling for the cyberpunk UI.
- **JavaScript (ES6)**: DOM manipulation, data filtering, multi-select tag system, and dynamic updates without page reloads.
- **Plotly.js**: High-performance interactive charting for radar charts, bar charts, and the global choropleth map.

## How to Run
To view the dashboard:
1. Open the `/Module 6` folder.
2. Double-click on `index.html` to open it in your default web browser. 
3. Alternatively, you can run a local development server in this directory:
   ```bash
   python -m http.server 8080
   ```
   And navigate to `http://localhost:8080` in your browser.

The hosted app in Netlify to be opened in pc: "https://infosys-global-military-analysis-gosh.netlify.app/"