# Dashboard Usage Guide

## Unified Military Analytics Dashboard

This guide explains how to open and use the Power BI dashboard.

---

# Opening the Dashboard

1. Download or clone the project repository.
2. Install Microsoft Power BI Desktop.
3. Navigate to:

   Milestone-3 - Full Dashboard Development

4. Open the final:

   Global_Military_Analytics_Dashboard.pbix

5. If Power BI asks for the data source, update the file path to:

   military_final.xlsx

---

# Dashboard Navigation

The report contains four interactive dashboard pages:

1. Quick Stats
2. Nation Overview
3. Power Comparison
4. Coalition Builder

Use the navigation buttons available on each page to move between dashboards.

---

# Quick Stats

The Quick Stats page provides a high-level overview of global military power.

## Available Filters

- Continent
- Region
- Alliance

Use these filters to explore different groups of countries.

The dashboard dynamically updates:

- KPI cards
- Top 10 Power Index visualization

To reset the dashboard, clear the applied filters.

---

# Nation Overview

The Nation Overview page provides a detailed military profile for an individual country.

## How to Use

1. Select a country from the country selector.
2. The dashboard will update automatically.

The dashboard displays:

- Global Power Rank
- Power Index
- GDP
- Defense Budget
- Active Personnel
- Total Military Assets
- Air Power
- Land Power
- Naval Power
- Overall Military Strength Profile

---

# Power Comparison

The Power Comparison page allows side-by-side comparison between two countries.

## How to Use

1. Select Country 1.
2. Select Country 2.
3. Review the KPI cards and comparison chart.

The comparison includes:

- Global Power Rank
- Power Index
- Active Personnel
- Military Aircraft
- Naval Fleet
- Defense Budget

The comparison chart uses normalized values so that metrics with different scales can be visually compared.

---

# Coalition Builder

The Coalition Builder allows multiple countries to be combined into a coalition.

## How to Use

1. Select one or more countries from the Coalition selector.
2. Their military metrics are automatically aggregated.
3. Select a Reference Country.
4. Compare the coalition against the selected country.

The coalition analysis includes:

- Combined Active Personnel
- Combined Military Aircraft
- Combined Naval Fleet
- Combined Defense Budget

The comparison chart provides a normalized visual comparison between the coalition and the reference country.

---

# Tips

- Use dropdown selectors to change countries.
- Multiple countries can be selected in the Coalition Builder.
- The Coalition and Reference Country selectors operate independently.
- Use the navigation buttons to move between dashboard pages.
- Clear slicers to reset selections.

---

# Troubleshooting

## Dashboard shows blank values

Check whether a valid country has been selected.

## Dataset path error

If Power BI cannot locate the dataset:

1. Open Power BI.
2. Go to Transform Data.
3. Open Data Source Settings.
4. Update the source path to the available `military_final.xlsx` file.
5. Refresh the data.

## Dashboard does not update

Try refreshing the report data using:

Home → Refresh

---

# Dashboard Pages

Quick Stats → High-level global overview

Nation Overview → Detailed profile of one country

Power Comparison → Side-by-side comparison of two countries

Coalition Builder → Combined analysis of multiple countries against a reference country