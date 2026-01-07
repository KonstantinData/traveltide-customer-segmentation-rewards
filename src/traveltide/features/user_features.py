"""User-level feature engineering for TT-017."""

from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd


def _first_non_null(series: pd.Series) -> object:
    non_null = series.dropna()
    if non_null.empty:
        return pd.NA
    return non_null.iloc[0]


def _mean_numeric(series: pd.Series) -> float:
    return pd.to_numeric(series, errors="coerce").mean()


def _rate_positive(series: pd.Series) -> float:
    values = pd.to_numeric(series, errors="coerce")
    mask = values.notna()
    return (values > 0).where(mask).mean()


def _rate_mean(series: pd.Series) -> float:
    values = pd.to_numeric(series, errors="coerce")
    return values.mean()


def _session_span_days(series: pd.Series) -> float:
    times = pd.to_datetime(series, utc=True, errors="coerce")
    if times.isna().all():
        return np.nan
    span = times.max() - times.min()
    return span.total_seconds() / 86400.0


def build_user_features(df: pd.DataFrame) -> pd.DataFrame:
    """Build a user-level feature table (one row per user)."""

    if "user_id" not in df.columns:
        raise KeyError("Expected user_id column for user feature aggregation")

    out = df.copy()
    if "session_start" in out.columns:
        out["session_start"] = pd.to_datetime(
            out["session_start"], utc=True, errors="coerce"
        )

    g = out.groupby("user_id", dropna=False)

    features = pd.DataFrame(index=g.size().index).rename_axis("user_id")
    features["n_sessions"] = g["session_id"].nunique()
    if "trip_id" in out.columns:
        features["n_trips"] = g["trip_id"].nunique()
    else:
        features["n_trips"] = 0

    mean_map: dict[str, Callable[[pd.Series], float]] = {
        "avg_page_clicks": _mean_numeric,
        "avg_session_duration_sec": _mean_numeric,
        "avg_base_fare_usd": _mean_numeric,
        "avg_hotel_per_room_usd": _mean_numeric,
        "avg_nights": _mean_numeric,
        "avg_rooms": _mean_numeric,
        "avg_seats": _mean_numeric,
        "avg_checked_bags": _mean_numeric,
        "avg_flight_discount": _mean_numeric,
        "avg_hotel_discount": _mean_numeric,
        "avg_flight_discount_amount": _mean_numeric,
        "avg_hotel_discount_amount": _mean_numeric,
        "avg_customer_tenure_days": _mean_numeric,
        "avg_age_years": _mean_numeric,
    }

    source_cols = {
        "avg_page_clicks": "page_clicks",
        "avg_session_duration_sec": "session_duration_sec",
        "avg_base_fare_usd": "base_fare_usd",
        "avg_hotel_per_room_usd": "hotel_per_room_usd",
        "avg_nights": "nights",
        "avg_rooms": "rooms",
        "avg_seats": "seats",
        "avg_checked_bags": "checked_bags",
        "avg_flight_discount": "flight_discount",
        "avg_hotel_discount": "hotel_discount",
        "avg_flight_discount_amount": "flight_discount_amount",
        "avg_hotel_discount_amount": "hotel_discount_amount",
        "avg_customer_tenure_days": "customer_tenure_days",
        "avg_age_years": "age_years",
    }

    for feature, col in source_cols.items():
        if col in out.columns:
            features[feature] = g[col].apply(mean_map[feature])
        else:
            features[feature] = np.nan

    rate_cols = {
        "p_flight_booked": "flight_booked",
        "p_hotel_booked": "hotel_booked",
        "p_cancellation_session": "cancellation",
        "p_return_flight_booked": "return_flight_booked",
    }

    for feature, col in rate_cols.items():
        if col in out.columns:
            features[feature] = g[col].apply(_rate_mean)
        else:
            features[feature] = np.nan

    discount_rate_cols = {
        "p_flight_discount": "flight_discount",
        "p_hotel_discount": "hotel_discount",
    }
    for feature, col in discount_rate_cols.items():
        if col in out.columns:
            features[feature] = g[col].apply(_rate_positive)
        else:
            features[feature] = np.nan

    if "session_start" in out.columns:
        first_session = g["session_start"].min()
        last_session = g["session_start"].max()
        features["first_session_ts"] = first_session
        features["last_session_ts"] = last_session
        features["session_span_days"] = g["session_start"].apply(_session_span_days)
        features["sessions_per_active_day"] = features["n_sessions"] / (
            features["session_span_days"] + 1
        )
    else:
        features["first_session_ts"] = pd.NaT
        features["last_session_ts"] = pd.NaT
        features["session_span_days"] = np.nan
        features["sessions_per_active_day"] = np.nan

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
    dim_cols = [c for c in dim_cols if c in out.columns]
    if dim_cols:
        dim = g[dim_cols].agg(_first_non_null)
        features = features.merge(dim, left_index=True, right_index=True, how="left")

    features = features.reset_index()
    return features
