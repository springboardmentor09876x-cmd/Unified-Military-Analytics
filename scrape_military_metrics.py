import pandas as pd

# ------------------------------------
# Read CSV Files
# ------------------------------------
raw_df = pd.read_csv("military_raw_data.csv")
final_df = pd.read_csv("military_final.csv")

# ------------------------------------
# Clean Column Names
# ------------------------------------
raw_df.columns = raw_df.columns.str.strip()
final_df.columns = final_df.columns.str.strip()

# ------------------------------------
# Standardize Country Names
# ------------------------------------
raw_df["Country"] = raw_df["Country"].astype(str).str.strip().str.lower()
final_df["country"] = final_df["country"].astype(str).str.strip().str.lower()

# ------------------------------------
# Merge on Country
# ------------------------------------
merged_df = pd.merge(
    raw_df,
    final_df,
    left_on="Country",
    right_on="country",
    how="left"
)

# Remove duplicate country column
merged_df.drop(columns=["country"], inplace=True)

# ------------------------------------
# Save the merged dataset
# ------------------------------------
output_file = "merged_military_dataset.csv"
merged_df.to_csv(output_file, index=False)

# ------------------------------------
# Display Results
# ------------------------------------
print("=" * 50)
print("MERGE COMPLETED SUCCESSFULLY")
print("=" * 50)
print("Raw Dataset Shape   :", raw_df.shape)
print("Final Dataset Shape :", final_df.shape)
print("Merged Dataset Shape:", merged_df.shape)
print(f"\nMerged dataset saved as '{output_file}'")

print("\nFirst 5 Rows:")
print(merged_df.head())
