import pandas as pd
import numpy as np
import os

def generate_kpis():
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, '..', 'Module 2', 'military_cleaned.csv')
    output_file = os.path.join(base_dir, 'military_final.xlsx')
    
    # 1. Load data
    print(f"Loading cleaned data from {input_file}...")
    df = pd.read_csv(input_file)
    
    # 2. Compute KPIs
    # Power Index Rank Gap (gap to the next highest ranked country, i.e., difference in power index)
    # Lower power index is better. We sort by power index.
    df = df.sort_values(by='power_index', ascending=True).reset_index(drop=True)
    df['power_index_rank'] = df['power_index'].rank(method='min', ascending=True)
    # Gap between current country and the country ranked immediately better than it
    df['power_index_rank_gap'] = df['power_index'].diff().fillna(0)
    
    # Assets per Capita
    # Sum of major military assets
    asset_cols = [
        'total_military_aircraft', 'total_naval_fleet', 'tanks', 
        'armored_fighting_vehicles', 'self_propelled_artillery', 
        'towed_artillery', 'rocket_projectors', 'total_military_helicopters'
    ]
    df['total_military_assets'] = df[asset_cols].sum(axis=1)
    df['assets_per_capita'] = np.where(
        df['total_population'] > 0,
        df['total_military_assets'] / df['total_population'],
        0
    )
    
    # Budget-to-GDP Ratio
    # Use gdp if available, otherwise fallback to purchasing_power_parity_usd
    df['gdp_effective'] = np.where(df['gdp'] > 0, df['gdp'], df['purchasing_power_parity_usd'])
    df['budget_to_gdp_ratio'] = np.where(
        df['gdp_effective'] > 0,
        df['defense_budget_usd'] / df['gdp_effective'],
        0
    )
    
    # 3. Enrich with metadata: region, continent, alliance flags (e.g., NATO)
    # Continent, region and alliance already exist from Module 2, let's create a specific flag for NATO
    if 'alliance' in df.columns:
        df['is_nato'] = df['alliance'].str.contains('NATO', case=False, na=False)
    else:
        # Fallback if alliance not present
        nato_countries = ["United States", "United Kingdom", "France", "Germany", 
                          "Italy", "Canada", "Turkiye", "Poland", "Spain"]
        df['is_nato'] = df['country'].isin(nato_countries)
        df['alliance'] = np.where(df['is_nato'], 'NATO', 'Unknown')
        
    if 'continent' not in df.columns:
        df['continent'] = 'Unknown'
    if 'region' not in df.columns:
        df['region'] = 'Unknown'

    # 4. Format in wide and long forms for Tableau use
    wide_df = df.copy()
    
    # Identify identifier columns and metric columns for melting
    id_vars = ['country', 'continent', 'region', 'alliance', 'is_nato']
    # Select all numeric columns as value variables, or just all other columns
    value_vars = [col for col in wide_df.columns if col not in id_vars]
    
    long_df = pd.melt(
        wide_df, 
        id_vars=id_vars, 
        value_vars=value_vars, 
        var_name='metric_name', 
        value_name='metric_value'
    )
    
    # 5. Export to Excel
    print(f"Saving final dataset to {output_file}...")
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        wide_df.to_excel(writer, sheet_name='Wide_Format', index=False)
        long_df.to_excel(writer, sheet_name='Long_Format', index=False)
        
    print("KPI generation complete. Data is ready for Tableau.")

if __name__ == "__main__":
    generate_kpis()
