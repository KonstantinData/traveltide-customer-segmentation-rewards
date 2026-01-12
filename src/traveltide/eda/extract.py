# Description: Extract session-level EDA datasets from raw tables.
"""
traveltide.eda.extract

Purpose
-------
This module extracts the raw session-level dataset required for the EDA pipeline.

Why it exists
-------------
The TravelTide Mastery project uses raw -> cleaned -> transformed tables.

The project's source-of-truth is the local raw layer under `data/`.
Therefore EDA extraction loads raw tables from disk and assembles the
session-level dataset in-memory.

How it works
------------
- Load raw tables from disk via `load_raw_tables(...)`
- Assemble the session-level dataset by joining:
    sessions + users + (optional) flights + (optional) hotels
- Apply cohort filtering on sign_up_date (user dimension)
- Optionally apply a minimum session_start filter via config
- Optionally enforce a minimum session count per user during the filtered window
- Optionally enforce a minimum page_clicks threshold in the observation window

Notes
-----
- The raw join intentionally mirrors the legacy SQL logic:
    sessions (fact) + users (dimension) + left joins on trip_id for flights/hotels
"""

from __future__ import annotations

from typing import Final, Sequence

import pandas as pd

from traveltide.data import load_raw_tables

from .config import EDAConfig

# Stable output contract: keep column order consistent across runs.
# If some columns are missing in raw, they will be created as NA.
_SESSION_LEVEL_COLUMNS: Final[Sequence[str]] = [
    # Session facts
    "session_id",
    "user_id",
    "trip_id",
    "session_start",
    "session_end",
    "flight_discount",
    "hotel_discount",
    "flight_discount_amount",
    "hotel_discount_amount",
    "flight_booked",
    "hotel_booked",
    "page_clicks",
    "cancellation",
    # User attributes
    "birthdate",
    "gender",
    "married",
    "has_children",
    "home_country",
    "home_city",
    "home_airport",
    "sign_up_date",
    # Flight attributes (optional)
    "origin_airport",
    "destination",
    "destination_airport",
    "seats",
    "return_flight_booked",
    "departure_time",
    "return_time",
    "checked_bags",
    "trip_airline",
    "base_fare_usd",
    # Hotel attributes (optional)
    "hotel_name",
    "nights",
    "rooms",
    "check_in_time",
    "check_out_time",
    "hotel_per_room_usd",
]


_DATETIME_COLS: Final[list[str]] = [
    "session_start",
    "session_end",
    "birthdate",
    "sign_up_date",
    "departure_time",
    "return_time",
    "check_in_time",
    "check_out_time",
]

_NUMERIC_FLOAT_COLS: Final[list[str]] = [
    "flight_discount",
    "hotel_discount",
    "flight_discount_amount",
    "hotel_discount_amount",
    "base_fare_usd",
    "hotel_per_room_usd",
    "nights",
    "rooms",
    # keep these as float to avoid pandas NaN->float coercion issues for ints
    "seats",
    "checked_bags",
]

_INT_COLS: Final[list[str]] = [
    "user_id",
    "page_clicks",
]


