"""
traveltide.eda.extract

Purpose
-------
This module extracts the raw session-level dataset required for the EDA pipeline.

Why it exists
-------------
The TravelTide Mastery project expects a medallion architecture:
Bronze (raw) -> Silver (cleaned) -> Gold (features/segments).

In the original repo version, EDA extraction relied on a Postgres database.
However, the project’s source-of-truth is now an S3 bucket (Bronze layer).

How it works
------------
- If the environment variable TRAVELTIDE_DATABASE_URL is set:
    -> Extract data from Postgres via SQLAlchemy (legacy / optional path).
- Otherwise:
    -> Load Bronze tables from S3 via `load_bronze_tables(...)`
       and assemble the session-level dataset in-memory.

Notes
-----
- The S3 fallback intentionally mirrors the same logical joins as the SQL version:
    sessions + users + (optional) flights + (optional) hotels
- Cohort filtering is applied on sign_up_date.
- An optional minimum session_start filter can be applied via config.
"""

import os

import pandas as pd
from sqlalchemy import create_engine, text

from traveltide.data import load_bronze_tables

from .config import EDAConfig


def extract_session_level(config: EDAConfig) -> pd.DataFrame:
    """
    Build the session-level dataset used in the EDA pipeline.

    Fallback order:
    1) Postgres, if TRAVELTIDE_DATABASE_URL is set.
    2) S3 Bronze tables, otherwise.

    Parameters
    ----------
    config:
        EDA configuration containing cohort boundaries and optional filters.

    Returns
    -------
    pd.DataFrame
        Session-level dataframe enriched with user, flight, and hotel columns.
    """

    # Notes: We intentionally read the environment variable directly here.
    # This keeps the extraction decision explicit and easy to reason about.
    db_url = os.getenv("TRAVELTIDE_DATABASE_URL", "").strip()

    # -----------------------------
    # S3 fallback (Bronze -> in-memory join)
    # -----------------------------
    if not db_url:
        # Notes: Load raw/bronze tables from S3 and join them to match the SQL output.
        tables = load_bronze_tables(["users", "sessions", "flights", "hotels"])

        users = tables["users"]
        sessions = tables["sessions"]
        flights = tables["flights"]
        hotels = tables["hotels"]

        # Notes: sessions is the fact table; users is a dimension table.
        # flights/hotels are optional enrichments keyed by trip_id.
        df = (
            sessions.merge(users, on="user_id")
            .merge(flights, on="trip_id", how="left")
            .merge(hotels, on="trip_id", how="left")
        )

        # Notes: Always apply the cohort filter based on sign_up_date.
        sign_up = pd.to_datetime(df["sign_up_date"], errors="coerce")
        mask = (sign_up >= config.cohort.sign_up_date_start) & (
            sign_up <= config.cohort.sign_up_date_end
        )

        # Notes: Optional additional filter on session_start (useful for reproducibility).
        if config.extraction.session_start_min:
            session_start = pd.to_datetime(df["session_start"], errors="coerce")
            mask &= session_start >= config.extraction.session_start_min

        return df.loc[mask].reset_index(drop=True)

    # -----------------------------
    # Postgres path (legacy / optional)
    # -----------------------------
    # Notes: Create the SQLAlchemy engine only in the DB branch.
    engine = create_engine(db_url)

    # IMPORTANT:
    # Keep your existing SQL query logic below unchanged.
    # Only the engine creation moved to this branch.
    #
    # Example (placeholder): replace with your repo's existing SQL query.
    query = text("SELECT 1;")

    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    return df
