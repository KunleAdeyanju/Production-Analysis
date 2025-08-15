import os
import re
import sqlite3
import pandas as pd

# --- CONFIG ---
csv_folder = "./data_files"           # folder containing CSV files
output_folder = "./database"     # folder to save the .db file
db_name = "production.db"                # name of the SQLite database file
# --------------

# Make sure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Path to the SQLite database
db_path = os.path.join(output_folder, db_name)

# Create a connection to the SQLite database
conn = sqlite3.connect(db_path)

def sanitize_table_name(name: str) -> str:
    # Lowercase the name
    name = name.lower()
    # Replace spaces and non-alphanumeric chars with underscores
    name = re.sub(r'[^a-z0-9]', '_', name)
    # Ensure it starts with a letter (prefix with 't_' if not)
    if not re.match(r'^[a-z]', name):
        name = "t_" + name
    return name

# Loop through CSV files and add each as a table
for filename in os.listdir(csv_folder):
    if filename.lower().endswith(".csv"):
        csv_path = os.path.join(csv_folder, filename)
        
        # Read CSV into DataFrame
        df = pd.read_csv(csv_path)
        
        # Sanitize table name from filename
        table_name = sanitize_table_name(os.path.splitext(filename)[0])
        
        # Write to SQLite
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        
        print(f"Added table '{table_name}' from {filename}")

# Commit and close connection
conn.commit()
conn.close()

print(f"✅ All CSVs added to {db_path}")