"""Data extraction layer for the Step 1 (EDA) pipeline (TT-012).

Notes:
- This module is responsible for pulling *raw but analysis-ready* data from Postgres.
- All database access is centralized here to keep the rest of the pipeline deterministic and testable.
- The extraction output is a session-level dataset (1 row per session_id) enriched with user + trip context.
- Secrets must never live in code or config files; only environment variables are used.
"""

from __future__ import annotations

import os

import pandas as pd
from sqlalchemy import create_engine, text

from .config import EDAConfig


def _db_url() -> str:
    # Notes: Retrieves the Postgres connection string from the environment (no secrets in repo).
    url = os.getenv("TRAVELTIDE_DATABASE_URL", "").strip()
    if not url:
        raise RuntimeError(
            "Missing TRAVELTIDE_DATABASE_URL environment variable (required for EDA)."
        )
    return url


def extract_session_level(config: EDAConfig) -> pd.DataFrame:
    """Extract a session-level dataset joined with user + trip context.

    Notes:
    - Granularity: 1 row per sessions.session_id.
    - users is the cohort anchor (sign_up_date filter), sessions is the behavioral fact grain.
    - flights/hotels are LEFT JOINed to keep sessions even when no booking exists.
    - Filtering uses parameterized SQL to avoid SQL injection and improve clarity.
    """

    # Notes: Create SQLAlchemy engine once per extraction to keep connection handling consistent.
    engine = create_engine(_db_url())

    # Notes: WHERE clause assembled from config to keep cohort logic fully declarative.
    where_clauses: list[str] = [
        "u.sign_up_date >= :sign_up_date_start",
        "u.sign_up_date <= :sign_up_date_end",
    ]

    # Notes: Optional extraction constraint for performance; disabled when null in config.
    if config.extraction.session_start_min:
        where_clauses.append("s.session_start >= :session_start_min")

    # Notes: Select includes (1) session facts, (2) user dimensions, (3) trip enrichments.
    sql = f"""
        SELECT
            -- Session facts (behavioral)
            s.session_id,
            s.user_id,
            s.trip_id,
            s.session_start,
            s.session_end,
            s.flight_discount,
            s.hotel_discount,
            s.flight_discount_amount,
            s.hotel_discount_amount,
            s.flight_booked,
            s.hotel_booked,
            s.page_clicks,
            s.cancellation,

            -- User attributes (dimension)
            u.birthdate,
            u.gender,
            u.married,
            u.has_children,
            u.home_country,
            u.home_city,
            u.home_airport,
            u.sign_up_date,

            -- Flight attributes (trip enrichment)
            f.origin_airport,
            f.destination,
            f.destination_airport,
            f.seats,
            f.return_flight_booked,
            f.departure_time,
            f.return_time,
            f.checked_bags,
            f.trip_airline,
            f.base_fare_usd,

            -- Hotel attributes (trip enrichment)
            h.hotel_name,
            h.nights,
            h.rooms,
            h.check_in_time,
            h.check_out_time,
            h.hotel_per_room_usd
        FROM sessions s
        JOIN users u
            ON u.user_id = s.user_id
        LEFT JOIN flights f
            ON f.trip_id = s.trip_id
        LEFT JOIN hotels h
            ON h.trip_id = s.trip_id
        WHERE {" AND ".join(where_clauses)}
    """

    # Notes: Parameter dict keeps SQL readable and prevents accidental string formatting issues.
    params = {
        "sign_up_date_start": config.cohort.sign_up_date_start,
        "sign_up_date_end": config.cohort.sign_up_date_end,
        "session_start_min": config.extraction.session_start_min,
    }

    # Notes: Use a single connection context to avoid leaking connections in long runs.
    with engine.connect() as conn:
        df = pd.read_sql(text(sql), conn, params=params)

    return df


def extract_table_row_counts() -> dict[str, int]:
    """Return row counts for core tables.

    Notes:
    - This is used for report context (schema scale) and reproducibility metadata.
    - Counts are unfiltered (raw DB counts), not cohort-restricted.
    """

    engine = create_engine(_db_url())
    sql = {
        "users": "SELECT COUNT(*) AS n FROM users",
        "sessions": "SELECT COUNT(*) AS n FROM sessions",
        "flights": "SELECT COUNT(*) AS n FROM flights",
        "hotels": "SELECT COUNT(*) AS n FROM hotels",
    }

    out: dict[str, int] = {}

    # Notes: Execute each count query deterministically to avoid dependence on ordering.
    with engine.connect() as conn:
        for name, q in sql.items():
            out[name] = int(pd.read_sql(text(q), conn).iloc[0]["n"])

    return out
