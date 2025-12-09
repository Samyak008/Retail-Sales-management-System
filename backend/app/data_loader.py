import os
from functools import lru_cache
from pathlib import Path
from typing import Dict, Optional

import pandas as pd
from supabase import create_client, Client

# Expected column remapping to normalized snake_case names
COLUMN_MAP: Dict[str, str] = {
    "Transaction ID": "transaction_id",
    "Date": "date",
    "Customer ID": "customer_id",
    "Customer Name": "customer_name",
    "Phone Number": "phone_number",
    "Gender": "gender",
    "Age": "age",
    "Customer Region": "customer_region",
    "Customer Type": "customer_type",
    "Product ID": "product_id",
    "Product Name": "product_name",
    "Brand": "brand",
    "Product Category": "product_category",
    "Tags": "tags",
    "Quantity": "quantity",
    "Price per Unit": "price_per_unit",
    "Discount Percentage": "discount_percentage",
    "Total Amount": "total_amount",
    "Final Amount": "final_amount",
    "Date": "date",
    "Payment Method": "payment_method",
    "Order Status": "order_status",
    "Delivery Type": "delivery_type",
    "Store ID": "store_id",
    "Store Location": "store_location",
    "Salesperson ID": "salesperson_id",
    "Employee Name": "employee_name",
}

DATA_FILENAME = "truestate_assignment_dataset.csv"


@lru_cache(maxsize=1)
def get_supabase_client() -> Optional[Client]:
    """Get Supabase client if credentials are available."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if url and key:
        return create_client(url, key)
    return None


def _standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {}
    for col in df.columns:
        if col in COLUMN_MAP:
            rename_map[col] = COLUMN_MAP[col]
        else:
            cleaned = col.strip().lower().replace(" ", "_")
            rename_map[col] = cleaned
    return df.rename(columns=rename_map)


def load_data_from_csv() -> pd.DataFrame:
    """Load data from CSV file (fallback method)."""
    # Try multiple locations for the dataset
    possible_paths = [
        Path(__file__).resolve().parents[2] / DATA_FILENAME,  # Original path (root)
        Path(__file__).resolve().parents[1] / DATA_FILENAME,  # backend/
        Path("/opt/render/project/src") / DATA_FILENAME,      # Render root explicit
        Path.cwd() / DATA_FILENAME,                           # Current working directory
    ]
    
    data_path = None
    for path in possible_paths:
        if path.exists():
            data_path = path
            break
            
    if not data_path:
        # List directories to help debug
        try:
            cwd_files = list(Path.cwd().glob("*"))
            print(f"CWD files: {cwd_files}")
        except Exception:
            pass
        raise FileNotFoundError(f"Dataset not found. Searched in: {[str(p) for p in possible_paths]}")

    df = pd.read_csv(data_path, low_memory=False)
    df = _standardize_columns(df)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    if "tags" in df.columns:
        df["tags"] = df["tags"].fillna("").astype(str)
    if "customer_name" in df.columns:
        df["customer_name"] = df["customer_name"].fillna("")
    if "phone_number" in df.columns:
        df["phone_number"] = df["phone_number"].fillna("")

    return df


@lru_cache(maxsize=1)
def load_data() -> pd.DataFrame:
    """
    Load data from Supabase if available, otherwise fall back to CSV.
    This function is cached to avoid repeated loads.
    """
    supabase = get_supabase_client()
    
    if supabase:
        # Use Supabase - much faster!
        print("Loading data from Supabase...")
        try:
            # Note: We don't load all data at once anymore
            # Repository will query Supabase directly
            # This just returns an empty DataFrame as a marker
            return pd.DataFrame()
        except Exception as e:
            print(f"Supabase load failed: {e}, falling back to CSV")
    
    # Fallback to CSV
    print("Loading data from CSV...")
    return load_data_from_csv()
