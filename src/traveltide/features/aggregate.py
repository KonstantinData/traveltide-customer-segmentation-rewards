"""Feature aggregation helpers for customer-level modeling tables."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd


def first_non_null(series: pd.Series):
    """Return the first non-null entry from a Series, if any."""
    non_null = series.dropna()
    return non_null.iloc[0] if not non_null.empty else None


def _build_mean_aggs(columns: Iterable[str], prefix: str) -> dict[str, tuple[str, str]]:
    return {f"{prefix}{col}": (col, "mean") for col in columns}


def _build_first_aggs(columns: Iterable[str]) -> dict[str, tuple[str, object]]:
    return {col: (col, first_non_null) for col in columns}


def _build_max_aggs(columns: Iterable[str]) -> dict[str, tuple[str, str]]:
    return {col: (col, "max") for col in columns}


def build_customer_features(
    df: pd.DataFrame,
    *,
    id_col: str,
    session_col: str,
    numeric_means: Iterable[str],
    boolean_means: Iterable[str],
    first_non_null_cols: Iterable[str],
    max_cols: Iterable[str] | None = None,
) -> pd.DataFrame:
    """Aggregate session-level data into customer-level features."""
    max_cols = list(max_cols or [])
    agg_spec: dict[str, tuple[str, object]] = {
        "n_sessions": (session_col, "nunique"),
        **_build_mean_aggs(numeric_means, "avg_"),
        **_build_mean_aggs(boolean_means, "p_"),
        **_build_max_aggs(max_cols),
        **_build_first_aggs(first_non_null_cols),
    }
    agg = df.groupby(id_col).agg(**agg_spec)
    return agg.reset_index()
