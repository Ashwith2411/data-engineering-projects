# ETL Pipeline: Extract, Transform, Load

# Step 1: Import libraries
import requests
import pandas as pd
from datetime import datetime

# Step 2: EXTRACT - Pull data from API
print("🔄 Extracting data from API...")
url = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(f"✅ Extracted {len(data)} records")
else:
    print(f"❌ API failed with status: {response.status_code}")
    exit()

# Step 3: TRANSFORM - Clean and structure data
print("🔄 Transforming data...")
df = pd.DataFrame(data)

# Clean data
df.columns = df.columns.str.upper()  # Uppercase columns
df['TITLE'] = df['TITLE'].str.title()  # Format titles

# Add timestamp
df['LOAD_TIMESTAMP'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(f"✅ Transformed {len(df)} records")

# Step 4: LOAD - Save to CSV
print("🔄 Loading data...")
filename = f"api_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
df.to_csv(filename, index=False)
print(f"✅ Loaded data to {filename}")

# Step 5: Display summary
print("\n📊 Data Summary:")
print(f"Total Records: {len(df)}")
print(f"Columns: {list(df.columns)}")
print("\nFirst 5 records:")
print(df.head())