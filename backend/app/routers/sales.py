from fastapi import APIRouter, Depends, HTTPException

from ..data_loader import load_data
from ..models import MetaResponse, SalesQuery, SalesResponse
from ..repository import apply_filters, apply_pagination, apply_sort
from ..utils import distinct_tags, distinct_values, total_pages

router = APIRouter(tags=["sales"])


@router.get("/sales", response_model=SalesResponse)
async def get_sales(params: SalesQuery = Depends()) -> SalesResponse:
    try:
        df = load_data()
    except FileNotFoundError as exc:  # pragma: no cover - configuration issue
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
    try:
        df = load_data()
    except FileNotFoundError as exc:  # pragma: no cover - configuration issue
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return MetaResponse(
        regions=distinct_values(df, "customer_region"),
        genders=distinct_values(df, "gender"),
        product_categories=distinct_values(df, "product_category"),
        tags=distinct_tags(df, "tags"),
        payment_methods=distinct_values(df, "payment_method"),
    )
