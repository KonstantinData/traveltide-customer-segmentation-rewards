from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

from traveltide.features.aggregate import build_customer_features


def test_build_customer_features_columns():
    cfg_path = Path(__file__).resolve().parents[2] / "config" / "features.yaml"
    cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
    features_cfg = cfg["features"]

    df = pd.DataFrame(
        {
            "user_id": ["u1", "u1", "u2"],
            "session_id": ["s1", "s2", "s3"],
            "session_duration_sec": [10, 20, 30],
            "page_clicks": [2, 3, 4],
            "flight_booked": [1, 0, 1],
            "hotel_booked": [0, 0, 1],
            "cancellation": [0, 0, 1],
            "flight_discount": [1, 0, 0],
            "hotel_discount": [0, 0, 1],
            "flight_discount_amount": [5, None, 0],
            "hotel_discount_amount": [None, None, 10],
            "base_fare_usd": [100, 120, 200],
            "hotel_per_room_usd": [None, None, 80],
            "nights": [None, None, 2],
            "rooms": [None, None, 1],
            "seats": [1, 1, 2],
            "checked_bags": [0, 1, 1],
            "return_flight_booked": [0, 1, 1],
            "customer_tenure_days": [100, 100, 50],
            "age_years": [30, 30, 40],
            "home_country": ["US", None, "DE"],
            "home_city": ["NYC", None, "BER"],
            "home_airport": ["JFK", None, "BER"],
            "gender": ["F", None, "M"],
            "married": [1, None, 0],
            "has_children": [0, None, 1],
            "birthdate": [None, None, "1984-01-01"],
        }
    )

    max_cols = ["customer_tenure_days", "age_years"]
    out = build_customer_features(
        df,
        id_col=features_cfg["id_col"],
        session_col=features_cfg["session_col"],
        numeric_means=features_cfg.get("numeric_means", []),
        boolean_means=features_cfg.get("boolean_means", []),
        first_non_null_cols=features_cfg.get("first_non_null", []),
        max_cols=max_cols,
    )

    expected_columns = {
        features_cfg["id_col"],
        "n_sessions",
        *{f"avg_{col}" for col in features_cfg.get("numeric_means", [])},
        *{f"p_{col}" for col in features_cfg.get("boolean_means", [])},
        *max_cols,
        *features_cfg.get("first_non_null", []),
    }

    assert expected_columns.issubset(out.columns)
