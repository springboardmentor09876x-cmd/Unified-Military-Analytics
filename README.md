# Military Power Analysis Dashboard – Power BI

## 1. Project Overview

This project presents an interactive **Military Power Analysis Dashboard** developed in Microsoft Power BI. The dashboard uses structured military and country-level data to compare military capabilities, defense spending, personnel, equipment, alliances, and overall power rankings.

The project contains:

* Power BI dashboard/report (`.pbix`)
* Excel source dataset (`.xlsx`)
* Interactive filters and parameters
* Country-level military comparisons
* Coalition analysis
* KPI cards and visual analytics

The main objective is to provide an easy-to-use dashboard for exploring and comparing military strength across countries.

---

# 2. Data Source

The primary source data is stored in:

`military_final(1).xlsx`

The dataset contains country-level military information, including:

* Country
* Continent
* Region
* Alliance
* Power Index Rank
* Defense Budget
* Military Personnel
* Military Equipment
* Land forces
* Naval forces
* Air forces
* Other military capability indicators

The Excel file contains **145 unique countries and 69 columns** based on the supplied project files.

The Power BI report uses this Excel dataset as its underlying data source.

---

# 3. Data Preparation / Scraping Method

The project follows a structured data collection and preparation process.

### Step 1 – Data Collection

Military-related country information is collected from publicly available structured sources and compiled into a common dataset.

### Step 2 – Data Cleaning

The collected data is cleaned before being imported into Power BI.

Typical cleaning operations include:

* Removing duplicate country records
* Standardizing country names
* Standardizing continent and region names
* Standardizing alliance names
* Handling missing values
* Converting numeric fields into appropriate numeric data types
* Converting budget and personnel fields into usable measures
* Checking country-level uniqueness

### Step 3 – Data Structuring

The cleaned information is organized into the Excel dataset:

`military_final(1).xlsx`

Each row represents a country and the columns contain its military-related attributes.

### Step 4 – Power BI Import

The cleaned Excel dataset is imported into Power BI.

Power BI is then used to:

* Create relationships/model structures where required
* Create calculated measures
* Build KPIs
* Configure slicers and parameters
* Create charts and comparison visuals
* Design interactive dashboards

### Step 5 – Validation

The dashboard values are manually spot-checked against the Excel source to verify that rankings, budgets, personnel values, and other displayed metrics are consistent with the underlying data.

---

# 4. Power BI Dashboard Structure

The supplied Power BI file contains four main dashboard pages.

## 4.1 Quick Stats

The **Quick Stats** dashboard provides a high-level overview of military power.

It includes controls for:

* Region
* Continent
* Alliance
* Country

It provides summary KPIs and charts for quickly exploring military strength.

A Top-10 analysis is also used for regional defense-budget comparison.

---

## 4.2 Nation Overview

The **Nation Overview** dashboard focuses on an individual country.

The main control is a country selector.

The default country in the supplied Power BI file is:

**Russia**

The dashboard provides country-level information such as:

* Military power ranking
* Defense budget
* Military personnel
* Military hardware
* Other country-level military indicators

Users can change the selected country to analyze another nation.

---

## 4.3 Compare Powers

The **Compare Powers** dashboard allows two countries to be compared directly.

The supplied report uses:

* **Country 1:** India
* **Country 2:** China

as the default selections.

Users can change both selections to compare different countries.

The comparison includes military indicators such as:

* Power ranking
* Defense spending
* Personnel
* Military capabilities
* Other available military metrics

This dashboard is designed to make differences between two countries easy to identify.

---

## 4.4 Coalition Builder

The **Coalition Builder** dashboard allows users to construct a group of countries and compare the resulting coalition against a reference country.

The supplied default coalition contains:

* France
* India
* Japan
* Afghanistan

The default reference country is:

**Algeria**

The coalition selector supports multiple country selections and includes a **Select All** capability.

Users can:

1. Add countries to the coalition.
2. Remove countries from the coalition.
3. Select all available countries.
4. Change the reference country.
5. Compare coalition-level military indicators against the selected reference country.

---

# 5. KPI Definitions

The following definitions should be used when interpreting the dashboard.

## Power Index Rank

The **Power Index Rank** represents the relative military position of a country in the dataset.

A lower numerical rank indicates a stronger position.

For example:

* Rank 1 = strongest position
* Rank 2 = second position
* Rank 10 = tenth position

The rank should therefore not be interpreted as a score where a higher number means greater strength.

---

## Defense Budget

**Defense Budget** represents the reported military/defense expenditure for the country.

It is used to compare the financial resources allocated to defense.

The dashboard may aggregate or compare defense budgets depending on the selected countries, regions, or coalition members.

---

## Military Personnel

**Military Personnel** represents the number of military personnel associated with the country in the source dataset.

This KPI is used to compare the size of military manpower between countries.

---

## Military Hardware

**Military Hardware** represents the available military equipment/capability information captured in the source dataset.

Depending on the visualization, this may be represented through equipment categories such as:

* Aircraft
* Tanks
* Naval assets
* Armored vehicles
* Artillery
* Other military equipment

---

## Country

The **Country** field identifies the nation represented by each record in the dataset.

Country selection is used throughout the dashboards to filter the displayed military information.

---

## Region

The **Region** field groups countries geographically.

It is used to analyze military indicators at a regional level.

---

## Continent

The **Continent** field groups countries by continent.

It allows users to analyze and compare military indicators across broader geographic areas.

---

## Alliance

The **Alliance** field identifies the military/political alliance associated with a country in the dataset.

It can be used as a dashboard filter to compare groups of countries.

---

# 6. Dashboard Filters and Parameters

The Power BI report contains multiple interactive controls.

### Quick Stats

Available controls include:

* Region
* Continent
* Alliance
* Country

