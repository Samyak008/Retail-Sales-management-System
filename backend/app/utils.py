from math import ceil
from typing import Iterable, List

import pandas as pd


def total_pages(total: int, page_size: int) -> int:
    return ceil(total / page_size) if page_size else 0


def distinct_values(df: pd.DataFrame, column: str) -> List[str]:
    if column not in df.columns:
        return []
    series = df[column].dropna().astype(str)
    return sorted(series.unique())


def distinct_tags(df: pd.DataFrame, column: str = "tags") -> List[str]:
    if column not in df.columns:
        return []
    tags: Iterable[str] = (
        tag.strip()
        for cell in df[column].dropna().astype(str)
        for tag in cell.split(",")
        if tag.strip()
    )
    return sorted(set(tags))
