#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('pip', 'install openpyxl')


# In[2]:


import pandas as pd
import numpy as np

pd.set_option("display.max_columns", None)

print("Libraries imported successfully!")


# In[4]:


from pathlib import Path

csv_file = list(Path(".").glob("military_cleaned*.csv"))[0]

df = pd.read_csv(csv_file)
reference = pd.read_excel(
    "military_final.xlsx",
    sheet_name="Wide_Format"
)

print("Files loaded successfully!")
print("Countries:", df.shape[0])
print("Columns:", df.shape[1])

df.head()


# In[5]:


from pathlib import Path

csv_file = list(Path(".").glob("military_cleaned*.csv"))[0]

df = pd.read_csv(csv_file)

reference = pd.read_excel(
    "military_final.xlsx",
    sheet_name="Wide_Format"
)

print("Files loaded successfully!")
print("Cleaned data:", df.shape)
print("Reference data:", reference.shape)

df.head()


# In[6]:


from pathlib import Path

csv_file = list(Path(".").glob("military_cleaned*.csv"))[0]

df = pd.read_csv(csv_file)

reference = pd.read_excel(
    "military_final.xlsx",
    sheet_name="Wide_Format"
)

print("Files loaded successfully!")
print("Cleaned data:", df.shape)
print("Reference data:", reference.shape)

df.head()


# In[7]:


metadata_columns = [
    "country_name",
    "iso3_code",
    "region",
    "continent",
    "alliance",
    "nato_flag",
    "power_index",
    "power_index_rank",
    "nominal_gdp_usd",
    "gdp_year",
    "gdp_basis"
]

df = df.merge(
    reference[metadata_columns],
    on="country_name",
    how="left"
)

print("Metadata added successfully!")
df[
    ["country_name", "region", "continent", "alliance", "nato_flag"]
].head()


# In[8]:


asset_columns = [
    "total_military_aircraft",
    "tanks",
    "armored_fighting_vehicles",
    "self_propelled_artillery",
    "towed_artillery",
    "rocket_projectors",
    "total_naval_fleet"
]

df["total_assets"] = df[asset_columns].fillna(0).sum(axis=1)

print("Total Assets calculated successfully!")

df[
    ["country_name", "total_assets"]
].head()


# In[9]:


df["gdp_rank"] = df["nominal_gdp_usd"].rank(
    ascending=False,
    method="min"
).astype(int)

df["power_index_rank_gap"] = (
    df["gdp_rank"] - df["power_index_rank"]
)

print("Power Index Rank Gap calculated successfully!")

df[
    [
        "country_name",
        "gdp_rank",
        "power_index_rank",
        "power_index_rank_gap"
    ]
].head()


# In[11]:


df["assets_rank"] = df["total_assets"].rank(

    ascending=False,
    method="min"
).astype(int)

df["assets_per_capita"] = (
    df["total_assets"] / df["total_population"]
)

print("Assets per Capita calculated successfully!")

df[
    [
        "country_name",
        "total_assets",
        "total_population",
        "assets_per_capita"
    ]
].head()


# In[12]:


df["budget_to_gdp_ratio"] = (
    df["defense_budget_usd"] / df["nominal_gdp_usd"]
)

print("Budget-to-GDP Ratio calculated successfully!")

df[[
    "country_name",
    "defense_budget_usd",
    "nominal_gdp_usd",
    "budget_to_gdp_ratio"
]].head()


# In[13]:


df.replace([np.inf, -np.inf], np.nan, inplace=True)

df.sort_values(
    "country_name",
    key=lambda x: x.str.lower(),
    inplace=True
)

df.reset_index(drop=True, inplace=True)

print("Data cleaned and sorted successfully!")

df[[
    "country_name",
    "power_index_rank_gap",
    "assets_per_capita",
    "budget_to_gdp_ratio"
]].head()


# In[14]:


id_columns = [
    "country_name",
    "iso3_code",
    "region",
    "continent",
    "alliance",
    "nato_flag"
]

kpi_columns = [
    "power_index",
    "power_index_rank",
    "gdp_rank",
    "power_index_rank_gap",
    "total_assets",
    "assets_rank",
    "assets_per_capita",
    "budget_to_gdp_ratio"
]

long_df = df[id_columns + kpi_columns].melt(
    id_vars=id_columns,
    var_name="kpi_name",
    value_name="kpi_value"
)

print("Long Format created successfully!")
print("Rows:", len(long_df))

long_df.head()


# In[15]:


definitions = pd.DataFrame({
    "KPI": [
        "Power Index Rank Gap",
        "Assets per Capita",
        "Budget-to-GDP Ratio",
        "NATO Flag"
    ],
    "Formula": [
        "GDP Rank - Power Index Rank",
        "Total Assets / Total Population",
        "Defense Budget / Nominal GDP",
        "1 = NATO, 0 = Non-NATO"
    ]
})

print("KPI Definitions created successfully!")

definitions


# In[16]:


with pd.ExcelWriter(
    "military_final.xlsx",
    engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        sheet_name="Wide_Format",
        index=False
    )

    long_df.to_excel(
        writer,
        sheet_name="Long_Format",
        index=False
    )

    definitions.to_excel(
        writer,
        sheet_name="KPI_Definitions",
        index=False
    )

print("military_final.xlsx saved successfully!")


# In[17]:


check_wide = pd.read_excel(
    "military_final.xlsx",
    sheet_name="Wide_Format"
)

check_long = pd.read_excel(
    "military_final.xlsx",
    sheet_name="Long_Format"
)

print("Wide Format:", check_wide.shape)
print("Long Format:", check_long.shape)

print("All KPIs Present:", all(col in check_wide.columns for col in [
    "power_index_rank_gap",
    "assets_per_capita",
    "budget_to_gdp_ratio"
]))

print("Metadata Present:", all(col in check_wide.columns for col in [
    "region",
    "continent",
    "alliance",
    "nato_flag"
]))


# In[ ]:




