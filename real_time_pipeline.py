import os
import glob
import sqlite3
import pandas as pd
import schedule
import time
from datetime import datetime

# Paths configuration
DB_PATH = "ecommerce.db"
INCOMING_FOLDER = "incoming_stream/"

def process_real_time_stream():
    print(f"\n[{datetime.now()}] Checking for incoming real-time data files...")
    
    # Find any new CSV files dropped into the stream folder
    search_path = os.path.join(INCOMING_FOLDER, "*.csv")
    files = glob.glob(search_path)
    
    if not files:
        print("No new data files found. Standing by...")
        return

    conn = sqlite3.connect(DB_PATH)

    for file_path in files:
        print(f"Processing new file: {os.path.basename(file_path)}")
        
        # 1. Read incoming stream chunk
        df_new = pd.read_csv(file_path)
        
        # 2. Data Cleaning / Transformation Step
        df_new.dropna(subset=['order_id', 'customer_id'], inplace=True)
        if 'price' in df_new.columns:
            df_new['price'] = pd.to_numeric(df_new['price'], errors='coerce')
        
        # 3. Incremental Load: Append new rows directly to SQLite table
        df_new.to_sql('ecommerce_master_clean', conn, if_exists='append', index=False)
        print(f"Successfully appended {len(df_new)} rows into SQLite database.")
        
        # 4. Move processed file to archive so it isn't processed twice
        archive_folder = os.path.join(INCOMING_FOLDER, "archive/")
        os.makedirs(archive_folder, exist_ok=True)
        os.rename(file_path, os.path.join(archive_folder, os.path.basename(file_path)))

    conn.close()
    print("Pipeline execution complete. Database updated.")

# Schedule the pipeline to check every 1 minute
schedule.every(1).minutes.do(process_real_time_stream)

print("--- Real-Time Data Pipeline Initialized ---")
print("Listening for incoming streams... Press Ctrl+C to stop.")

# Keep the script running continuously
while True:
    schedule.run_pending()
    time.sleep(1)