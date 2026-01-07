import numpy as np
import pandas as pd

from traveltide.eda.preprocess import aggregate_user_level


def test_aggregate_user_level_handles_missing_dim_columns() -> None:
    df = pd.DataFrame(
        [
            {
                "user_id": 1,
                "session_id": 10,
                "page_clicks": 3,
                "flight_booked": True,
                "hotel_booked": False,
                "cancellation": False,
                "base_fare_usd": 200.0,
                "hotel_per_room_usd": 100.0,
                "nights": 2,
                "rooms": 1,
                "seats": 1,
            },
            {
                "user_id": 1,
                "session_id": 11,
                "page_clicks": 5,
                "flight_booked": False,
                "hotel_booked": True,
                "cancellation": True,
                "base_fare_usd": 300.0,
                "hotel_per_room_usd": 150.0,
                "nights": 3,
                "rooms": 1,
                "seats": 2,
            },
            {
                "user_id": 2,
                "session_id": 20,
                "page_clicks": 2,
                "flight_booked": False,
                "hotel_booked": False,
                "cancellation": False,
                "base_fare_usd": 180.0,
                "hotel_per_room_usd": 90.0,
                "nights": 1,
                "rooms": 1,
                "seats": 1,
            },
        ]
    )

    aggregated = aggregate_user_level(df)

    expected_columns = {
        "user_id",
        "n_sessions",
        "avg_page_clicks",
        "p_flight_booked",
        "p_hotel_booked",
        "p_cancellation_session",
        "avg_base_fare_usd",
        "avg_hotel_per_room_usd",
        "avg_nights",
        "avg_rooms",
        "avg_seats",
    }
    assert set(aggregated.columns) == expected_columns
    assert aggregated.loc[aggregated["user_id"] == 1, "n_sessions"].iloc[0] == 2


def test_aggregate_user_level_uses_first_non_null_dimension_values() -> None:
    df = pd.DataFrame(
        [
            {
                "user_id": 1,
                "session_id": 10,
                "page_clicks": 3,
                "flight_booked": True,
                "hotel_booked": False,
                "cancellation": False,
                "base_fare_usd": 200.0,
                "hotel_per_room_usd": 100.0,
                "nights": 2,
                "rooms": 1,
                "seats": 1,
                "gender": pd.NA,
                "home_country": pd.NA,
                "sign_up_date": pd.NA,
                "birthdate": pd.NA,
            },
            {
                "user_id": 1,
                "session_id": 11,
                "page_clicks": 5,
                "flight_booked": False,
                "hotel_booked": True,
                "cancellation": True,
                "base_fare_usd": 300.0,
                "hotel_per_room_usd": 150.0,
                "nights": 3,
                "rooms": 1,
                "seats": 2,
                "gender": "F",
                "home_country": "USA",
                "sign_up_date": "2020-01-01",
                "birthdate": "1990-01-01",
            },
        ]
    )

    aggregated = aggregate_user_level(df)
    row = aggregated.loc[aggregated["user_id"] == 1].iloc[0]

    assert row["gender"] == "F"
    assert row["home_country"] == "USA"
    assert row["sign_up_date"] == "2020-01-01"
    assert row["birthdate"] == "1990-01-01"


def test_aggregate_user_level_keeps_nan_user_ids() -> None:
    df = pd.DataFrame(
        [
            {
                "user_id": 1,
                "session_id": 10,
                "page_clicks": 3,
                "flight_booked": True,
                "hotel_booked": False,
                "cancellation": False,
                "base_fare_usd": 200.0,
                "hotel_per_room_usd": 100.0,
                "nights": 2,
                "rooms": 1,
                "seats": 1,
            },
            {
                "user_id": np.nan,
                "session_id": 11,
                "page_clicks": 5,
                "flight_booked": False,
                "hotel_booked": True,
                "cancellation": False,
                "base_fare_usd": 150.0,
                "hotel_per_room_usd": 90.0,
                "nights": 1,
                "rooms": 1,
                "seats": 1,
            },
        ]
    )

    aggregated = aggregate_user_level(df)

    assert len(aggregated) == 2
    assert aggregated["user_id"].isna().any()
