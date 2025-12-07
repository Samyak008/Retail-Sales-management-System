from fastapi import APIRouter, Depends, HTTPException

from ..data_loader import load_data, get_supabase_client
from ..models import MetaResponse, SalesQuery, SalesResponse
from ..repository import apply_filters, apply_pagination, apply_sort
from ..repository_supabase import query_supabase, get_metadata_from_supabase
from ..utils import distinct_tags, distinct_values, total_pages

router = APIRouter(tags=["sales"])


@router.get("/sales", response_model=SalesResponse)
async def get_sales(params: SalesQuery = Depends()) -> SalesResponse:
    supabase = get_supabase_client()
    
    if supabase:
        # Use Supabase - fast and efficient!
        try:
            items, total = query_supabase(params)
            return SalesResponse(
                items=items,  # Already a list of dicts, no pandas conversion needed
                total=total,
                page=params.page,
                page_size=params.page_size,
                total_pages=total_pages(total, params.page_size),
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")
    
    # Fallback to CSV if Supabase not configured
    try:
        df = load_data()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    filtered = apply_filters(df, params)
    sorted_df = apply_sort(filtered, params)
    page_df, total = apply_pagination(sorted_df, params.page, params.page_size)

    return SalesResponse(
        items=page_df.fillna("").to_dict(orient="records"),
        total=total,
        page=params.page,
        page_size=params.page_size,
        total_pages=total_pages(total, params.page_size),
    )


@router.get("/meta", response_model=MetaResponse)
async def get_meta() -> MetaResponse:
    supabase = get_supabase_client()
    
    if supabase:
        # Use Supabase for metadata
        try:
            metadata = get_metadata_from_supabase()
            return MetaResponse(**metadata)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Metadata fetch failed: {str(e)}")
    
    # Fallback to CSV if Supabase not configured
    try:
        df = load_data()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return MetaResponse(
        regions=distinct_values(df, "customer_region"),
        genders=distinct_values(df, "gender"),
        product_categories=distinct_values(df, "product_category"),
        tags=distinct_tags(df, "tags"),
        payment_methods=distinct_values(df, "payment_method"),
    )
