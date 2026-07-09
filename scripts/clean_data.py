import pandas as pd

print("=" * 60)
print("MILITARY DATA CLEANING")
print("=" * 60)

# -------------------------------------------------
# Load Raw Dataset
# -------------------------------------------------

input_file = "../data/military_raw_data.csv"

df = pd.read_csv(input_file)

print("Dataset Loaded Successfully.")
print("Rows :", df.shape[0])
print("Columns :", df.shape[1])

# -------------------------------------------------
# Standardize Column Names
# -------------------------------------------------

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("\nColumn names standardized.")

# -------------------------------------------------
# Clean Numeric Columns
# -------------------------------------------------

print("\nCleaning numeric columns...")

numeric_columns = df.columns.drop("country")

for col in numeric_columns:

    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.replace("+", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.replace("km", "", regex=False)
        .str.replace("Cu.M", "", regex=False)
        .str.replace("mt", "", regex=False)
        .str.replace("bbl", "", regex=False)
        .str.replace("No Data", "", regex=False)
        .str.replace("N/A", "", regex=False)
        .str.replace("-", "", regex=False)
        .str.strip()
    )

    df[col] = pd.to_numeric(df[col], errors="coerce")

print("Numeric conversion completed.")

# -------------------------------------------------
# Check Missing Values
# -------------------------------------------------

print("\nMissing values before cleaning:\n")

print(df.isnull().sum())

# Fill missing numeric values with 0

df.fillna(0, inplace=True)

print("\nMissing values after cleaning:\n")

print(df.isnull().sum())

# -------------------------------------------------
# Display Data Types
# -------------------------------------------------

print("\nColumn Data Types:\n")

print(df.dtypes)

# -------------------------------------------------
# Save Clean Dataset
# -------------------------------------------------

output_file = "../data/military_cleaned.csv"

df.to_csv(
    output_file,
    index=False
)

print("\n" + "=" * 60)
print("DATA CLEANING COMPLETED")
print("=" * 60)

print("Output File :", output_file)
print("Rows        :", df.shape[0])
print("Columns     :", df.shape[1])

print("\nFirst 5 Rows:\n")

print(df.head())