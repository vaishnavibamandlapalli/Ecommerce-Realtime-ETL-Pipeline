import sqlite3
import pandas as pd

# 1. Connect to your SQLite database
conn = sqlite3.connect("ecommerce.db")

# 2. Query the master clean table containing all historical and real-time batches
query = "SELECT * FROM ecommerce_master_clean"
df = pd.read_sql(query, conn)

# 3. Export the dataframe to a clean CSV file for Power BI
output_file = "powerbi_ready_data.csv"
df.to_csv(output_file, index=False)

# 4. Close the connection
conn.close()

print(f"Successfully exported {len(df)} rows to '{output_file}' for Power BI!")