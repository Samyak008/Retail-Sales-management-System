from typing import Tuple

import pandas as pd

from .models import SalesQuery


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
