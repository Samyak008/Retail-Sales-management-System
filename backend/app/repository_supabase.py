from typing import List, Tuple, Dict, Any
from functools import lru_cache

import pandas as pd
from postgrest import APIResponse

from .data_loader import get_supabase_client
from .models import SalesQuery


def query_supabase(params: SalesQuery) -> Tuple[List[Dict[str, Any]], int]:
    """
    Query Supabase directly with filters, sorting, and pagination.
    Returns (list of dicts, total_count).
    """
    supabase = get_supabase_client()
    
    if not supabase:
        # Fallback to old method if Supabase not configured
        return [], 0
    
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
    
    return response.data, total


@lru_cache(maxsize=1)
def get_metadata_from_supabase() -> dict:
    """Get unique values for filters from Supabase. Cached for performance."""
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
        # Use DISTINCT queries directly - much faster than fetching all rows
        query = """
        SELECT DISTINCT customer_region FROM sales WHERE customer_region IS NOT NULL ORDER BY customer_region;
        """
        regions = supabase.rpc('exec_sql', {'query': query}).execute()
        
        query = """
        SELECT DISTINCT gender FROM sales WHERE gender IS NOT NULL ORDER BY gender;
        """
        genders = supabase.rpc('exec_sql', {'query': query}).execute()
        
        query = """
        SELECT DISTINCT product_category FROM sales WHERE product_category IS NOT NULL ORDER BY product_category;
        """
        categories = supabase.rpc('exec_sql', {'query': query}).execute()
        
        query = """
        SELECT DISTINCT payment_method FROM sales WHERE payment_method IS NOT NULL ORDER BY payment_method;
        """
        payments = supabase.rpc('exec_sql', {'query': query}).execute()
        
        return {
            "regions": [r[0] for r in regions.data] if regions.data else [],
            "genders": [g[0] for g in genders.data] if genders.data else [],
            "product_categories": [c[0] for c in categories.data] if categories.data else [],
            "tags": [],
            "payment_methods": [p[0] for p in payments.data] if payments.data else []
        }
    except Exception as e:
        print(f"Error fetching metadata with RPC: {e}")
        # Simplified fallback - use PostgREST's built-in distinct
        try:
            # Much faster approach: query just 10k rows and get unique values
            regions = supabase.table("sales").select("customer_region").limit(10000).execute()
            genders = supabase.table("sales").select("gender").limit(100).execute()
            categories = supabase.table("sales").select("product_category").limit(10000).execute()
            payments = supabase.table("sales").select("payment_method").limit(100).execute()
            
            return {
                "regions": sorted(list(set(r["customer_region"] for r in regions.data if r.get("customer_region")))),
                "genders": sorted(list(set(g["gender"] for g in genders.data if g.get("gender")))),
                "product_categories": sorted(list(set(c["product_category"] for c in categories.data if c.get("product_category")))),
                "tags": [],
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
