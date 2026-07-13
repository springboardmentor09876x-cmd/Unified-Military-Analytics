import pandas as pd
import re

df = pd.read_csv("data/military_raw_data.csv")
print(df.columns)
df.rename(columns={
    "Country": "country"
}, inplace=True)
print(df.columns)
def clean_number(value):

    if pd.isna(value):
        return value

    value = str(value)

    # Keep only the value before "("
    value = value.split("(")[0]

    # Remove common text
    value = value.replace(",", "")
    value = value.replace("$", "")
    value = value.replace("USD", "")
    value = value.replace("km", "")
    value = value.replace("BBL", "")
    value = value.replace("cu.m", "")
    value = value.replace("mt", "")
    value = value.replace("Stock:", "")
    value = value.replace("Readiness:", "")
    value = value.replace("*", "")

    return value.strip()
for col in df.columns:
    if col != "country":
        df[col] = df[col].apply(clean_number)
print(df.head())

numeric_columns = [col for col in df.columns if col != "country"]
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")
print(df.dtypes)

naval_columns = [
    "aircraft_carriers",
    "helicopter_carriers",
    "destroyers",
    "frigates",
    "corvettes",
    "submarines",
    "coastal_patrol_craft",
    "mine_warfare_craft"
]

df[naval_columns] = df[naval_columns].fillna(0)
print(df.isnull().sum())

df = df.drop_duplicates(subset=["country"])
print(len(df))

df.to_csv("military_cleaned.csv", index=False)

print("Module 2 Completed Successfully!")