import os
import re
import sqlite3
import pandas as pd
from sqlalchemy import types, create_engine

# --- CONFIG ---
csv_folder = "./data_files"
output_folder = "./database"
db_name = "production3.db"
# --------------

# --- DATA TYPE SCHEMA ---
SCHEMA_CONFIG = {
    # (Your schema remains the same, it's correct)
    'cheese_production': { 'Year': types.Integer(), 'Period': types.TEXT(), 'Geo_Level': types.TEXT(), 'State_ANSI': types.INTEGER(), 'Commodity_ID': types.INTEGER(), 'Domain': types.TEXT(), 'Value': types.INTEGER() },
    'coffe_production': { 'Year': types.Integer(), 'Period': types.TEXT(), 'Geo_Level': types.TEXT(), 'State_ANSI': types.INTEGER(), 'Commodity_ID': types.INTEGER(), 'Value': types.INTEGER() },
    'egg_production':{ 'Year': types.Integer(), 'Period': types.TEXT(), 'Geo_Level': types.TEXT(), 'State_ANSI': types.INTEGER(), 'Commodity_ID': types.INTEGER(), 'Value': types.INTEGER() },
    'honey_production':{ 'Year': types.Integer(), 'Geo_Level': types.TEXT(), 'State_ANSI': types.INTEGER(), 'Commodity_ID': types.INTEGER(), 'Value': types.INTEGER() },
    'milk_production': { 'Year': types.Integer(), 'Period': types.TEXT(), 'Geo_Level': types.TEXT(), 'State_ANSI': types.INTEGER(), 'Commodity_ID': types.INTEGER(), 'Domain': types.TEXT(), 'Value': types.INTEGER() },
    'state_lookup':{ 'State': types.TEXT(), 'State_ANSI': types.INTEGER() },
    'yogurt_production': { 'Year': types.Integer(), 'Period': types.TEXT(), 'Geo_Level': types.TEXT(), 'State_ANSI': types.INTEGER(), 'Commodity_ID': types.INTEGER(), 'Domain': types.TEXT(), 'Value': types.INTEGER() }
}

# --- SCRIPT START ---
os.makedirs(output_folder, exist_ok=True)
db_path = os.path.join(output_folder, db_name)
engine = create_engine(f'sqlite:///{db_path}')

def sanitize_table_name(name: str) -> str:
    name = name.lower()
    name = re.sub(r'[^a-z0-9]', '_', name)
    if not re.match(r'^[a-z]', name):
        name = "t_" + name
    return name

for filename in os.listdir(csv_folder):
    if filename.lower().endswith(".csv"):
        csv_path = os.path.join(csv_folder, filename)
        table_name = sanitize_table_name(os.path.splitext(filename)[0])
        print(f"Processing {filename} for table '{table_name}'...")
        
        try:
            # We still use thousands=',' as a first-pass optimization
            df = pd.read_csv(csv_path, thousands=',')
        except Exception as e:
            print(f"  - ERROR: Could not read {filename}. Error: {e}")
            continue

        # --- ROBUST CLEANING BLOCK FOR 'Value' COLUMN ---
        if 'Value' in df.columns:
            print("  - Applying robust cleaning to 'Value' column...")
            df['Value'] = df['Value'].astype(str).str.replace(',', '', regex=False)
            df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
            df['Value'] = df['Value'].fillna(0)
            df['Value'] = df['Value'].astype('Int64')
        # --- END OF NEW BLOCK ---

        if table_name in SCHEMA_CONFIG:
            table_schema = SCHEMA_CONFIG[table_name]
            for col_name, col_type in table_schema.items():
                if isinstance(col_type, types.DateTime) and col_name in df.columns:
                    df[col_name] = pd.to_datetime(df[col_name])
                    print(f"  - Converted column '{col_name}' to datetime.")

        dtype_mapping = SCHEMA_CONFIG.get(table_name)

        df.to_sql(
            table_name, 
            engine, 
            if_exists="replace", 
            index=False,
            dtype=dtype_mapping
        )
        
        if dtype_mapping:
            print(f"  - Applied custom schema to table '{table_name}'.")
        else:
            print(f"  - No custom schema found for '{table_name}', using default types.")

engine.dispose()
print(f"✅ All CSVs added to {db_path} on this evening of August 15, 2025.")