import pandas as pd
df = pd.read_csv("military_data.csv")
print(df.head())
print(df.info())
print(df.describe(include='all'))  #to check if there are anything missing?

print(df.isnull().sum())   #to check how many null values are there

print(df.dtypes) #to check the data types

#df["total_population"] = pd.to_numeric(df["total_population"])     # Converts numeric strings into actual numeric values

for column in df.columns[1:]:  # Loop through every numeric column except Country

    #df[column] = df[column].str.replace(",","")     #used to remove the commas which numbers are labbled as string

    df[column] = df[column].astype(str).str.replace(",", "")   # Convert values to string so commas can be removed safely

    df[column] = pd.to_numeric(df[column], errors="coerce") # Invalid values become NaN instead of raising an error

df.fillna(0, inplace=True)  #it turns the value from NaN to 0

print("Duplicate rows:", df.duplicated().sum())

df.to_csv("military_data_cleaned.csv", index=False)
