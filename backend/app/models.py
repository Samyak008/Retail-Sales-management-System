from datetime import date
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, field_validator, Field


class SalesQuery(BaseModel):
    """
    SalesQuery model for filtering and sorting sales data.
    This Pydantic model defines query parameters for searching and filtering sales records
    with support for customer information, product details, date ranges, and result pagination.
    Attributes:
        customer_name (Optional[str]): Search by customer name using case-insensitive contains matching.
        phone (Optional[str]): Search by phone number using contains matching.
        region (Optional[str]): Filter results by customer region.
        gender (Optional[str]): Filter results by customer gender.
        age_min (Optional[int]): Minimum age filter (inclusive, must be >= 0).
        age_max (Optional[int]): Maximum age filter (inclusive, must be >= 0).
        product_category (Optional[str]): Filter results by product category.
        tag (Optional[str]): Filter results by tag using contains matching.
        payment_method (Optional[str]): Filter results by payment method.
        date_from (Optional[date]): Start date for date range filter (inclusive).
        date_to (Optional[date]): End date for date range filter (inclusive).
        sort_by (str): Field to sort results by. Valid values: 'date', 'quantity', 'customer_name'.
            Defaults to 'date'.
        order (str): Sort order direction. Valid values: 'asc' (ascending), 'desc' (descending).
            Defaults to 'desc'.
        page (int): Page number for pagination (1-indexed). Defaults to 1, must be >= 1.
        page_size (int): Number of items per page. Defaults to 10, must be between 1 and 100.
    Raises:
        ValueError: If 'order' is not 'asc' or 'desc'.
        ValueError: If 'sort_by' is not one of 'date', 'quantity', or 'customer_name'.
    """
    customer_name: Optional[str] = Field(None, description="Search by customer name (contains, case-insensitive)")
    phone: Optional[str] = Field(None, description="Search by phone number (contains)")
    region: Optional[List[str]] = Field(None, description="Filter by customer region (multi-select)")
    gender: Optional[List[str]] = Field(None, description="Filter by gender (multi-select)")
    age_min: Optional[int] = Field(None, ge=0, description="Minimum age")
    age_max: Optional[int] = Field(None, ge=0, description="Maximum age")
    product_category: Optional[List[str]] = Field(None, description="Filter by product category (multi-select)")
    tag: Optional[List[str]] = Field(None, description="Filter by tag (multi-select contains)")
    payment_method: Optional[List[str]] = Field(None, description="Filter by payment method (multi-select)")
    date_from: Optional[date] = Field(None, description="Start date (inclusive)")
    date_to: Optional[date] = Field(None, description="End date (inclusive)")
    sort_by: str = Field("date", description="Sort field: date|quantity|customer_name")
    order: str = Field("desc", description="Sort order: asc|desc")
    page: int = Field(1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(10, ge=1, le=100, description="Items per page")

    @field_validator('order', mode="before")
    def validate_order(cls, v: str) -> str:
        if v not in {"asc", "desc"}:
            raise ValueError("order must be 'asc' or 'desc'")
        return v

    @field_validator('sort_by', mode="after")
    def validate_sort_by(cls, v: str) -> str:
        if v not in {"date", "quantity", "customer_name"}:
            raise ValueError("sort_by must be one of: date, quantity, customer_name")
        return v

    @field_validator("region", "gender", "product_category", "payment_method", "tag", mode="before")
    def coerce_to_list(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            parts = [part.strip() for part in v.split(",")]
            cleaned = [part for part in parts if part]
            return cleaned or None
        if isinstance(v, list):
            cleaned = [item for item in v if isinstance(item, str) and item.strip()]
            return cleaned or None
        return None


class SalesResponse(BaseModel):
    items: List[Dict[str, Any]]
    total: int
    page: int
    page_size: int
    total_pages: int


class MetaResponse(BaseModel):
    regions: List[str]
    genders: List[str]
    product_categories: List[str]
    tags: List[str]
    payment_methods: List[str]
