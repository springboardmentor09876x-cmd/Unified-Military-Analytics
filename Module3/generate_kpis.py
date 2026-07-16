######      MODULE-3 : KPI Feature Engineering    ########
#importing the required libraries
import pandas as pd
import numpy as np

df=pd.read_csv("C:\\Users\\hirai\\Desktop\\Unified-Military-Analytics\\Module2\\military_cleaned.csv")
print(df.shape)
print(df.head(10))

#-----------------------Computing the KPIs--------------------

#KPI-1: Power Index Rank Gap
print("Missing values : " + str(df["power_index_rank"].isnull().sum()))
df["power_index_rank_gap"]=df["power_index_rank"]-1  
#print(df[["country", "power_index_rank", "power_index_rank_gap"]].head(10))

#KPI-2:Assets per Capita
df["total_assets"] = (df["total_aircraft"] + df["tanks"] + df["total_naval_fleet"])
df["assets_per_capita"] = (df["total_assets"] / df["total_population"])
#print(df[["country", "total_assets", "assets_per_capita"]].head(10))

#KPI-3:Budget-to-GDP Ratio
df["budget_to_gdp_ratio"] = (df["defense_budget_usd"] / df["gdp"]) * 100
print(df[["country", "power_index_rank_gap", "total_assets", "assets_per_capita", "budget_to_gdp_ratio"]].head(10))


#----------------------Create long format--------------
long_df = df.melt( id_vars=["country","continent","region","nato_member"],    
                  value_vars=["power_index_rank_gap", "assets_per_capita", "budget_to_gdp_ratio"],
                  var_name="KPI",value_name="Value" )  #melt() reshapes the dataframe


#------------------Exporting the dataframes to an Excel file-----------------
with pd.ExcelWriter("military_final.xlsx") as writer:
    df.to_excel(writer, sheet_name="Wide_Format", index=False)
    long_df.to_excel(writer, sheet_name="Long_Format", index=False)
print("military_final.xlsx created successfully.")


                           






