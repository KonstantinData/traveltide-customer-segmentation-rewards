"""
traveltide.data.raw_loader

Purpose
-------
Provide local raw data access for the TravelTide pipeline.

Why it exists
-------------
Raw data is shipped with the repository under `data/`, so the pipeline needs a
local, deterministic loader that targets the filesystem rather than cloud storage.

How it works
------------
- Resolve the repository root and default raw data directory.
- Construct file paths for requested tables.
- Load CSV or Parquet files into pandas DataFrames.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd


@dataclass(frozen=True)
class RawConfig:
    """Configuration describing where raw data files live."""

    # Notes: Encapsulates the resolved filesystem location for reproducible access.
    base_path: Path


def resolve_raw_config(base_path: Path | None = None) -> RawConfig:
    """Resolve the raw data configuration for local, repository-based datasets."""

    # Notes: Default to the repository-level data directory for portability.
    repo_root = Path(__file__).resolve().parents[3]
    resolved_base = base_path or repo_root / "data"
    return RawConfig(base_path=resolved_base)


def build_raw_path(
    table: str,
    ext: str = "csv",
    config: RawConfig | None = None,
) -> Path:
    """Build the file path for a raw table stored on disk."""

    # Notes: Centralizes path construction to keep table naming consistent.
    cfg = config or resolve_raw_config()
    filename = f"{table}.{ext}"
    return cfg.base_path / filename


def resolve_raw_table_path(
    table: str,
    ext: str = "csv",
    config: RawConfig | None = None,
) -> Path:
    """Resolve a raw table path, including the `_full` filename convention."""

    # Notes: Fall back to `{table}_full` when the base filename is absent.
    base_path = build_raw_path(table, ext=ext, config=config)
    if base_path.exists():
        return base_path
    full_path = build_raw_path(f"{table}_full", ext=ext, config=config)
    return full_path


def load_table_from_raw(
    table: str,
    ext: str = "csv",
    config: RawConfig | None = None,
) -> pd.DataFrame:
    """Load a single raw table from the local filesystem."""

    # Notes: Supports CSV and Parquet for local reproducibility.
    path = resolve_raw_table_path(table, ext=ext, config=config)
    extension = ext.lower()
    if extension == "csv":
        return pd.read_csv(path)
    if extension == "parquet":
        return pd.read_parquet(path)
    raise ValueError(f"Unsupported extension: {ext}")


def load_raw_tables(
    tables: Iterable[str],
    ext: str = "csv",
    config: RawConfig | None = None,
) -> dict[str, pd.DataFrame]:
    """Load multiple raw tables from the local filesystem."""

    # Notes: Keeps multi-table loading consistent for downstream pipelines.
    return {
        table: load_table_from_raw(table, ext=ext, config=config) for table in tables
    }
