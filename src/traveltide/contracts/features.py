"""Pandera schemas for Gold feature artifacts (TT-017)."""

from __future__ import annotations

import pandera as pa
from pandera import Column, DataFrameSchema

USER_FEATURES_SCHEMA = DataFrameSchema(
    {
        "user_id": Column(pa.Int64, nullable=False),
        "n_sessions": Column(pa.Int64, nullable=False),
        "n_trips": Column(pa.Int64, nullable=False),
        "avg_page_clicks": Column(pa.Float64, nullable=True),
        "avg_session_duration_sec": Column(pa.Float64, nullable=True),
        "avg_base_fare_usd": Column(pa.Float64, nullable=True),
        "avg_hotel_per_room_usd": Column(pa.Float64, nullable=True),
        "avg_nights": Column(pa.Float64, nullable=True),
        "avg_rooms": Column(pa.Float64, nullable=True),
        "avg_seats": Column(pa.Float64, nullable=True),
        "avg_checked_bags": Column(pa.Float64, nullable=True),
        "avg_flight_discount": Column(pa.Float64, nullable=True),
        "avg_hotel_discount": Column(pa.Float64, nullable=True),
        "avg_flight_discount_amount": Column(pa.Float64, nullable=True),
        "avg_hotel_discount_amount": Column(pa.Float64, nullable=True),
        "avg_customer_tenure_days": Column(pa.Float64, nullable=True),
        "avg_age_years": Column(pa.Float64, nullable=True),
        "p_flight_booked": Column(pa.Float64, nullable=True),
        "p_hotel_booked": Column(pa.Float64, nullable=True),
        "p_cancellation_session": Column(pa.Float64, nullable=True),
        "p_return_flight_booked": Column(pa.Float64, nullable=True),
        "p_flight_discount": Column(pa.Float64, nullable=True),
        "p_hotel_discount": Column(pa.Float64, nullable=True),
        "first_session_ts": Column(pa.DateTime, nullable=True),
        "last_session_ts": Column(pa.DateTime, nullable=True),
        "session_span_days": Column(pa.Float64, nullable=True),
        "sessions_per_active_day": Column(pa.Float64, nullable=True),
        "gender": Column(pa.String, nullable=True),
        "married": Column(pa.Bool, nullable=True),
        "has_children": Column(pa.Bool, nullable=True),
        "home_country": Column(pa.String, nullable=True),
        "home_city": Column(pa.String, nullable=True),
        "home_airport": Column(pa.String, nullable=True),
        "sign_up_date": Column(pa.DateTime, nullable=True),
        "birthdate": Column(pa.DateTime, nullable=True),
    },
    coerce=True,
    strict=True,
)
