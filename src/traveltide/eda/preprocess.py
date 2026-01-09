# Description: Preprocessing, cleaning, and aggregation for Step 1 EDA data.
"""Preprocessing, cleaning, outlier handling, and aggregation for Step 1 (EDA) (TT-012).

Notes:
- This module transforms raw extracted data into:
  (1) a cleaned session-level table and
  (2) a first user-level aggregated table suitable as a Step-1 handoff artifact.
- Decisions (e.g., invalid hotel nights handling, outlier method/thresholds) must be explicit and auditable.
- The functions are pure (DataFrame in → DataFrame out) where practical to keep behavior testable.
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime

import numpy as np
import pandas as pd

from .config import EDAConfig
from .dq_report import RuleImpact


# Notes: Normalize raw table dtypes for cleaned tables.
def coerce_columns(
    df: pd.DataFrame,
    *,
    datetime_cols: tuple[str, ...] = (),
    numeric_cols: tuple[str, ...] = (),
) -> pd.DataFrame:
    """Coerce datetimes and numerics for cleaned EDA tables.

    Notes:
    - "Cleaned" means the raw table is type-stable with no feature derivations.
    - "Transformed" variants add derived features for EDA summaries (see *_transformed helpers).
    """

    out = df.copy()
    for col in datetime_cols:
        if col in out.columns:
            out[col] = pd.to_datetime(out[col], errors="coerce", utc=True)
    for col in numeric_cols:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


# Notes: Clean session tables to stable types without derived features.
def clean_sessions_table(df: pd.DataFrame) -> pd.DataFrame:
    """Return the cleaned sessions table (type-stable, no derived features)."""

    return coerce_columns(
        df,
        datetime_cols=("session_start", "session_end"),
        numeric_cols=("user_id", "page_clicks"),
    )


# Notes: Clean user tables to stable types without derived features.
def clean_users_table(df: pd.DataFrame) -> pd.DataFrame:
    """Return the cleaned users table (type-stable, no derived features)."""

    return coerce_columns(
        df,
        datetime_cols=("birthdate", "sign_up_date"),
        numeric_cols=("user_id",),
    )


# Notes: Clean flight tables to stable types without derived features.
def clean_flights_table(df: pd.DataFrame) -> pd.DataFrame:
    """Return the cleaned flights table (type-stable, no derived features)."""

    return coerce_columns(
        df,
        datetime_cols=("departure_time", "return_time"),
        numeric_cols=("seats", "checked_bags", "base_fare_usd"),
    )


# Notes: Clean hotel tables to stable types without derived features.
def clean_hotels_table(df: pd.DataFrame) -> pd.DataFrame:
    """Return the cleaned hotels table (type-stable, no derived features)."""

    return coerce_columns(
        df,
        datetime_cols=("check_in_time", "check_out_time"),
        numeric_cols=("nights", "rooms", "hotel_per_room_usd"),
    )


# Notes: Add derived session-level metrics for EDA.
def transform_sessions_table(df: pd.DataFrame) -> pd.DataFrame:
    """Return the transformed sessions table with EDA-ready derived features."""

    out = df.copy()
    if "session_start" in out.columns and "session_end" in out.columns:
        out["session_duration_sec"] = (
            out["session_end"] - out["session_start"]
        ).dt.total_seconds()
    return out


# Notes: Add derived user-level metrics for EDA.
def transform_users_table(df: pd.DataFrame) -> pd.DataFrame:
    """Return the transformed users table with EDA-ready derived features."""

    out = df.copy()
    if "birthdate" in out.columns:
        today = datetime.utcnow().date()
        out["age_years"] = (
            pd.to_datetime(today) - pd.to_datetime(out["birthdate"])
        ).dt.days / 365.25
    if "sign_up_date" in out.columns:
        today = datetime.utcnow().date()
        out["tenure_days"] = (
            pd.to_datetime(today) - pd.to_datetime(out["sign_up_date"])
        ).dt.days
    return out


# Notes: Add derived flight-level metrics for EDA.
def transform_flights_table(df: pd.DataFrame) -> pd.DataFrame:
    """Return the transformed flights table with EDA-ready derived features."""

    out = df.copy()
    if "departure_time" in out.columns and "return_time" in out.columns:
        out["trip_duration_hours"] = (
            out["return_time"] - out["departure_time"]
        ).dt.total_seconds() / 3600.0
    return out


# Notes: Add derived hotel-level metrics for EDA.
def transform_hotels_table(df: pd.DataFrame) -> pd.DataFrame:
    """Return the transformed hotels table with EDA-ready derived features."""

    out = df.copy()
    if "check_in_time" in out.columns and "check_out_time" in out.columns:
        out["stay_duration_nights"] = (
            out["check_out_time"] - out["check_in_time"]
        ).dt.total_seconds() / 86400.0
    return out


# Notes: Create derived session features used in EDA summaries.
def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived, analysis-friendly columns.

    Notes:
    - Converts timestamp columns to datetime consistently.
    - Adds session duration and approximate age/tenure metrics for descriptive EDA.
    - Keeps derivations explicit so report + downstream steps can rely on stable column names.
    """

    # Notes: Work on a copy to avoid mutating caller-owned DataFrames.
    out = df.copy()

    # Notes: Normalize time columns; errors='coerce' ensures bad values become NaT (tracked in missingness).
    out["session_start"] = pd.to_datetime(
        out["session_start"], utc=True, errors="coerce"
    )
    out["session_end"] = pd.to_datetime(out["session_end"], utc=True, errors="coerce")
    out["sign_up_date"] = pd.to_datetime(
        out["sign_up_date"], utc=False, errors="coerce"
    )
    out["birthdate"] = pd.to_datetime(out["birthdate"], utc=False, errors="coerce")

    # Notes: Derived session duration for behavioral exploration and quality checks.
    out["session_duration_sec"] = (
        out["session_end"] - out["session_start"]
    ).dt.total_seconds()

    # Notes: Age is approximate and used only for descriptive purposes in EDA.
    today = datetime.utcnow().date()
    out["age_years"] = (pd.to_datetime(today) - out["birthdate"]).dt.days / 365.25

    # Notes: Customer tenure at time of session; supports cohort sanity checks.
    out["customer_tenure_days"] = (
        out["session_start"].dt.date.astype("datetime64[ns]") - out["sign_up_date"]
    ) / np.timedelta64(1, "D")

    return out


