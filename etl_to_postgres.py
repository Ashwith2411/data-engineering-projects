# ============================================
# ETL PIPELINE: API → PostgreSQL
# ============================================

import requests
import pandas as pd
from datetime import datetime
import psycopg2
import os

# --------------------------------------------
# STEP 1: EXTRACT - Pull data from API
# --------------------------------------------
print("🔄 Extracting data from API...")

url = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(f"✅ Extracted {len(data)} records")
else:
    print(f"❌ API failed with status: {response.status_code}")
    exit()

# --------------------------------------------
# STEP 2: TRANSFORM - Clean and structure data
# --------------------------------------------
print("🔄 Transforming data...")

df = pd.DataFrame(data)

# Clean column names
df.columns = df.columns.str.upper()
df['TITLE'] = df['TITLE'].str.title()

# Add timestamp
df['LOAD_TIMESTAMP'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(f"✅ Transformed {len(df)} records")

# --------------------------------------------
# STEP 3: LOAD to PostgreSQL
# --------------------------------------------
print("🔄 Loading data to PostgreSQL...")

# Database connection details
DB_CONFIG = {
    "host": "localhost",
    "database": "data_engineering",
    "user": "postgres",
    "password": "root"  # <-- CHANGE THIS!
}

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS api_posts (
        userid INTEGER,
        id INTEGER PRIMARY KEY,
        title TEXT,
        body TEXT,
        load_timestamp TIMESTAMP
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    print("✅ Table created/verified")

    # Clear existing data (optional - for fresh load)
    cursor.execute("TRUNCATE TABLE api_posts;")
    conn.commit()

    # Insert data row by row
    print("🔄 Inserting records...")
    inserted = 0
    for _, row in df.iterrows():
        insert_query = """
        INSERT INTO api_posts (userid, id, title, body, load_timestamp)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            row['USERID'],
            row['ID'],
            row['TITLE'],
            row['BODY'],
            row['LOAD_TIMESTAMP']
        ))
        inserted += 1

    conn.commit()
    print(f"✅ Inserted {inserted} records into PostgreSQL")

    # Verify data
    cursor.execute("SELECT COUNT(*) FROM api_posts;")
    count = cursor.fetchone()[0]
    print(f"✅ Verification: {count} records in database")

    # Close connection
    cursor.close()
    conn.close()

except Exception as e:
    print(f"❌ Database error: {e}")
    exit()

# --------------------------------------------
# STEP 4: SAVE CSV (Optional)
# --------------------------------------------
print("🔄 Saving CSV backup...")
filename = f"api_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
df.to_csv(filename, index=False)
print(f"✅ Loaded data to {filename}")

# --------------------------------------------
# STEP 5: SUMMARY
# --------------------------------------------
print("\n📊 Data Summary:")
print(f"Total Records: {len(df)}")
print(f"Columns: {list(df.columns)}")
print("\nFirst 5 records:")
print(df.head())

# --------------------------------------------
# STEP 6: LOGGING
# --------------------------------------------
with open("pipeline_log.txt", "a") as log:
    log.write(f"{datetime.now()}: Loaded {len(df)} records to PostgreSQL\n")