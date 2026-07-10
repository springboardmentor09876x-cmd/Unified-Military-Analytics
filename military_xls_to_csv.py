print("Script started")

import pandas as pd

print("Pandas imported")

df = pd.read_excel("military_data.xls")

print("Excel file read successfully")

df.to_csv("military_data.csv", index=False)

print("CSV saved successfully")