# Notes: Apply the configured policy for invalid hotel nights.
def fix_invalid_hotel_nights(df: pd.DataFrame, policy: str) -> pd.DataFrame:
    """Handle invalid values in hotels.nights (0 or negative).

    Notes:
    - The course material highlights anomalous nights values (0 or negative).
    - Policy options:
      - 'recompute': infer nights from check_in_time/check_out_time (preferred to avoid data loss).
      - 'drop': remove rows with invalid nights values.
    """

    # Notes: Operate on a copy to keep the transformation side-effect free.
    out = df.copy()
    if "nights" not in out.columns:
        return out

    nights = pd.to_numeric(out["nights"], errors="coerce")
    invalid = nights.isna() | (nights <= 0)

    # Notes: Drop policy trades correctness for data loss; must be explicit via config.
    if policy == "drop":
        return out.loc[~invalid].copy()

    # Notes: Recompute policy attempts to salvage records using timestamps.
    if policy != "recompute":
        raise ValueError(
            "cleaning.invalid_hotel_nights_policy must be one of: recompute, drop"
        )

    out["check_in_time"] = pd.to_datetime(
        out["check_in_time"], utc=True, errors="coerce"
    )
    out["check_out_time"] = pd.to_datetime(
        out["check_out_time"], utc=True, errors="coerce"
    )

    # Notes: Convert stay duration to days; NaT becomes NaN (preserved for missingness visibility).
    recomputed = (
        out["check_out_time"] - out["check_in_time"]
    ).dt.total_seconds() / 86400.0

    # Notes: Use ceil to avoid 0-night due to partial days; still clamp to >= 1 where possible.
    recomputed = np.ceil(recomputed).astype("float")
    recomputed = recomputed.where(recomputed >= 1)

    out.loc[invalid, "nights"] = recomputed.loc[invalid]
    return out


