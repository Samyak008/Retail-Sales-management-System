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
    # Optimization: Use 'planned' count for unfiltered queries to avoid full table scan
    # 'exact' count is slow on large tables. 'planned' uses Postgres statistics (instant).
    def has_value(value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, list):
            return len(value) > 0
        return bool(value)

    has_filters = any([
        params.customer_name, params.phone, has_value(params.region), has_value(params.gender),
        params.age_min is not None, params.age_max is not None,
        has_value(params.product_category), has_value(params.tag), has_value(params.payment_method),
        params.date_from, params.date_to
    ])
    
    count_method = "exact" if has_filters else "planned"
    query = supabase.table("sales").select("*", count=count_method)
    
    # Apply filters
    if params.customer_name:
        query = query.ilike("customer_name", f"%{params.customer_name}%")
    
    if params.phone:
        query = query.ilike("phone_number", f"%{params.phone}%")
    
    regions = params.region or []
    if regions:
        query = query.in_("customer_region", regions)

    genders = params.gender or []
    if genders:
        query = query.in_("gender", genders)
    
    if params.age_min is not None:
        query = query.gte("age", params.age_min)
    
    if params.age_max is not None:
        query = query.lte("age", params.age_max)
    
    categories = params.product_category or []
    if categories:
        query = query.in_("product_category", categories)

    tags = params.tag or []
    if tags:
        tag_filters = ",".join([f"tags.ilike.%{tag}%" for tag in tags])
        query = query.or_(tag_filters)

    methods = params.payment_method or []
    if methods:
        query = query.in_("payment_method", methods)
    
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
        # Optimized metadata query: Fetch all distinct values in a single round-trip
        # This reduces latency significantly compared to 4 sequential requests
        query = """
        SELECT json_build_object(
            'regions', (SELECT COALESCE(array_agg(DISTINCT customer_region ORDER BY customer_region), '{}') FROM sales WHERE customer_region IS NOT NULL),
            'genders', (SELECT COALESCE(array_agg(DISTINCT gender ORDER BY gender), '{}') FROM sales WHERE gender IS NOT NULL),
            'product_categories', (SELECT COALESCE(array_agg(DISTINCT product_category ORDER BY product_category), '{}') FROM sales WHERE product_category IS NOT NULL),
            'payment_methods', (SELECT COALESCE(array_agg(DISTINCT payment_method ORDER BY payment_method), '{}') FROM sales WHERE payment_method IS NOT NULL),
            'tags', (
                SELECT COALESCE(array_agg(DISTINCT trimmed_tag ORDER BY trimmed_tag), '{}')
                FROM (
                    SELECT trim(both ' ' FROM unnest(string_to_array(tags, ','))) AS trimmed_tag
                    FROM sales
                    WHERE tags IS NOT NULL
                ) tag_list
                WHERE trimmed_tag <> ''
            )
        );
        """
        # Try to execute via RPC if available
        result = supabase.rpc('exec_sql', {'query': query}).execute()
        
        if result.data and len(result.data) > 0:
            data = result.data[0]
            # Handle case where data might be wrapped or direct
            if isinstance(data, dict) and 'json_build_object' in data:
                data = data['json_build_object']
            
            return {
                "regions": data.get("regions", []),
                "genders": data.get("genders", []),
                "product_categories": data.get("product_categories", []),
                "tags": data.get("tags", []),
                "payment_methods": data.get("payment_methods", [])
            }
            
        # If we get here, the result format wasn't as expected, fall through to fallback
        raise ValueError("Unexpected RPC response format")

    except Exception as e:
        print(f"Error fetching metadata with RPC: {e}")
        # Simplified fallback - use PostgREST's built-in distinct
        try:
            # Much faster approach: query just 10k rows and get unique values
            regions = supabase.table("sales").select("customer_region").limit(10000).execute()
            genders = supabase.table("sales").select("gender").limit(100).execute()
            categories = supabase.table("sales").select("product_category").limit(10000).execute()
            payments = supabase.table("sales").select("payment_method").limit(100).execute()
            tags = supabase.table("sales").select("tags").limit(10000).execute()
            
            return {
                "regions": sorted(list(set(r["customer_region"] for r in regions.data if r.get("customer_region")))),
                "genders": sorted(list(set(g["gender"] for g in genders.data if g.get("gender")))),
                "product_categories": sorted(list(set(c["product_category"] for c in categories.data if c.get("product_category")))),
                "tags": sorted(list({tag.strip() for row in tags.data for tag in str(row.get("tags", "")).split(",") if tag.strip()})),
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
        filtered = filtered[filtered["customer_region"].isin(params.region)]

    if params.gender and "gender" in filtered.columns:
        filtered = filtered[filtered["gender"].isin(params.gender)]

    if params.age_min is not None and "age" in filtered.columns:
        filtered = filtered[filtered["age"] >= params.age_min]

    if params.age_max is not None and "age" in filtered.columns:
        filtered = filtered[filtered["age"] <= params.age_max]

    if params.product_category and "product_category" in filtered.columns:
        filtered = filtered[filtered["product_category"].isin(params.product_category)]

    if params.tag and "tags" in filtered.columns:
        lowered_tags = [t.lower() for t in params.tag]
        filtered = filtered[filtered["tags"].astype(str).str.lower().apply(
            lambda cell: any(tag in cell for tag in lowered_tags)
        )]

    if params.payment_method and "payment_method" in filtered.columns:
        filtered = filtered[filtered["payment_method"].isin(params.payment_method)]

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
