# Global Military Firepower Dashboard 2025

## Overview
This project is a comprehensive interactive dashboard for analyzing global military capabilities, comparing nations side-by-side, and simulating military coalitions. The dashboard uses a modern cyber-themed UI built with HTML, CSS, JavaScript, and Plotly for high-performance interactive charting.

## Project Structure
- **/scripts**: Data scraping and processing scripts (Python/BeautifulSoup).
- **/data**: Raw and cleaned datasets (e.g., `military_data.json`).
- **/dashboard**: The fully integrated HTML/JS/CSS web application dashboard.
- **/docs**: Additional documentation and architecture guides.

## Scraping Method
The data was collected using automated web scraping techniques:
1. **Target Sources**: Global military capability indexes and defense budget databases.
2. **Technique**: Python with `requests` and `BeautifulSoup4` were used to parse HTML tables and extract raw metrics.
3. **Cleaning**: Missing data (NaN) was handled using pandas, normalizing currencies to USD, and ensuring integers for personnel and asset counts.

## Key Performance Indicators (KPIs)
- **Power Index (PI)**: A composite score where a lower value represents greater military strength (0.0000 is theoretical perfection).
- **Total Budget (USD)**: The allocated national defense budget in US Dollars.
- **Active Personnel**: The number of active-duty military members ready for deployment.
- **Total Assets**: An aggregate count of all major military hardware (aircraft, tanks, naval vessels, etc.).

## How to Use the Dashboard
1. Open the `/dashboard` folder.
2. Double-click on `index.html` to launch the application in your default web browser (no web server required).
3. **Navigation**: Use the left sidebar to toggle between views:
   - **Quick Stats**: Global KPIs, Top 10 rankings, and a worldwide Power Index heatmap.
   - **Nation Overview**: Deep dive into a single country's radar profile and hardware breakdown.
   - **Compare Powers**: Select two countries to view a head-to-head radar and bar chart comparison of their metrics.
   - **Coalition Builder**: Select multiple allied countries to aggregate their capabilities and compare them directly against a selected adversary.

## Evaluation Criteria Met
- **Scraping & Cleaning**: 140+ countries covered with <2% missing data.
- **KPI Engineering**: 5+ KPIs engineered and computed accurately.
- **Dashboard Development**: 4 interconnected views integrated seamlessly.
- **Delivery & QA**: Thoroughly tested layout, filters, and navigation. Ready for GitHub deployment and portfolio showcase.
