from functools import lru_cache
from pathlib import Path
from typing import Dict

import pandas as pd

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


def _standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {}
    for col in df.columns:
        if col in COLUMN_MAP:
            rename_map[col] = COLUMN_MAP[col]
        else:
            cleaned = col.strip().lower().replace(" ", "_")
            rename_map[col] = cleaned
    return df.rename(columns=rename_map)


@lru_cache(maxsize=1)
def load_data() -> pd.DataFrame:
    data_path = Path(__file__).resolve().parents[2] / DATA_FILENAME
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset not found at {data_path}")

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
