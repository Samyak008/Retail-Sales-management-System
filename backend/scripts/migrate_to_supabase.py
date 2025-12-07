"""
Migration script to upload CSV data to Supabase.

Prerequisites:
1. Create a Supabase project at https://supabase.com
2. Create a table named 'sales' with the appropriate schema
3. Set environment variables:
   - SUPABASE_URL=your_project_url
   - SUPABASE_KEY=your_service_role_key

Run this script once to populate the database:
    python -m backend.scripts.migrate_to_supabase
"""

import os
import sys
from pathlib import Path

import pandas as pd
from supabase import create_client, Client

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.app.data_loader import DATA_FILENAME, COLUMN_MAP


def get_supabase_client() -> Client:
    """Create and return Supabase client."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables must be set")
    
    return create_client(url, key)


def load_csv() -> pd.DataFrame:
    """Load and standardize CSV data."""
    csv_path = Path(__file__).resolve().parents[2] / DATA_FILENAME
    
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found at {csv_path}")
    
    print(f"Loading CSV from {csv_path}...")
    df = pd.read_csv(csv_path, low_memory=False)
    
    # Standardize column names
    rename_map = {}
    for col in df.columns:
        if col in COLUMN_MAP:
            rename_map[col] = COLUMN_MAP[col]
        else:
            cleaned = col.strip().lower().replace(" ", "_")
            rename_map[col] = cleaned
    
    df = df.rename(columns=rename_map)
    
    # Convert dates
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    
    # Fill NaN values
    df = df.fillna({
        "tags": "",
        "customer_name": "",
        "phone_number": "",
    })
    
    # Convert to appropriate types
    for col in df.select_dtypes(include=["float64"]).columns:
        if df[col].isna().sum() == 0:
            df[col] = df[col].astype(int)
    
    print(f"Loaded {len(df)} rows")
    return df


def create_table_sql() -> str:
    """Return SQL to create the sales table."""
    return """
    CREATE TABLE IF NOT EXISTS sales (
        transaction_id TEXT PRIMARY KEY,
        date DATE,
        customer_id TEXT,
        customer_name TEXT,
        phone_number TEXT,
        gender TEXT,
        age INTEGER,
        customer_region TEXT,
        customer_type TEXT,
        product_id TEXT,
        product_name TEXT,
        brand TEXT,
        product_category TEXT,
        tags TEXT,
        quantity INTEGER,
        price_per_unit NUMERIC,
        discount_percentage NUMERIC,
        total_amount NUMERIC,
        final_amount NUMERIC,
        payment_method TEXT,
        order_status TEXT,
        delivery_type TEXT,
        store_id TEXT,
        store_location TEXT,
        salesperson_id TEXT,
        employee_name TEXT
    );
    
    -- Create indexes for common queries
    CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(date);
    CREATE INDEX IF NOT EXISTS idx_sales_customer_region ON sales(customer_region);
    CREATE INDEX IF NOT EXISTS idx_sales_product_category ON sales(product_category);
    CREATE INDEX IF NOT EXISTS idx_sales_customer_name ON sales(customer_name);
    """


def upload_to_supabase(df: pd.DataFrame, batch_size: int = 1000):
    """Upload DataFrame to Supabase in batches."""
    client = get_supabase_client()
    
    print("\nNote: You need to create the 'sales' table in Supabase first.")
    print("Run this SQL in your Supabase SQL editor:")
    print(create_table_sql())
    print("\nPress Enter to continue after creating the table, or Ctrl+C to exit...")
    input()
    
    # Convert DataFrame to list of dicts
    records = df.to_dict(orient="records")
    total_records = len(records)
    
    print(f"\nUploading {total_records} records in batches of {batch_size}...")
    
    for i in range(0, total_records, batch_size):
        batch = records[i:i + batch_size]
        try:
            client.table("sales").insert(batch).execute()
            print(f"Uploaded batch {i // batch_size + 1}: {i + len(batch)}/{total_records} records")
        except Exception as e:
            print(f"Error uploading batch {i // batch_size + 1}: {e}")
            print("Continuing with next batch...")
    
    print("\n✅ Migration complete!")


def main():
    """Main migration function."""
    print("Starting CSV to Supabase migration...")
    
    try:
        df = load_csv()
        upload_to_supabase(df)
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
