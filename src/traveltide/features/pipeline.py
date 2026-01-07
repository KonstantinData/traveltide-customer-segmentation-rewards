"""Gold feature pipeline (TT-017)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from traveltide.contracts.features import USER_FEATURES_SCHEMA

from .user_features import build_user_features


def run_user_features(*, input_path: str, output_path: str) -> Path:
    """Build and persist the user-level feature table."""

    source = Path(input_path)
    target = Path(output_path)
    if not source.exists():
        raise FileNotFoundError(f"Input file not found: {source}")

    df = pd.read_parquet(source)
    features = build_user_features(df)
    features = USER_FEATURES_SCHEMA.validate(features, lazy=True)

    target.parent.mkdir(parents=True, exist_ok=True)
    features.to_parquet(target, index=False)
    return target
