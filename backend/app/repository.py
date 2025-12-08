from typing import Tuple

import pandas as pd

from .models import SalesQuery


def apply_filters(df: pd.DataFrame, params: SalesQuery) -> pd.DataFrame:
    filtered = df

    def to_list(val):
        if val is None:
            return []
        if isinstance(val, list):
            return [v for v in val if v is not None and v != ""]
        return [val]

    if params.customer_name and "customer_name" in filtered.columns:
        mask = filtered["customer_name"].str.contains(params.customer_name, case=False, na=False)
        filtered = filtered[mask]

    if params.phone and "phone_number" in filtered.columns:
        mask = filtered["phone_number"].astype(str).str.contains(params.phone, na=False)
        filtered = filtered[mask]

    regions = to_list(params.region)
    if regions and "customer_region" in filtered.columns:
        filtered = filtered[filtered["customer_region"].isin(regions)]

    genders = to_list(params.gender)
    if genders and "gender" in filtered.columns:
        filtered = filtered[filtered["gender"].isin(genders)]

    if params.age_min is not None and "age" in filtered.columns:
        filtered = filtered[filtered["age"] >= params.age_min]

    if params.age_max is not None and "age" in filtered.columns:
        filtered = filtered[filtered["age"] <= params.age_max]

    categories = to_list(params.product_category)
    if categories and "product_category" in filtered.columns:
        filtered = filtered[filtered["product_category"].isin(categories)]

    tags = [t.lower() for t in to_list(params.tag)]
    if tags and "tags" in filtered.columns:
        filtered = filtered[filtered["tags"].astype(str).str.lower().apply(
            lambda cell: any(tag in cell for tag in tags)
        )]

    methods = to_list(params.payment_method)
    if methods and "payment_method" in filtered.columns:
        filtered = filtered[filtered["payment_method"].isin(methods)]

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
