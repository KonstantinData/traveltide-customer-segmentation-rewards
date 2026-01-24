"""Orchestrate feature engineering for customer-level modeling tables."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

from .aggregate import build_customer_features
from .schema import build_customer_features_schema


def _apply_time_derivations(
    df: pd.DataFrame,
    *,
    session_start_col: str,
    sign_up_date_col: str,
    birthdate_col: str | None = None,
) -> pd.DataFrame:
    out = df.copy()
    out[session_start_col] = pd.to_datetime(
        out[session_start_col], utc=True, errors="coerce"
    )
    out[sign_up_date_col] = pd.to_datetime(
        out[sign_up_date_col], utc=False, errors="coerce"
    )
    if birthdate_col:
        out[birthdate_col] = pd.to_datetime(
            out[birthdate_col], utc=False, errors="coerce"
        )
        out["age_years"] = (
            out[session_start_col].dt.tz_convert(None) - out[birthdate_col]
        ).dt.days / 365.25
    out["customer_tenure_days"] = (
        out[session_start_col].dt.tz_convert(None) - out[sign_up_date_col]
    ).dt.days
    return out


def run_features(config_path: str, outdir: str | None = None) -> Path:
    """Run the features pipeline and return the output path."""
    cfg = yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))
    df = pd.read_parquet(cfg["input"]["sessions_clean_path"])

    features_cfg = cfg["features"]
    time_cols = features_cfg.get("time_cols", {})
    if time_cols:
        df = _apply_time_derivations(
            df,
            session_start_col=time_cols["session_start"],
            sign_up_date_col=time_cols["sign_up_date"],
            birthdate_col=time_cols.get("birthdate"),
        )

    max_cols = features_cfg.get("max_cols")
    if max_cols is None:
        max_cols = [
            col for col in ("customer_tenure_days", "age_years") if col in df.columns
        ]

    features = build_customer_features(
        df,
        id_col=features_cfg["id_col"],
        session_col=features_cfg["session_col"],
        numeric_means=features_cfg.get("numeric_means", []),
        boolean_means=features_cfg.get("boolean_means", []),
        first_non_null_cols=features_cfg.get("first_non_null", []),
        max_cols=max_cols,
    )

    # Fill missing values for numeric features with 0 (means customer didn't use that service)
    numeric_cols = [
        col
        for col in features.columns
        if col.startswith("avg_") and features[col].dtype in ["float64", "int64"]
    ]
    features[numeric_cols] = features[numeric_cols].fillna(0)

    if features_cfg.get("validate_schema", False):
        schema = build_customer_features_schema(features_cfg)
        schema.validate(features)

    out_path = Path(cfg["output"]["customer_features_path"])
    if outdir:
        out_path = Path(outdir) / out_path.name
    out_path.parent.mkdir(parents=True, exist_ok=True)
    features.to_parquet(out_path, index=False)
    return out_path