# Notes: Normalize session-level columns and order for schema stability.
def _normalize_session_level_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure we return a stable set/order of columns."""

    # Notes: Normalization keeps downstream schema checks deterministic.
    out = df.copy()

    # Add missing columns as NA
    for col in _SESSION_LEVEL_COLUMNS:
        if col not in out.columns:
            out[col] = pd.NA

    # Keep only expected columns, in order
    return out.loc[:, _SESSION_LEVEL_COLUMNS]


# Notes: Coerce raw column types to predictable dtypes.
def _coerce_types(df: pd.DataFrame) -> pd.DataFrame:
    """Coerce raw dtypes into stable, schema-friendly types."""

    # Notes: Casting aligns raw local files with Pandera expectations.
    out = df.copy()

    # IDs: Raw exports often use UUID-like strings for session_id/trip_id.
    if "session_id" in out.columns:
        out["session_id"] = out["session_id"].astype("string")
    if "trip_id" in out.columns:
        out["trip_id"] = out["trip_id"].astype("string")

    # user_id is expected numeric (if your export is UUID, change schema + cast to string)
    for c in _INT_COLS:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce").astype("Int64")

    # Datetimes: parse strings/objects -> datetime64[ns]
    for c in _DATETIME_COLS:
        if c in out.columns:
            out[c] = pd.to_datetime(out[c], errors="coerce")

    # Floats: ensure numeric where expected
    for c in _NUMERIC_FLOAT_COLS:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce").astype("float64")

    # Booleans: ensure True/False/NA consistency (no hard-cast to avoid breaking on odd values)
    for c in [
        "flight_booked",
        "hotel_booked",
        "cancellation",
        "married",
        "has_children",
        "return_flight_booked",
    ]:
        if c in out.columns:
            # Pandera can coerce bool-like values; keep as-is unless clearly numeric/strings.
            pass

    return out


# Notes: Apply cohort + extraction filters to a session-level dataframe.
def _apply_extraction_filters(df: pd.DataFrame, config: EDAConfig) -> pd.DataFrame:
    """Return cohort-filtered session-level data based on config rules."""

    # Cohort filter on sign_up_date.
    mask = pd.Series(True, index=df.index)
    if "sign_up_date" in df.columns:
        sign_up = df["sign_up_date"]
        start = pd.to_datetime(config.cohort.sign_up_date_start)
        end = pd.to_datetime(config.cohort.sign_up_date_end)
        mask &= (sign_up >= start) & (sign_up <= end)

    # Optional filter on minimum session_start.
    if config.extraction.session_start_min and "session_start" in df.columns:
        min_start = pd.to_datetime(config.extraction.session_start_min)
        mask &= df["session_start"] >= min_start

    filtered = df.loc[mask]

    # Optional filter on minimum page_clicks per session.
    if (
        config.extraction.min_page_clicks is not None
        and "page_clicks" in filtered.columns
    ):
        filtered = filtered[
            filtered["page_clicks"] >= config.extraction.min_page_clicks
        ]

    # Optional filter on minimum session count per user.
    if config.extraction.min_sessions and "user_id" in filtered.columns:
        session_counts = (
            filtered.groupby("user_id")["session_id"].nunique().sort_index()
        )
        keep_users = session_counts[session_counts > config.extraction.min_sessions]
        filtered = filtered[filtered["user_id"].isin(keep_users.index)]

    return filtered.reset_index(drop=True)


# Notes: Public helper for reusing cohort filters on pre-joined dataframes.
def filter_session_level(df: pd.DataFrame, config: EDAConfig) -> pd.DataFrame:
    """Filter a session-level dataframe using cohort/extraction config rules."""

    return _apply_extraction_filters(df, config)


# Notes: Build the unfiltered session-level dataset for EDA exploration.
def extract_session_level_full() -> pd.DataFrame:
    """Build the full session-level dataset without cohort filtering."""

    # Notes: Load raw tables from the local data directory (source-of-truth).
    tables = load_raw_tables(["users", "sessions", "flights", "hotels"])

    users = tables["users"]
    sessions = tables["sessions"]
    flights = tables.get("flights")
    hotels = tables.get("hotels")

    # sessions = fact; users = dimension (inner join).
    df = sessions.merge(users, on="user_id", how="inner")

    # Optional enrichments on trip_id.
    if flights is not None and "trip_id" in df.columns and "trip_id" in flights.columns:
        df = df.merge(flights, on="trip_id", how="left")

    if hotels is not None and "trip_id" in df.columns and "trip_id" in hotels.columns:
        df = df.merge(hotels, on="trip_id", how="left")

    # Coerce types BEFORE downstream filtering and schema validation.
    df = _coerce_types(df)
    df = _normalize_session_level_columns(df)
    return df


# Notes: Build the cohort-scoped session-level dataset for EDA.
def extract_session_level(config: EDAConfig) -> pd.DataFrame:
    """
    Build the session-level dataset used in the EDA pipeline from raw files.

    Parameters
    ----------
    config:
        EDA configuration containing cohort boundaries and optional filters.

    Returns
    -------
    pd.DataFrame
        Session-level dataframe enriched with user, flight, and hotel columns.
    """
    df = extract_session_level_full()
    df = _apply_extraction_filters(df, config)
    return df


# Notes: Load raw tables for EDA cleaning/transformation.
def extract_eda_tables() -> dict[str, pd.DataFrame]:
    """Load raw tables needed for the EDA context.

    Notes
    -----
    - Returns raw tables with no filtering so they can be cleaned/transformed separately.
    - Includes flights/hotels alongside sessions/users for cleaned/transformed artifact creation.
    """

    return load_raw_tables(["users", "sessions", "flights", "hotels"])


# Notes: Capture raw row counts for audit metadata.
def extract_table_row_counts() -> dict[str, int]:
    """
    Return raw row counts for core raw tables (unfiltered).

    Used in pipeline metadata as an audit trail (scale/context).
    """
    # Notes: Keep counts unfiltered to reflect the full raw footprint.
    tables = load_raw_tables(["users", "sessions", "flights", "hotels"])
    return {name: int(len(df)) for name, df in tables.items()}
