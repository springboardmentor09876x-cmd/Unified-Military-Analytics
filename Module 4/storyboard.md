# Module 4: Dashboard Storyboard and Prototype Layouts

## Overview
This storyboard defines the flow, navigation, and structural layout of the Military Analysis Dashboard, customized for a dark, neon aesthetic. The application is built entirely with **Vanilla HTML, CSS, and JavaScript**, ensuring it is lightweight, blazing fast, and easily deployable to static hosts like Netlify.

---

## 1. Quick Stats (Global Overview)
**Target**: Operational dashboard providing an at-a-glance view of global military standings.

### Layout Structure:
- **Header**: Main title "MILITARY ANALYTICS" and a collapsible sidebar button (`☰`).
- **Top Filter Bar**: Selectors for Continent and Region.
- **KPI Row (4 Cards)**:
  - **Total Global Defense Budget (USD)**
  - **Total Global Military Manpower**
  - **Total Global Assets**
  - **Top Power Index**
  *Each card features a unique neon glowing top-border (pink, cyan, yellow, purple) and text shadow.*
- **Charts Row**:
  - **Horizontal Bar Chart**: Top 10 Countries by Budget to GDP Ratio using 10 distinct, vibrant neon colors.
  - **Donut Chart**: Asset share by continent using custom neon color palettes.

---

## 2. Nation Overview
**Target**: Deep dive into the capabilities of a single chosen nation.

### Layout Structure:
- **Header**: Title and Subtitle.
- **Top Filter Bar**: A dynamic, searchable text input with an autocomplete dropdown (`<datalist>`) for selecting a specific country.
- **KPI Row**: 
  - **Power Index Score & Global Rank**.
  - **Defense Budget**.
  - **Active Personnel**.
  - **Total Assets**.
- **Charts**:
  - **Radar Chart (Center)**: Visualizing military balance (Personnel, Tanks, Aircraft, Naval Fleet).
  - **Horizontal Bar Charts**: Detailed hardware breakdown (Tanks, AFVs, Artillery, Fighters, etc.).

---

## Navigation Logic
- A **Sidebar** hosts the navigation radio buttons allowing the user to seamlessly switch between the views.
- The sidebar features a toggle button to completely collapse it, allowing the main dashboard content and Plotly charts to dynamically resize and take over the full screen.

## Theme Configuration
The visual aesthetic relies heavily on a centralized `style.css` file enforcing a dark mode base (`#0A0A0F`) with customized neon primary colors (`#B829EA`, `#FF007F`, `#00F0FF`). Charting is handled natively by `Plotly.js` manipulating the DOM directly, ensuring the charts blend perfectly into the dark, glowing aesthetic.

The hosted app in Netlify to be opened in pc: "https://infosys-military-analysis-1.netlify.app/"
