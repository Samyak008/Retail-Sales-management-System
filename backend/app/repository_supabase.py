from typing import List, Tuple

import pandas as pd
from postgrest import APIResponse

from .data_loader import get_supabase_client
from .models import SalesQuery


def query_supabase(params: SalesQuery) -> Tuple[pd.DataFrame, int]:
    """
    Query Supabase directly with filters, sorting, and pagination.
    Returns (dataframe, total_count).
    """
    supabase = get_supabase_client()
    
    if not supabase:
        # Fallback to old method if Supabase not configured
        return pd.DataFrame(), 0
    
    # Start building the query
    query = supabase.table("sales").select("*", count="exact")
    
    # Apply filters
    if params.customer_name:
        query = query.ilike("customer_name", f"%{params.customer_name}%")
    
    if params.phone:
        query = query.ilike("phone_number", f"%{params.phone}%")
    
    if params.region:
        query = query.eq("customer_region", params.region)
    
    if params.gender:
        query = query.eq("gender", params.gender)
    
    if params.age_min is not None:
        query = query.gte("age", params.age_min)
    
    if params.age_max is not None:
        query = query.lte("age", params.age_max)
    
    if params.product_category:
        query = query.eq("product_category", params.product_category)
    
    if params.tag:
        query = query.ilike("tags", f"%{params.tag}%")
    
    if params.payment_method:
        query = query.eq("payment_method", params.payment_method)
    
    if params.date_from:
        query = query.gte("date", params.date_from)
    
    if params.date_to:
        query = query.lte("date", params.date_to)
    
    # Apply sorting
    column_map = {
        "date": "date",
        "quantity": "quantity",
        "customer_name": "customer_name",
    }
    sort_column = column_map.get(params.sort_by, "date")
    ascending = params.order == "asc"
    query = query.order(sort_column, desc=not ascending)
    
    # Apply pagination
    start = (params.page - 1) * params.page_size
    end = start + params.page_size - 1
    query = query.range(start, end)
    
    # Execute query
    response: APIResponse = query.execute()
    
    # Get total count
    total = response.count if hasattr(response, 'count') else 0
    
    # Convert to DataFrame
    df = pd.DataFrame(response.data)
    
    # Convert date column to datetime
    if "date" in df.columns and not df.empty:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    
    return df, total


def get_metadata_from_supabase() -> dict:
    """Get unique values for filters from Supabase."""
    supabase = get_supabase_client()
    
    if not supabase:
        return {
            "regions": [],
            "genders": [],
            "product_categories": [],
            "tags": [],
            "payment_methods": []
        }
    
    try:
        # Get distinct values for each field
        regions_response = supabase.rpc("get_distinct_regions").execute()
        genders_response = supabase.rpc("get_distinct_genders").execute()
        categories_response = supabase.rpc("get_distinct_categories").execute()
        tags_response = supabase.rpc("get_distinct_tags").execute()
        payment_methods_response = supabase.rpc("get_distinct_payment_methods").execute()
        
        return {
            "regions": regions_response.data if regions_response.data else [],
            "genders": genders_response.data if genders_response.data else [],
            "product_categories": categories_response.data if categories_response.data else [],
            "tags": tags_response.data if tags_response.data else [],
            "payment_methods": payment_methods_response.data if payment_methods_response.data else []
        }
    except Exception as e:
        print(f"Error fetching metadata: {e}")
        # Fallback to simple queries
        try:
            regions = supabase.table("sales").select("customer_region").limit(1000).execute()
            genders = supabase.table("sales").select("gender").limit(100).execute()
            categories = supabase.table("sales").select("product_category").limit(1000).execute()
            payments = supabase.table("sales").select("payment_method").limit(100).execute()
            
            return {
                "regions": sorted(list(set(r["customer_region"] for r in regions.data if r.get("customer_region")))),
                "genders": sorted(list(set(g["gender"] for g in genders.data if g.get("gender")))),
                "product_categories": sorted(list(set(c["product_category"] for c in categories.data if c.get("product_category")))),
                "tags": [],  # Tags need special handling
                "payment_methods": sorted(list(set(p["payment_method"] for p in payments.data if p.get("payment_method"))))
            }
        except Exception as e2:
            print(f"Error in fallback metadata: {e2}")
            return {
                "regions": [],
                "genders": [],
                "product_categories": [],
                "tags": [],
                "payment_methods": []
            }


# Old pandas-based functions (kept for CSV fallback)
def apply_filters(df: pd.DataFrame, params: SalesQuery) -> pd.DataFrame:
    filtered = df

    if params.customer_name and "customer_name" in filtered.columns:
        mask = filtered["customer_name"].str.contains(params.customer_name, case=False, na=False)
        filtered = filtered[mask]

    if params.phone and "phone_number" in filtered.columns:
        mask = filtered["phone_number"].astype(str).str.contains(params.phone, na=False)
        filtered = filtered[mask]

    if params.region and "customer_region" in filtered.columns:
        filtered = filtered[filtered["customer_region"] == params.region]

    if params.gender and "gender" in filtered.columns:
        filtered = filtered[filtered["gender"] == params.gender]

    if params.age_min is not None and "age" in filtered.columns:
        filtered = filtered[filtered["age"] >= params.age_min]

    if params.age_max is not None and "age" in filtered.columns:
        filtered = filtered[filtered["age"] <= params.age_max]

    if params.product_category and "product_category" in filtered.columns:
        filtered = filtered[filtered["product_category"] == params.product_category]

    if params.tag and "tags" in filtered.columns:
        filtered = filtered[filtered["tags"].str.contains(params.tag, case=False, na=False)]

    if params.payment_method and "payment_method" in filtered.columns:
        filtered = filtered[filtered["payment_method"] == params.payment_method]

    if params.date_from and "date" in filtered.columns:
        filtered = filtered[filtered["date"] >= pd.to_datetime(params.date_from)]

    if params.date_to and "date" in filtered.columns:
        filtered = filtered[filtered["date"] <= pd.to_datetime(params.date_to)]

    return filtered


def apply_sort(df: pd.DataFrame, params: SalesQuery) -> pd.DataFrame:
    column_map = {
        "date": "date",
        "quantity": "quantity",
        "customer_name": "customer_name",
    }
    column = column_map.get(params.sort_by, "date")
    if column not in df.columns:
        return df
    ascending = params.order == "asc"
    return df.sort_values(by=column, ascending=ascending, na_position="last")


def apply_pagination(df: pd.DataFrame, page: int, page_size: int) -> Tuple[pd.DataFrame, int]:
    total = len(df)
    start = (page - 1) * page_size
    end = start + page_size
    return df.iloc[start:end], total
