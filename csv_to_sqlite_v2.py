import os
import re
import sqlite3
import pandas as pd
from sqlalchemy import types # Import SQLAlchemy types

# --- CONFIG ---
csv_folder = "./data_files"           # folder containing CSV files
output_folder = "./database"     # folder to save the .db file
db_name = "production.db"                # name of the SQLite database file
# --------------

# --- DATA TYPE SCHEMA (YOUR CUSTOMIZATION GOES HERE) ---
# Define the desired SQL data types for columns in specific tables.
# Keys are the SANITIZED table names. Values are dictionaries
# mapping column names to SQLAlchemy types.
SCHEMA_CONFIG = {
    'cheese_production': {
        'Year': types.Integer(),
        'Period': types.TEXT(),
        'Geo_Level': types.TEXT(),
        'State_ANSI': types.INTEGER(), # Note: INTEGER is a synonym for Integer
        'Commodity_ID': types.INTEGER(), # Corrected typo from Comodity_ID
        'Domain': types.TEXT(),
        'Value': types.INTEGER()
    },
    'coffe_production': {
        'Year': types.Integer(),
        'Period': types.TEXT(),
        'Geo_Level': types.TEXT(),
        'State_ANSI': types.INTEGER(),
        'Commodity_ID': types.INTEGER(),
        'Value': types.INTEGER()
    },
    'egg_production':{
        'Year': types.Integer(),
        'Period': types.TEXT(),
        'Geo_Level': types.TEXT(),
        'State_ANSI': types.INTEGER(),
        'Commodity_ID': types.INTEGER(),
        'Value': types.INTEGER()
    },
    'honey_production':{
        'Year': types.Integer(),
        'Geo_Level': types.TEXT(),
        'State_ANSI': types.INTEGER(),
        'Commodity_ID': types.INTEGER(),
        'Value': types.INTEGER()
    },
    'milk_production': {
        'Year': types.Integer(),
        'Period': types.TEXT(),
        'Geo_Level': types.TEXT(),
        'State_ANSI': types.INTEGER(),
        'Commodity_ID': types.INTEGER(),
        'Domain': types.TEXT(),
        'Value': types.INTEGER()
    },
    'state_lookup':{
        'State': types.TEXT(),
        'State_ANSI': types.INTEGER()
    },
    'yogurt_production': {
        'Year': types.Integer(),
        'Period': types.TEXT(),
        'Geo_Level': types.TEXT(),
        'State_ANSI': types.INTEGER(),
        'Commodity_ID': types.INTEGER(),
        'Domain': types.TEXT(),
        'Value': types.INTEGER()
    }
}

# Make sure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Path to the SQLite database
db_path = os.path.join(output_folder, db_name)

# Create a connection to the SQLite database
conn = sqlite3.connect(db_path)

def sanitize_table_name(name: str) -> str:
    # (Your sanitize function remains the same)
    name = name.lower()
    name = re.sub(r'[^a-z0-9]', '_', name)
    if not re.match(r'^[a-z]', name):
        name = "t_" + name
    return name

# Loop through CSV files and add each as a table
for filename in os.listdir(csv_folder):
    if filename.lower().endswith(".csv"):
        csv_path = os.path.join(csv_folder, filename)
        
        # Sanitize table name from filename
        table_name = sanitize_table_name(os.path.splitext(filename)[0])
        
        print(f"Processing {filename} for table '{table_name}'...")
        
        # Read CSV into DataFrame
        df = pd.read_csv(csv_path)

        # --- SPECIAL HANDLING FOR DATES (VERY IMPORTANT) ---
        # If the table is in our schema and has a DateTime column, convert it first.
        if table_name in SCHEMA_CONFIG:
            table_schema = SCHEMA_CONFIG[table_name]
            for col_name, col_type in table_schema.items():
                if isinstance(col_type, types.DateTime) and col_name in df.columns:
                    # Convert the column to datetime objects in pandas
                    df[col_name] = pd.to_datetime(df[col_name])
                    print(f"  - Converted column '{col_name}' to datetime.")
        
        # Look up the schema for the current table
        dtype_mapping = SCHEMA_CONFIG.get(table_name)

        # Write to SQLite, applying the specific dtype mapping if it exists
        df.to_sql(
            table_name, 
            conn, 
            if_exists="replace", 
            index=False,
            dtype=dtype_mapping  # This is the key parameter!
        )
        
        if dtype_mapping:
            print(f"  - Applied custom schema to table '{table_name}'.")
        else:
            print(f"  - No custom schema found for '{table_name}', using default types.")

# Commit and close connection
conn.commit()
conn.close()

print(f"✅ All CSVs added to {db_path}")