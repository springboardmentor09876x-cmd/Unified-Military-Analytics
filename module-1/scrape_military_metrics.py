import pandas as pd
import numpy as np
import re

# ======================================================
# LOAD MERGED DATASET
# ======================================================

print("=" * 60)
print("MILITARY DATA CLEANING STARTED")
print("=" * 60)

df = pd.read_csv("merged_military_dataset.csv")

print("\nDataset Loaded Successfully!")
print("Original Shape:", df.shape)

# ======================================================
# STANDARDIZE COLUMN NAMES
# ======================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
    .str.replace("-", "_", regex=False)
    .str.replace("/", "_", regex=False)
    .str.replace("(", "", regex=False)
    .str.replace(")", "", regex=False)
)

print("\nColumn names standardized.")

# ======================================================
# REMOVE EXTRA SPACES FROM TEXT COLUMNS
# ======================================================

text_columns = df.select_dtypes(include=["object"]).columns

for col in text_columns:
    df[col] = df[col].astype(str).str.strip()

# ======================================================
# FUNCTION TO CLEAN NUMERIC VALUES
# ======================================================

def clean_numeric(value):

    if pd.isna(value):
        return np.nan

    value = str(value)

    # Remove commas
    value = value.replace(",", "")

    # Remove percentage
    value = value.replace("%", "")

    # Remove plus sign
    value = value.replace("+", "")

    # Remove dollar symbol
    value = value.replace("$", "")

    # Remove brackets
    value = value.replace("(", "")
    value = value.replace(")", "")

    # Remove units
    value = re.sub(r"km²|sq km|km|mt|bbl|usd|cum", "", value, flags=re.IGNORECASE)

    # Remove remaining unwanted characters
    value = re.sub(r"[^\d\.\-]", "", value)

    if value == "":
        return np.nan

    return value

# ======================================================
# CLEAN ALL OBJECT COLUMNS
# ======================================================

for col in text_columns:

    if col not in ["country", "metric", "source_url", "region", "continent", "alliance", "major_ports_and_terminals"]:

        df[col] = df[col].apply(clean_numeric)

print("Special symbols removed.")

# ======================================================
# CONVERT TO NUMERIC
# ======================================================

for col in df.columns:

    if col not in [
        "country",
        "metric",
        "source_url",
        "region",
        "continent",
        "alliance",
        "major_ports_and_terminals",
    ]:

        df[col] = pd.to_numeric(df[col], errors="coerce")

print("Numeric conversion completed.")

# ======================================================
# HANDLE MISSING VALUES
# ======================================================

numeric_cols = df.select_dtypes(include=["number"]).columns

for col in numeric_cols:
    median = df[col].median()
    df[col] = df[col].fillna(median)

categorical_cols = df.select_dtypes(include=["object"]).columns

for col in categorical_cols:

    mode = df[col].mode()

    if len(mode) > 0:
        df[col] = df[col].fillna(mode[0])
    else:
        df[col] = df[col].fillna("Unknown")

print("Missing values handled.")

# ======================================================
# REMOVE DUPLICATES
# ======================================================

before = len(df)

df.drop_duplicates(inplace=True)

after = len(df)

print(f"Duplicate rows removed: {before - after}")

# ======================================================
# CHECK MISSING PERCENTAGE
# ======================================================

missing_percentage = (df.isnull().sum() / len(df)) * 100

print("\nMissing Percentage Per Column")

print(missing_percentage)

print("\nMaximum Missing Percentage:")

print(round(missing_percentage.max(), 2), "%")

# ======================================================
# SAVE CLEAN DATASET
# ======================================================

output_file = "final_military_cleaned.csv"

df.to_csv(output_file, index=False)

# ======================================================
# FINAL REPORT
# ======================================================

print("\n" + "=" * 60)
print("DATA CLEANING COMPLETED SUCCESSFULLY")
print("=" * 60)

print("Original Shape :", before)
print("Final Shape    :", df.shape)

print("\nOutput File Saved As:")
print(output_file)

print("\nFirst 5 Rows:\n")
print(df.head())

print("\nCleaning Completed Successfully!")