def _validation_rationale() -> str:
    return (
        "Exploratory EDA: flag anomalies for review while retaining rows for analysis."
    )


def _resolve_duplicate_keys(df: pd.DataFrame) -> tuple[list[str], str | None]:
    if "session_id" in df.columns:
        return ["session_id"], None
    composite = ["user_id", "session_start", "session_end"]
    if all(col in df.columns for col in composite):
        return composite, None
    fallback = ["user_id", "session_start"]
    if all(col in df.columns for col in fallback):
        return fallback, None
    return [], "Missing session identifier columns for duplicate detection."


def detect_duplicate_sessions(df: pd.DataFrame) -> dict[str, object]:
    """Detect duplicate rows in session-level data."""

    keys, reason = _resolve_duplicate_keys(df)
    base = {
        "keys": keys,
        "decision": "flag_only",
        "action": "retained",
        "rationale": _validation_rationale(),
    }

    if not keys:
        return {
            **base,
            "status": "skipped",
            "reason": reason,
            "duplicate_rows": 0,
            "rows_in_duplicate_groups": 0,
            "duplicate_groups": 0,
        }

    duplicate_rows = df.duplicated(subset=keys, keep="first")
    rows_in_duplicate_groups = df.duplicated(subset=keys, keep=False)
    counts = df[keys].value_counts(dropna=False)
    duplicate_groups = int((counts > 1).sum())

    return {
        **base,
        "status": "evaluated",
        "duplicate_rows": int(duplicate_rows.sum()),
        "rows_in_duplicate_groups": int(rows_in_duplicate_groups.sum()),
        "duplicate_groups": duplicate_groups,
    }


def _range_check(
    df: pd.DataFrame,
    *,
    column: str,
    min_value: float | int | None = None,
    max_value: float | int | None = None,
) -> dict[str, object]:
    base = {
        "column": column,
        "min_allowed": min_value,
        "max_allowed": max_value,
        "decision": "flag_only",
        "action": "retained",
        "rationale": _validation_rationale(),
    }

    if column not in df.columns:
        return {
            **base,
            "status": "skipped",
            "reason": "Column not available for range check.",
            "invalid_count": 0,
        }

    s = pd.to_numeric(df[column], errors="coerce")
    invalid = pd.Series(False, index=df.index)
    if min_value is not None:
        invalid |= s < min_value
    if max_value is not None:
        invalid |= s > max_value
    invalid &= s.notna()

    return {
        **base,
        "status": "evaluated",
        "invalid_count": int(invalid.sum()),
    }


def _datetime_order_check(
    df: pd.DataFrame, *, name: str, earlier_col: str, later_col: str, comparison: str
) -> dict[str, object]:
    base = {
        "name": name,
        "comparison": comparison,
        "decision": "flag_only",
        "action": "retained",
        "rationale": _validation_rationale(),
    }

    if earlier_col not in df.columns or later_col not in df.columns:
        return {
            **base,
            "status": "skipped",
            "reason": "Required columns missing for logical check.",
            "invalid_count": 0,
        }

    earlier = pd.to_datetime(df[earlier_col], errors="coerce", utc=True)
    later = pd.to_datetime(df[later_col], errors="coerce", utc=True)
    invalid = earlier.notna() & later.notna() & (later < earlier)

    return {
        **base,
        "status": "evaluated",
        "invalid_count": int(invalid.sum()),
    }


