# Description: Exploratory transformation experiments for EDA reporting.
"""Exploratory transformation experiments for EDA reporting.

Notes:
- This module is exploratory only and must never modify downstream production features.
- It computes distribution summaries before/after simple scaling and feature derivations.
- Results are persisted as machine-readable JSON under the run's exploratory folder.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd


def _numeric_summary(series: pd.Series) -> dict[str, float | int]:
    """Return a compact numeric summary for a series."""

    s = pd.to_numeric(series, errors="coerce").dropna()
    if s.empty:
        return {}

    return {
        "count": int(s.count()),
        "mean": float(s.mean()),
        "median": float(s.median()),
        "min": float(s.min()),
        "max": float(s.max()),
        "std": float(s.std(ddof=0)),
        "skew": float(s.skew()),
    }


def _standard_scale(series: pd.Series) -> pd.Series | None:
    s = pd.to_numeric(series, errors="coerce")
    mean = s.mean()
    std = s.std(ddof=0)
    if pd.isna(std) or std == 0:
        return None
    return (s - mean) / std


def _minmax_scale(series: pd.Series) -> pd.Series | None:
    s = pd.to_numeric(series, errors="coerce")
    min_val = s.min()
    max_val = s.max()
    if pd.isna(min_val) or pd.isna(max_val) or max_val == min_val:
        return None
    return (s - min_val) / (max_val - min_val)


def _top_correlations(
    df: pd.DataFrame, series: pd.Series, *, top_n: int = 5
) -> list[dict[str, float | str]]:
    numeric = df.select_dtypes(include="number")
    if numeric.empty:
        return []

    correlations: list[dict[str, float | str]] = []
    for col in numeric.columns:
        if col == series.name:
            continue
        corr = series.corr(numeric[col])
        if pd.notna(corr):
            correlations.append({"column": col, "corr": float(corr)})
    correlations.sort(key=lambda item: abs(item["corr"]), reverse=True)
    return correlations[:top_n]


def _ratio_feature(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    denom = pd.to_numeric(denominator, errors="coerce").replace(0, np.nan)
    return pd.to_numeric(numerator, errors="coerce") / denom


def run_transform_experiments(
    *,
    session_df: pd.DataFrame,
    out_dir: Path,
) -> dict[str, Any]:
    """Run exploratory transformation experiments and persist outputs."""

    exploratory_dir = out_dir / "exploratory"
    exploratory_dir.mkdir(parents=True, exist_ok=True)
    output_path = exploratory_dir / "transform_experiments.json"

    scaling_candidates = [
        "base_fare_usd",
        "hotel_per_room_usd",
        "page_clicks",
        "session_duration_sec",
        "nights",
        "rooms",
        "seats",
    ]
    available_scaling_cols = [
        col for col in scaling_candidates if col in session_df.columns
    ]

    scaling_summary: list[dict[str, Any]] = []
    for col in available_scaling_cols:
        base = pd.to_numeric(session_df[col], errors="coerce")
        base_summary = _numeric_summary(base)
        if not base_summary:
            continue

        standard_scaled = _standard_scale(base)
        minmax_scaled = _minmax_scale(base)

        scaling_summary.append(
            {
                "column": col,
                "before": base_summary,
                "standard_scaled": _numeric_summary(standard_scaled)
                if standard_scaled is not None
                else {},
                "minmax_scaled": _numeric_summary(minmax_scaled)
                if minmax_scaled is not None
                else {},
            }
        )

    derivations: list[dict[str, Any]] = []
    numeric_reference = session_df.select_dtypes(include="number")
    feature_specs: list[dict[str, Any]] = [
        {
            "name": "log1p_base_fare_usd",
            "description": "Log-transform base fare to reduce right skew.",
            "source_columns": ["base_fare_usd"],
            "builder": lambda df: np.log1p(
                pd.to_numeric(df["base_fare_usd"], errors="coerce").clip(lower=0)
            ),
        },
        {
            "name": "log1p_hotel_per_room_usd",
            "description": "Log-transform hotel room rate to reduce right skew.",
            "source_columns": ["hotel_per_room_usd"],
            "builder": lambda df: np.log1p(
                pd.to_numeric(df["hotel_per_room_usd"], errors="coerce").clip(lower=0)
            ),
        },
        {
            "name": "fare_per_seat",
            "description": "Base fare divided by seats booked.",
            "source_columns": ["base_fare_usd", "seats"],
            "builder": lambda df: _ratio_feature(df["base_fare_usd"], df["seats"]),
        },
        {
            "name": "rooms_per_night",
            "description": "Rooms booked per night stay.",
            "source_columns": ["rooms", "nights"],
            "builder": lambda df: _ratio_feature(df["rooms"], df["nights"]),
        },
    ]

    for spec in feature_specs:
        if not all(col in session_df.columns for col in spec["source_columns"]):
            continue
        series = spec["builder"](session_df)
        series.name = spec["name"]
        summary = _numeric_summary(series)
        if not summary:
            continue

        distribution_shift: dict[str, float | None] = {}
        base_col = spec["source_columns"][0]
        if base_col in session_df.columns:
            base_summary = _numeric_summary(session_df[base_col])
            if base_summary:
                skew_before = base_summary.get("skew")
                skew_after = summary.get("skew")
                if skew_before is not None and skew_after is not None:
                    distribution_shift = {
                        "skew_before": float(skew_before),
                        "skew_after": float(skew_after),
                        "delta_skew": float(skew_after - skew_before),
                    }

        correlations = _top_correlations(numeric_reference, series)

        derivations.append(
            {
                "name": spec["name"],
                "description": spec["description"],
                "source_columns": spec["source_columns"],
                "summary": summary,
                "distribution_shift": distribution_shift,
                "top_correlations": correlations,
            }
        )

    results = {
        "notes": "Exploratory transformations only; downstream artifacts remain unchanged.",
        "scaling_summary": scaling_summary,
        "feature_derivations": derivations,
    }

    output_path.write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    return {
        "artifact_path": str(output_path.relative_to(out_dir)),
        "scaling_summary": scaling_summary,
        "feature_derivations": derivations,
    }
