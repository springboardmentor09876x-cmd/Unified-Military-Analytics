# Module 5: Quick Stats and Nation Overview Dashboards

## Overview
This module expands upon the dashboard layout designed in Module 4 to fulfill specific analytical requirements. It is a fully static, serverless web application built with Vanilla HTML, CSS, JavaScript, and Plotly.js, maintaining the dark, neon-themed aesthetic. 

The dashboard is structured into two main views:

### 1. Quick Stats
A global operational overview featuring:
- **Filters**: Dynamically filter the entire dataset by **Continent**, **Region**, and **Alliance**.
- **Dynamic KPIs**: Key performance indicators (Total Budget, Total Manpower, Total Assets, and the Top Ranked country) that update dynamically based on the selected filters.
- **Top 10 Chart**: A horizontal bar chart displaying the Top 10 countries by **Power Index**. 

### 2. Nation Overview
A deep dive into individual national military capabilities featuring:
- **Country Selection**: A searchable dropdown to select and view a specific country's full profile.
- **Dynamic KPIs**: Quick access to the country's Power Index, Rank, Defense Budget, Active Personnel, and Total Assets.
- **Military Balance Radar Chart**: A radar chart visualizing the balance between Personnel, Tanks, Aircraft, and Naval Fleet. Includes custom tooltips that compare the country's stats against the **Global Maximum** values.
- **Hardware Breakdown**: A detailed horizontal bar chart breaking down specific military hardware (Destroyers, Submarines, Helicopters, Fighters, Artillery, AFVs, and Tanks). Also features tooltips comparing counts to global maximums.

## How to Run

Because this dashboard is entirely static and relies on frontend technologies, no backend server or Python dependencies are strictly required.

1. Navigate to the `Module 5` directory.
2. For the best experience and to bypass local CORS policies when fetching the JSON data, start a local HTTP server:
   ```bash
   cd "Module 5"
   python -m http.server 8080
   ```
3. Open `http://localhost:8080` in your web browser. 

The hosted app in Netlify to be opened in pc: "https://infosys-military-analysis-2.netlify.app/"