# Notes: Apply validity rules and log their impact for metadata.
def apply_validity_rules(
    df: pd.DataFrame, config: EDAConfig
) -> tuple[
    pd.DataFrame,
    dict[str, RuleImpact],
    dict[str, int | str],
    dict[str, object],
]:
    """Apply validity rules and capture their impact for metadata."""

    out = df.copy()
    validity_rules: dict[str, RuleImpact] = {}
    invalid_hotel_nights_meta: dict[str, int | str] = {}
    validation_checks = {
        "duplicates": detect_duplicate_sessions(out),
        "range_checks": {
            "session_duration_sec": _range_check(
                out, column="session_duration_sec", min_value=0
            ),
            "age_years": _range_check(
                out, column="age_years", min_value=0, max_value=120
            ),
            "nights": _range_check(out, column="nights", min_value=1),
            "rooms": _range_check(out, column="rooms", min_value=1),
            "seats": _range_check(out, column="seats", min_value=1),
        },
        "logical_checks": {
            "session_end_before_start": _datetime_order_check(
                out,
                name="session_end_before_start",
                earlier_col="session_start",
                later_col="session_end",
                comparison="session_end < session_start",
            ),
            "birthdate_after_session_start": _datetime_order_check(
                out,
                name="birthdate_after_session_start",
                earlier_col="birthdate",
                later_col="session_start",
                comparison="birthdate > session_start",
            ),
        },
    }

    if "nights" in out.columns:
        nights = pd.to_numeric(out["nights"], errors="coerce")
        invalid_mask = nights.isna() | (nights <= 0)
        invalid_detected = int(invalid_mask.sum())

        rows_before = int(len(out))
        policy = config.cleaning.invalid_hotel_nights_policy

        if policy == "drop":
            out = out.loc[~invalid_mask].copy()
            invalid_hotel_nights_meta = {
                "policy": "drop",
                "invalid_detected": invalid_detected,
                "dropped_rows": invalid_detected,
                "decision": "drop",
                "rationale": (
                    "Configured policy for known hotel nights anomaly; rows removed."
                ),
            }
        else:
            out = fix_invalid_hotel_nights(out, policy=policy)
            recomputed = pd.to_numeric(out["nights"], errors="coerce")
            recomputed_success = int((recomputed.loc[invalid_mask] >= 1).sum())
            still_missing = invalid_detected - recomputed_success
            invalid_hotel_nights_meta = {
                "policy": "recompute",
                "invalid_detected": invalid_detected,
                "recomputed_success": recomputed_success,
                "still_missing": still_missing,
                "decision": "recompute",
                "rationale": (
                    "Configured policy for known hotel nights anomaly; recompute to preserve rows."
                ),
            }

        rows_after = int(len(out))
        validity_rules["invalid_hotel_nights"] = RuleImpact(
            rows_before=rows_before,
            rows_after=rows_after,
            rows_removed=rows_before - rows_after,
        )

    return out, validity_rules, invalid_hotel_nights_meta, validation_checks


# Notes: Remove outliers based on configured method and thresholds.
def remove_outliers(
    df: pd.DataFrame, config: EDAConfig
) -> tuple[pd.DataFrame, dict[str, RuleImpact]]:
    """Remove outliers from selected numeric columns.

    Notes:
    - Outliers are removed before user aggregation to reduce distortion of means and rates.
    - Returns the filtered DataFrame plus per-column removed counts for report metadata.
    - Missing values are not treated as outliers (kept), because missingness is itself an EDA signal.
    """

    out = df.copy()
    rules: dict[str, RuleImpact] = {}

    # Notes: Only apply to configured columns that actually exist in the dataset.
    cols = [c for c in config.outliers.columns if c in out.columns]
    if not cols:
        return out, rules

    # Notes: Keep-mask accumulates constraints across columns (intersection).
    mask_keep = pd.Series(True, index=out.index)

    for col in cols:
        s = pd.to_numeric(out[col], errors="coerce")
        rows_before = int(mask_keep.sum())

        if config.outliers.method == "iqr":
            # Notes: IQR method is robust under non-normal distributions.
            q1 = s.quantile(0.25)
            q3 = s.quantile(0.75)
            iqr = q3 - q1
            if pd.isna(iqr) or iqr == 0:
                continue
            lo = q1 - config.outliers.iqr_multiplier * iqr
            hi = q3 + config.outliers.iqr_multiplier * iqr
            keep = s.between(lo, hi) | s.isna()

        elif config.outliers.method == "zscore":
            # Notes: Z-score assumes approximate normality; threshold should be conservative in EDA.
            mu = s.mean()
            sigma = s.std(ddof=0)
            if pd.isna(sigma) or sigma == 0:
                continue
            z = (s - mu) / sigma
            keep = (z.abs() <= config.outliers.zscore_threshold) | s.isna()

        else:
            raise ValueError("outliers.method must be one of: iqr, zscore")

        mask_keep &= keep.fillna(True)
        rows_after = int(mask_keep.sum())
        rules[col] = RuleImpact(
            rows_before=rows_before,
            rows_after=rows_after,
            rows_removed=rows_before - rows_after,
        )

    return out.loc[mask_keep].copy(), rules


