import pandas as pd
import pandera as pa
import pytest

from traveltide.contracts.eda import (
    SESSION_CLEAN_SCHEMA,
    SESSION_RAW_SCHEMA,
    USER_AGGREGATE_SCHEMA,
)


def _raw_session_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "session_id": 1,
                "user_id": 10,
                "trip_id": 100,
                "session_start": "2024-01-01T10:00:00Z",
                "session_end": "2024-01-01T11:00:00Z",
                "flight_discount": 0.1,
                "hotel_discount": 0.2,
                "flight_discount_amount": 15.0,
                "hotel_discount_amount": 20.0,
                "flight_booked": True,
                "hotel_booked": False,
                "page_clicks": 5,
                "cancellation": False,
                "birthdate": "1990-01-01",
                "gender": "F",
                "married": True,
                "has_children": False,
                "home_country": "USA",
                "home_city": "Austin",
                "home_airport": "AUS",
                "sign_up_date": "2020-01-01",
                "origin_airport": "AUS",
                "destination": "LAX",
                "destination_airport": "LAX",
                "seats": 1,
                "return_flight_booked": True,
                "departure_time": "2024-02-01T12:00:00Z",
                "return_time": "2024-02-05T12:00:00Z",
                "checked_bags": 1,
                "trip_airline": "TT",
                "base_fare_usd": 200.0,
                "hotel_name": "Hotel",
                "nights": 4.0,
                "rooms": 1.0,
                "check_in_time": "2024-02-01T15:00:00Z",
                "check_out_time": "2024-02-05T11:00:00Z",
                "hotel_per_room_usd": 120.0,
            }
        ]
    )


def test_session_raw_schema_validates() -> None:
    df = _raw_session_frame()
    validated = SESSION_RAW_SCHEMA.validate(df, lazy=True)
    assert len(validated) == 1


def test_session_clean_schema_validates() -> None:
    df = _raw_session_frame()
    df["session_duration_sec"] = 3600.0
    df["age_years"] = 34.0
    df["customer_tenure_days"] = 1460.0
    validated = SESSION_CLEAN_SCHEMA.validate(df, lazy=True)
    assert len(validated) == 1


def test_user_aggregate_schema_validates() -> None:
    user_df = pd.DataFrame(
        [
            {
                "user_id": 10,
                "n_sessions": 5,
                "avg_page_clicks": 4.2,
                "p_flight_booked": 0.8,
                "p_hotel_booked": 0.6,
                "p_cancellation_session": 0.1,
                "avg_base_fare_usd": 210.5,
                "avg_hotel_per_room_usd": 130.0,
                "avg_nights": 3.5,
                "avg_rooms": 1.0,
                "avg_seats": 1.2,
                "gender": "F",
                "married": True,
                "has_children": False,
                "home_country": "USA",
                "home_city": "Austin",
                "home_airport": "AUS",
                "sign_up_date": "2020-01-01",
                "birthdate": "1990-01-01",
            }
        ]
    )
    validated = USER_AGGREGATE_SCHEMA.validate(user_df, lazy=True)
    assert len(validated) == 1


def test_schema_missing_required_column_fails() -> None:
    df = _raw_session_frame().drop(columns=["session_id"])
    with pytest.raises(pa.errors.SchemaErrors):
        SESSION_RAW_SCHEMA.validate(df, lazy=True)


def test_schema_unexpected_column_fails() -> None:
    df = _raw_session_frame()
    df["unexpected"] = 1
    with pytest.raises(pa.errors.SchemaErrors):
        SESSION_RAW_SCHEMA.validate(df, lazy=True)
