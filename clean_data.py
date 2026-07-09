import pandas as pd
import re

# =====================================================
# MODULE 2 - DATA CLEANING & STRUCTURING
# Input  : military_raw_data.csv
# Output : military_cleaned.csv
# =====================================================

print("=" * 60)
print("Loading Raw Dataset...")
print("=" * 60)

# Load dataset
df = pd.read_csv("military_raw_data.csv")

print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

# =====================================================
# Standardize Column Names
# =====================================================

print("\nStandardizing column names...")

df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(" ", "_", regex=False)
      .str.replace("-", "_", regex=False)
      .str.replace("/", "_", regex=False)
)

# =====================================================
# Clean Text Data
# =====================================================

print("Cleaning text values...")

def clean_text(value):

    if pd.isna(value):
        return None

    value = str(value).strip()

    # Remove commas
    value = value.replace(",", "")

    # Remove percentage
    value = value.replace("%", "")

    # Remove plus sign
    value = value.replace("+", "")

    # Remove dollar sign
    value = value.replace("$", "")

    # Remove brackets
    value = re.sub(r"[\(\)\[\]]", "", value)

    # Remove multiple spaces
    value = re.sub(r"\s+", " ", value)

    return value


for column in df.columns:
    if df[column].dtype == object:
        df[column] = df[column].apply(clean_text)

# =====================================================
# Convert Numeric Columns
# =====================================================

print("Converting numeric columns...")

# Rank should always be numeric
df["rank"] = pd.to_numeric(df["rank"], errors="coerce")

# Convert Value column only if every value is numeric
temp = pd.to_numeric(df["value"], errors="coerce")

if temp.notna().sum() == len(df):
    df["value"] = temp

# =====================================================
# Handle Missing Values
# =====================================================

print("Handling missing values...")

# Numeric columns
numeric_columns = df.select_dtypes(include=["number"]).columns

for column in numeric_columns:
    median = df[column].median()
    df[column] = df[column].fillna(median)

# Text columns
text_columns = df.select_dtypes(include=["object"]).columns

for column in text_columns:
    df[column] = df[column].fillna("Unknown")

# =====================================================
# Remove Duplicate Rows
# =====================================================

print("Removing duplicate rows...")

before = len(df)

df = df.drop_duplicates()

after = len(df)

print(f"Duplicates Removed : {before-after}")

# =====================================================
# Validate Dataset
# =====================================================

print("\nValidating dataset...")

missing_percentage = (
    df.isnull().sum().sum()
    /
    (df.shape[0] * df.shape[1])
) * 100

print(f"Missing Percentage : {missing_percentage:.2f}%")

print(f"Final Rows         : {df.shape[0]}")
print(f"Final Columns      : {df.shape[1]}")

# =====================================================
# Save Clean Dataset
# =====================================================

output_file = "military_cleaned.csv"

df.to_csv(output_file, index=False)

print("\n" + "=" * 60)
print("DATA CLEANING COMPLETED SUCCESSFULLY")
print("=" * 60)

print(f"Output File : {output_file}")

print("\nPreview:\n")
print(df.head(10))

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)