# Notes: Aggregate session data to a customer-level table.
def aggregate_user_level(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate session-level data to one row per user.

    Notes:
    - This is a *first* aggregated table for Step 1; deeper feature engineering happens in Step 2.
    - Aggregations are intentionally simple: counts, means, and booking/cancellation rates.
    - Dimension attributes are carried forward via a stable "first non-null" rule.
    """

    if "user_id" not in df.columns:
        raise KeyError("Expected user_id column for aggregation")

    # Notes: Group by user_id to create the customer-level view required by the project.
    g = df.groupby("user_id", dropna=False)

    # Notes: Start with core behavioral KPIs most relevant to initial segmentation hypotheses.
    user = pd.DataFrame(
        {
            "n_sessions": g["session_id"].nunique(),
            "avg_page_clicks": g["page_clicks"].mean(),
            "p_flight_booked": g["flight_booked"].mean(),
            "p_hotel_booked": g["hotel_booked"].mean(),
            "p_cancellation_session": g["cancellation"].mean(),
            "avg_base_fare_usd": g["base_fare_usd"].mean(),
            "avg_hotel_per_room_usd": g["hotel_per_room_usd"].mean(),
            "avg_nights": g["nights"].mean(),
            "avg_rooms": g["rooms"].mean(),
            "avg_seats": g["seats"].mean(),
        }
    ).reset_index()

    # Notes: Re-attach demographic/dimension fields for descriptive breakdowns.
    dim_cols = [
        "gender",
        "married",
        "has_children",
        "home_country",
        "home_city",
        "home_airport",
        "sign_up_date",
        "birthdate",
    ]
    dim_cols = [c for c in dim_cols if c in df.columns]
    if dim_cols:
        # Notes: Use "first non-null" to avoid accidental mixing when fields are repeated per session.
        dim = g[dim_cols].agg(
            lambda s: s.dropna().iloc[0] if len(s.dropna()) else pd.NA
        )
        user = user.merge(dim.reset_index(), on="user_id", how="left")

    return user


# Notes: Build the EDA run metadata payload.
def build_metadata(
    config: EDAConfig,
    row_counts: dict[str, int],
    n_rows_raw: int,
    n_rows_after_validity: int,
    n_rows_clean: int,
    validity_rules: dict[str, RuleImpact],
    outlier_rules: dict[str, RuleImpact],
    invalid_hotel_nights_meta: dict[str, int | str],
    validation_checks: dict[str, object] | None = None,
) -> dict[str, object]:
    """Create a run metadata payload saved next to artifacts.

    Notes:
    - Metadata is part of the artifact contract: it explains *what was run* and *what was produced*.
    - This enables reviewers (and future you) to reproduce the artifact precisely.
    """

    return {
        "config": asdict(config),
        "source_table_row_counts": row_counts,
        "rows": {
            "session_level_raw": n_rows_raw,
            "session_level_after_validity": n_rows_after_validity,
            "session_level_clean": n_rows_clean,
        },
        "validity_rules": {
            name: asdict(impact) for name, impact in validity_rules.items()
        },
        "validation_checks": validation_checks or {},
        "outliers": {col: asdict(impact) for col, impact in outlier_rules.items()},
        "invalid_hotel_nights": invalid_hotel_nights_meta,
        "outliers_removed_by_column": {
            col: impact.rows_removed for col, impact in outlier_rules.items()
        },
    }
