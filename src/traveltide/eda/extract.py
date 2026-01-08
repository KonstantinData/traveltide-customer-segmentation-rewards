"""
traveltide.eda.extract

Purpose
-------
This module extracts the raw session-level dataset required for the EDA pipeline.

Why it exists
-------------
The TravelTide Mastery project expects a medallion architecture:
Bronze (raw) -> Silver (cleaned) -> Gold (features/segments).

The project's source-of-truth is an S3 bucket (Bronze layer). Therefore EDA
extraction loads Bronze tables from S3 and assembles the session-level dataset
in-memory.

How it works
------------
- Load Bronze tables from S3 via `load_bronze_tables(...)`
- Assemble the session-level dataset by joining:
    sessions + users + (optional) flights + (optional) hotels
- Apply cohort filtering on sign_up_date (user dimension)
- Optionally apply a minimum session_start filter via config

Notes
-----
- The S3 join intentionally mirrors the legacy SQL logic:
    sessions (fact) + users (dimension) + left joins on trip_id for flights/hotels
"""

from __future__ import annotations

from typing import Final

import pandas as pd

from traveltide.data import load_bronze_tables

from .config import EDAConfig

# Stable output contract: keep column order consistent across runs.
# If some columns are missing in Bronze, they will be created as NA.
_SESSION_LEVEL_COLUMNS: Final[list[str]] = [
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


def _normalize_session_level_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure we return a stable set/order of columns."""
    out = df.copy()

    # Add missing columns as NA
    for col in _SESSION_LEVEL_COLUMNS:
        if col not in out.columns:
            out[col] = pd.NA

    # Keep only expected columns, in order
    return out.loc[:, _SESSION_LEVEL_COLUMNS]


def extract_session_level(config: EDAConfig) -> pd.DataFrame:
    """
    Build the session-level dataset used in the EDA pipeline from S3 Bronze.

    Parameters
    ----------
    config:
        EDA configuration containing cohort boundaries and optional filters.

    Returns
    -------
    pd.DataFrame
        Session-level dataframe enriched with user, flight, and hotel columns.
    """
    # Load raw/bronze tables from S3 (source-of-truth)
    tables = load_bronze_tables(["users", "sessions", "flights", "hotels"])

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

    # Cohort filter on sign_up_date
    sign_up = pd.to_datetime(df["sign_up_date"], errors="coerce")
    start = pd.to_datetime(config.cohort.sign_up_date_start)
    end = pd.to_datetime(config.cohort.sign_up_date_end)
    mask = (sign_up >= start) & (sign_up <= end)

    # Optional filter on minimum session_start
    if config.extraction.session_start_min:
        session_start = pd.to_datetime(df["session_start"], errors="coerce")
        min_start = pd.to_datetime(config.extraction.session_start_min)
        mask &= session_start >= min_start

    df = df.loc[mask].reset_index(drop=True)
    return _normalize_session_level_columns(df)


def extract_table_row_counts() -> dict[str, int]:
    """
    Return raw row counts for core Bronze tables (unfiltered).

    Used in pipeline metadata as an audit trail (scale/context).
    """
    tables = load_bronze_tables(["users", "sessions", "flights", "hotels"])
    return {name: int(len(df)) for name, df in tables.items()}
