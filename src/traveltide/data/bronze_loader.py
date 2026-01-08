"""
traveltide.data.bronze_loader

Purpose
-------
Provide local Bronze data access for the TravelTide pipeline.

Why it exists
-------------
Raw data is now shipped with the repository under `data/bronze`, so the
pipeline needs a deterministic, offline-friendly loader that targets the
local filesystem rather than cloud storage.

How it works
------------
- Resolve the repository root and default Bronze directory.
- Construct file paths for requested tables.
- Load CSV or Parquet files into pandas DataFrames.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd


@dataclass(frozen=True)
class BronzeConfig:
    """Configuration describing where Bronze data files live."""

    # Notes: Encapsulates the resolved filesystem location for reproducible access.
    base_path: Path


def resolve_bronze_config(base_path: Path | None = None) -> BronzeConfig:
    """Resolve the Bronze configuration for local, repository-based datasets."""

    # Notes: Default to the repository-level data/bronze directory for portability.
    repo_root = Path(__file__).resolve().parents[3]
    resolved_base = base_path or repo_root / "data" / "bronze"
    return BronzeConfig(base_path=resolved_base)


def build_bronze_path(
    table: str,
    ext: str = "csv",
    config: BronzeConfig | None = None,
) -> Path:
    """Build the file path for a Bronze table stored on disk."""

    # Notes: Centralizes path construction to keep table naming consistent.
    cfg = config or resolve_bronze_config()
    filename = f"{table}.{ext}"
    return cfg.base_path / filename


def resolve_bronze_table_path(
    table: str,
    ext: str = "csv",
    config: BronzeConfig | None = None,
) -> Path:
    """Resolve a Bronze table path, including the `_full` filename convention."""

    # Notes: Fall back to `{table}_full` when the base filename is absent.
    base_path = build_bronze_path(table, ext=ext, config=config)
    if base_path.exists():
        return base_path
    full_path = build_bronze_path(f"{table}_full", ext=ext, config=config)
    return full_path


def load_table_from_bronze(
    table: str,
    ext: str = "csv",
    config: BronzeConfig | None = None,
) -> pd.DataFrame:
    """Load a single Bronze table from the local filesystem."""

    # Notes: Supports CSV and Parquet for local reproducibility.
    path = resolve_bronze_table_path(table, ext=ext, config=config)
    extension = ext.lower()
    if extension == "csv":
        return pd.read_csv(path)
    if extension == "parquet":
        return pd.read_parquet(path)
    raise ValueError(f"Unsupported extension: {ext}")


def load_bronze_tables(
    tables: Iterable[str],
    ext: str = "csv",
    config: BronzeConfig | None = None,
) -> dict[str, pd.DataFrame]:
    """Load multiple Bronze tables from the local filesystem."""

    # Notes: Keeps multi-table loading consistent for downstream pipelines.
    return {
        table: load_table_from_bronze(table, ext=ext, config=config) for table in tables
    }
