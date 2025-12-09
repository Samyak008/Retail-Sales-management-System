from fastapi import APIRouter, Depends, HTTPException, Query

from ..data_loader import load_data, get_supabase_client, load_data_from_csv
from ..models import MetaResponse, SalesQuery, SalesResponse
from ..repository import apply_filters, apply_pagination, apply_sort
from ..repository_supabase import query_supabase, get_metadata_from_supabase
from ..utils import distinct_tags, distinct_values, total_pages

router = APIRouter(tags=["sales"])

DEFAULT_META = {
    "regions": ["Central", "East", "North", "South", "West"],
    "genders": ["Female", "Male"],
    "product_categories": ["Beauty", "Clothing", "Electronics"],
    "tags": [
        "accessories",
        "beauty",
        "casual",
        "cotton",
        "fashion",
        "formal",
        "fragrance-free",
        "gadgets",
        "makeup",
        "organic",
        "portable",
        "skincare",
        "smart",
        "unisex",
        "wireless",
    ],
    "payment_methods": ["Cash", "Credit Card", "Debit Card", "Net Banking", "UPI", "Wallet"],
}


def sales_query(
    customer_name: str | None = Query(None),
    phone: str | None = Query(None),
    region: list[str] | None = Query(None),
    gender: list[str] | None = Query(None),
    age_min: int | None = Query(None),
    age_max: int | None = Query(None),
    product_category: list[str] | None = Query(None),
    tag: list[str] | None = Query(None),
    payment_method: list[str] | None = Query(None),
    date_from: str | None = Query(None),
    date_to: str | None = Query(None),
    sort_by: str = Query("date"),
    order: str = Query("desc"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
) -> SalesQuery:
    return SalesQuery(
        customer_name=customer_name,
        phone=phone,
        region=region,
        gender=gender,
        age_min=age_min,
        age_max=age_max,
        product_category=product_category,
        tag=tag,
        payment_method=payment_method,
        date_from=date_from,
        date_to=date_to,
        sort_by=sort_by,
        order=order,
        page=page,
        page_size=page_size,
    )


@router.get("/sales", response_model=SalesResponse)
async def get_sales(params: SalesQuery = Depends(sales_query)) -> SalesResponse:
    supabase = get_supabase_client()

    if supabase:
        try:
            items, total = query_supabase(params)
            return SalesResponse(
                items=items,
                total=total,
                page=params.page,
                page_size=params.page_size,
                total_pages=total_pages(total, params.page_size),
            )
        except Exception as e:
            # Graceful fallback to CSV to avoid hard failures on hosted DB timeouts
            print(f"Supabase query failed, falling back to CSV: {e}")

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
        try:
            metadata = get_metadata_from_supabase()
            # Always merge Supabase metadata with CSV distincts to ensure completeness across environments.
            try:
                df = load_data()
                if df is None or df.empty:
                    df = load_data_from_csv()
                merged = {
                    "regions": set(metadata.get("regions", [])) | set(distinct_values(df, "customer_region")),
                    "genders": set(metadata.get("genders", [])) | set(distinct_values(df, "gender")),
                    "product_categories": set(metadata.get("product_categories", [])) | set(distinct_values(df, "product_category")),
                    "tags": set(metadata.get("tags", [])) | set(distinct_tags(df, "tags")),
                    "payment_methods": set(metadata.get("payment_methods", [])) | set(distinct_values(df, "payment_method")),
                }
                # Final union with defaults to guarantee completeness
                merged = {k: sorted(merged.get(k, set()) | set(DEFAULT_META[k])) for k in DEFAULT_META}
                return MetaResponse(**merged)
            except Exception as merge_exc:
                print(f"Metadata merge fallback failed: {merge_exc}")
                # Still ensure defaults are included
                merged = {k: sorted(set(metadata.get(k, [])) | set(DEFAULT_META[k])) for k in DEFAULT_META}
                return MetaResponse(**merged)
        except Exception as e:
            print(f"Supabase metadata fetch failed, falling back to CSV: {e}")

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
