"""Pandera schemas for Step 1 (EDA) artifacts."""

from __future__ import annotations

import pandera as pa
from pandera import Column, DataFrameSchema

# NOTE:
# Raw exports often use UUID-like IDs for session_id/trip_id.
# Therefore we validate them as strings (not int64).
# user_id is kept as Int64 (typical TravelTide dataset uses numeric user IDs).
# If your raw export uses UUIDs for user_id too, switch user_id to pa.String.

SESSION_RAW_SCHEMA = DataFrameSchema(
    {
        "session_id": Column(pa.String, nullable=False),
        "user_id": Column(pa.Int64, nullable=False),
        "trip_id": Column(pa.String, nullable=True),
        "session_start": Column(pa.DateTime, nullable=False),
        # Raw exports may have missing/empty values -> allow null
        "session_end": Column(pa.DateTime, nullable=True),
        "flight_discount": Column(pa.Float64, nullable=True),
        "hotel_discount": Column(pa.Float64, nullable=True),
        "flight_discount_amount": Column(pa.Float64, nullable=True),
        "hotel_discount_amount": Column(pa.Float64, nullable=True),
        "flight_booked": Column(pa.Bool, nullable=True),
        "hotel_booked": Column(pa.Bool, nullable=True),
        "page_clicks": Column(pa.Int64, nullable=True),
        "cancellation": Column(pa.Bool, nullable=True),
        "birthdate": Column(pa.DateTime, nullable=True),
        "gender": Column(pa.String, nullable=True),
        "married": Column(pa.Bool, nullable=True),
        "has_children": Column(pa.Bool, nullable=True),
        "home_country": Column(pa.String, nullable=True),
        "home_city": Column(pa.String, nullable=True),
        "home_airport": Column(pa.String, nullable=True),
        "sign_up_date": Column(pa.DateTime, nullable=False),
        "origin_airport": Column(pa.String, nullable=True),
        "destination": Column(pa.String, nullable=True),
        "destination_airport": Column(pa.String, nullable=True),
        # These often become float64 due to NaNs in pandas.
        # If you want strict nullable integers, see the alternative below.
        "seats": Column(pa.Float64, nullable=True),
        "return_flight_booked": Column(pa.Bool, nullable=True),
        "departure_time": Column(pa.DateTime, nullable=True),
        "return_time": Column(pa.DateTime, nullable=True),
        "checked_bags": Column(pa.Float64, nullable=True),
        "trip_airline": Column(pa.String, nullable=True),
        "base_fare_usd": Column(pa.Float64, nullable=True),
        "hotel_name": Column(pa.String, nullable=True),
        "nights": Column(pa.Float64, nullable=True),
        "rooms": Column(pa.Float64, nullable=True),
        "check_in_time": Column(pa.DateTime, nullable=True),
        "check_out_time": Column(pa.DateTime, nullable=True),
        "hotel_per_room_usd": Column(pa.Float64, nullable=True),
    },
    coerce=True,
    strict=True,
)

SESSION_CLEAN_SCHEMA = DataFrameSchema(
    {
        **SESSION_RAW_SCHEMA.columns,
        "session_duration_sec": Column(pa.Float64, nullable=True),
        "age_years": Column(pa.Float64, nullable=True),
        "customer_tenure_days": Column(pa.Float64, nullable=True),
    },
    coerce=True,
    strict=True,
)

USER_AGGREGATE_SCHEMA = DataFrameSchema(
    {
        "user_id": Column(pa.Int64, nullable=False),
        "n_sessions": Column(pa.Int64, nullable=False),
        "avg_page_clicks": Column(pa.Float64, nullable=True),
        "p_flight_booked": Column(pa.Float64, nullable=True),
        "p_hotel_booked": Column(pa.Float64, nullable=True),
        "p_cancellation_session": Column(pa.Float64, nullable=True),
        "avg_base_fare_usd": Column(pa.Float64, nullable=True),
        "avg_hotel_per_room_usd": Column(pa.Float64, nullable=True),
        "avg_nights": Column(pa.Float64, nullable=True),
        "avg_rooms": Column(pa.Float64, nullable=True),
        "avg_seats": Column(pa.Float64, nullable=True),
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