### Nation Overview

* Country selector

### Compare Powers

* Country 1 selector
* Country 2 selector

### Coalition Builder

* Multi-select coalition selector
* Reference country selector

The controls allow users to dynamically change the information displayed in the charts and KPI cards.

---

# 7. How to Open the Power BI File

## Requirements

To open the Power BI report, install **Microsoft Power BI Desktop**.

The main report file is the `.pbix` file supplied with this project.

### Opening the report

1. Install Power BI Desktop.
2. Download/locate the supplied `.pbix` file.
3. Open the `.pbix` file using Power BI Desktop.
4. If Power BI asks for permission to access the Excel source, allow access.
5. Verify that the Excel source path is available.
6. Select **Refresh** if the data needs to be updated.
7. Navigate through the dashboard pages using the page navigation controls.

---

# 8. Excel Source File

The Power BI report uses the supplied Excel dataset:

`military_final(1).xlsx`

If the Excel file is moved to another location, Power BI may report that the data source cannot be found.

To update the source location:

1. Open the Power BI file.
2. Open **Transform Data** / **Power Query**.
3. Locate the Excel source.
4. Update the file path to the new location.
5. Apply the changes.
6. Refresh the report.

It is recommended to keep the `.pbix` file and Excel source file in the same project folder when distributing the project.

---

# 9. How to Use the Dashboard

### Step 1 – Select a Dashboard

Use the navigation buttons to open:

* Quick Stats
* Nation Overview
* Compare Powers
* Coalition Builder

### Step 2 – Apply Filters

Select values from the available slicers.

For example, users can select:

* A continent
* A region
* An alliance
* A country

The dashboard visuals should update automatically.

### Step 3 – Compare Countries

Open **Compare Powers** and select two countries.

The dashboard will update to show their relative military characteristics.

### Step 4 – Build a Coalition

Open **Coalition Builder**.

Select multiple countries to create a coalition and select a reference country for comparison.

### Step 5 – Explore Visuals

Hover over charts and data points to view available tooltips.

Use the displayed KPI cards for quick summary information.

---

# 10. Recommended User Workflow

For the best experience, use the dashboard in the following order:

**Quick Stats → Nation Overview → Compare Powers → Coalition Builder**

Start with Quick Stats to understand overall patterns.

Then select an individual country in Nation Overview.

Next, compare two countries using Compare Powers.

Finally, use Coalition Builder to analyze groups of countries.

---

# 11. Data Validation

The supplied project data was checked against the Excel source during QA.

The following were specifically verified:

* Country records
* Country names used by dashboard selectors
* Power Index rankings
* Defense-budget rankings
* Default country selections
* Default comparison countries
* Default coalition members
* Default reference country

The supplied report contains:

* **145 unique countries**
* **69 data columns**
* **4 Power BI dashboard pages**
* **9 detected slicer/parameter controls**

The default dashboard selections identified in the report are:

| Dashboard                     | Default Selection                 |
| ----------------------------- | --------------------------------- |
| Nation Overview               | Russia                            |
| Compare Powers – Country 1    | India                             |
| Compare Powers – Country 2    | China                             |
| Coalition Builder             | France, India, Japan, Afghanistan |
| Coalition Builder – Reference | Algeria                           |

---

# 12. Known QA / Runtime Checks

File-level analysis verifies the report structure and source data, but some functionality must be tested directly in Power BI Desktop or Power BI Service.

Before final release, verify:

* All slicers respond correctly.
* Multi-select controls work correctly.
* Select All works correctly.
* Filters update all intended visuals.
* Country comparisons update correctly.
* Coalition totals update after adding/removing countries.
* Navigation buttons work.
* Tooltips display the correct values.
* Labels and titles are correct.
* Number formats are correct.
* No visual objects overlap or become clipped.
* Refresh completes without errors.
* No broken data-source paths exist.
* The report performs smoothly.
* Publishing does not create broken visuals or missing data.

---

# 13. GitHub Repository Structure

A recommended repository structure is:

```text
military-power-analysis/
│
├── README.md
│
├── PowerBI/
│   └── military_power_dashboard.pbix
│
├── Data/
│   └── military_final(1).xlsx
│
├── Documentation/
│   ├── QA_Checklist.pdf
│   ├── QA_Checklist.xlsx
│   └── Project_Documentation.pdf
│
└── Screenshots/
    ├── quick_stats.png
    ├── nation_overview.png
    ├── compare_powers.png
    └── coalition_builder.png
```

---

# 14. GitHub Release Instructions

Before uploading the project:

1. Confirm the final Power BI file opens correctly.
2. Confirm the Excel source is included or its location is documented.
3. Complete the QA checklist.
4. Remove temporary/development files.
5. Add this README.md file.
6. Add screenshots of the completed dashboards.
7. Upload the project files to GitHub.
8. Add a meaningful repository description.
9. Create a release/tag for the final version.

Example release name:

**v1.0 – Final Military Power Analysis Dashboard**

---

# 15. Project Deliverables

The final project should contain:

* Final Power BI `.pbix` dashboard
* Clean Excel source dataset
* README documentation
* QA checklist
* Dashboard screenshots
* GitHub repository
* Final GitHub release

---

# 16. Conclusion

The Military Power Analysis Dashboard provides an interactive way to explore military strength across countries using defense spending, personnel, equipment, rankings, geographic groupings, alliances, country comparisons, and coalition analysis.

The Power BI report is designed to allow users to move from high-level military statistics to individual country analysis, direct country comparisons, and customized coalition analysis.

The supplied Power BI and Excel files should be kept together when opening the project to avoid data-source path errors.

For the final release, the report should be opened and refreshed in Power BI Desktop, all interactive controls should be tested, and the completed project should then be uploaded to GitHub together with this README and the supporting documentation.
