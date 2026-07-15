# Unified Military Analytics and Comparison Dashboard

## Project Overview
This project collects military data from Global Firepower, cleans the dataset, and prepares it for visualization in Tableau.

## Module 1
- Scraped military data from Global Firepower.
- Merged all metrics into a single dataset.
- Output: `military_raw_data.csv`

## Module 2
- Cleaned and structured the raw dataset.
- Converted columns to appropriate data types.
- Handled missing values.
- Output: `military_cleaned.csv`

## Technologies Used
- Python
- Pandas
- BeautifulSoup
- Requests
- Jupyter Notebook
- Git & GitHub

## Project Structure
```
data/
├── military_raw_data.csv
├── military_cleaned.csv

scripts/
├── scrape_all_metrics.py
├── clean_data.ipynb
```