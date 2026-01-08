"""Pandera schema helpers for customer-level feature tables."""

from __future__ import annotations

import pandera as pa
from pandera import Column, DataFrameSchema


def _infer_first_non_null_type(column: str) -> pa.DataType:
    if column in {"married", "has_children"}:
        return pa.Bool
    if column == "birthdate":
        return pa.DateTime
    return pa.String


def build_customer_features_schema(features_cfg: dict) -> DataFrameSchema:
    """Build a Pandera schema from the feature configuration."""
    id_col = features_cfg["id_col"]
    numeric_means = features_cfg.get("numeric_means", [])
    boolean_means = features_cfg.get("boolean_means", [])
    first_non_null_cols = features_cfg.get("first_non_null", [])
    max_cols = features_cfg.get("max_cols", ["customer_tenure_days", "age_years"])

    columns: dict[str, Column] = {
        id_col: Column(pa.Int64, nullable=False),
        "n_sessions": Column(pa.Int64, nullable=False),
        **{f"avg_{col}": Column(pa.Float64, nullable=True) for col in numeric_means},
        **{f"p_{col}": Column(pa.Float64, nullable=True) for col in boolean_means},
        **{col: Column(pa.Float64, nullable=True) for col in max_cols},
        **{
            col: Column(_infer_first_non_null_type(col), nullable=True)
            for col in first_non_null_cols
        },
    }

    return DataFrameSchema(columns, coerce=True, strict=False)
