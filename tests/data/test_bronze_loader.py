"""Unit tests for local Bronze data loading utilities."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from traveltide.data.bronze_loader import (
    BronzeConfig,
    load_table_from_bronze,
)


def _write_csv(path: Path) -> pd.DataFrame:
    """Write a minimal CSV file for loader tests."""

    # Notes: Use deterministic data to validate CSV loading behavior.
    df = pd.DataFrame({"user_id": [1, 2], "value": [10, 20]})
    df.to_csv(path, index=False)
    return df


def _write_parquet(path: Path) -> pd.DataFrame:
    """Write a minimal Parquet file for loader tests."""

    # Notes: Parquet validates the binary loading path.
    df = pd.DataFrame({"user_id": [1, 2], "value": [10.5, 20.5]})
    df.to_parquet(path, index=False)
    return df


def test_load_table_from_bronze_csv(tmp_path: Path) -> None:
    """Load a CSV Bronze table from a custom base path."""

    # Notes: Use a per-test directory to keep filesystem effects isolated.
    base_path = tmp_path / "bronze"
    base_path.mkdir()
    expected = _write_csv(base_path / "sessions.csv")
    config = BronzeConfig(base_path=base_path)

    result = load_table_from_bronze("sessions", ext="csv", config=config)

    pd.testing.assert_frame_equal(result, expected)


def test_load_table_from_bronze_parquet(tmp_path: Path) -> None:
    """Load a Parquet Bronze table from a custom base path."""

    # Notes: Confirm parquet loading respects the same base path contract.
    base_path = tmp_path / "bronze"
    base_path.mkdir()
    expected = _write_parquet(base_path / "sessions.parquet")
    config = BronzeConfig(base_path=base_path)

    result = load_table_from_bronze("sessions", ext="parquet", config=config)

    pd.testing.assert_frame_equal(result, expected)


def test_load_table_from_bronze_full_suffix(tmp_path: Path) -> None:
    """Fallback to the `_full` naming convention when base names are absent."""

    # Notes: Mirrors the repository's bronze filenames (e.g., users_full.csv).
    base_path = tmp_path / "bronze"
    base_path.mkdir()
    expected = _write_csv(base_path / "users_full.csv")
    config = BronzeConfig(base_path=base_path)

    result = load_table_from_bronze("users", ext="csv", config=config)

    pd.testing.assert_frame_equal(result, expected)
