"""Orchestrated EDA pipeline for Step 1 (TT-012).

Notes:
- This module is the single orchestration entrypoint for generating the EDA artifact directory.
- It wires together config loading, DB extraction, preprocessing, aggregation, metadata persistence,
  and report rendering.
- The artifact directory is versioned by timestamp to ensure runs are comparable and auditable.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

from .config import load_config
from .extract import extract_session_level, extract_table_row_counts
from .preprocess import (
    add_derived_columns,
    aggregate_user_level,
    apply_validity_rules,
    build_metadata,
    remove_outliers,
)
from .report import build_basic_charts, render_html_report


def _timestamp_slug() -> str:
    # Notes: Generates a stable UTC timestamp folder name to version artifacts deterministically.
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def run_eda(*, config_path: str, outdir: str) -> Path:
    """Run the Step 1 EDA pipeline and write a versioned artifact directory.

    Notes:
    - Returns the created run directory for CLI printing and automation.
    - Failure should be loud (exceptions) to avoid producing partial/untrustworthy artifacts.
    """

    # Notes: Load config once and pass typed config through the pipeline for determinism.
    config = load_config(config_path)

    # Notes: Create a new versioned artifact directory per run; fail if it already exists.
    base = Path(outdir)
    run_dir = base / _timestamp_slug()
    run_dir.mkdir(parents=True, exist_ok=False)

    # Notes: Keep data artifacts separate from report/metadata within the run directory.
    data_dir = run_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # 1) Extract
    # Notes: Capture raw DB scale and then cohort-filtered extraction dataset.
    row_counts = extract_table_row_counts()
    raw = extract_session_level(config)

    # 2) Preprocess
    # Notes: Derive consistent columns, then apply anomaly fixes and outlier removal.
    df = add_derived_columns(raw)
    df_valid, validity_rules, invalid_hotel_nights_meta = apply_validity_rules(
        df, config
    )
    df_clean, outlier_rules = remove_outliers(df_valid, config)

    # 3) Aggregate
    # Notes: Create a first customer-level table; deeper feature engineering comes later.
    user = aggregate_user_level(df_clean)

    # 4) Persist data artifacts
    # Notes: Parquet is efficient and preserves dtypes; artifacts are used by later steps.
    session_path = data_dir / "sessions_clean.parquet"
    user_path = data_dir / "users_agg.parquet"
    df_clean.to_parquet(session_path, index=False)
    user.to_parquet(user_path, index=False)

    # 5) Metadata
    # Notes: Persist config + row counts + outlier impact as audit trail.
    meta = build_metadata(
        config=config,
        row_counts=row_counts,
        n_rows_raw=int(len(raw)),
        n_rows_after_validity=int(len(df_valid)),
        n_rows_clean=int(len(df_clean)),
        validity_rules=validity_rules,
        outlier_rules=outlier_rules,
        invalid_hotel_nights_meta=invalid_hotel_nights_meta,
    )
    (run_dir / "metadata.yaml").write_text(
        yaml.safe_dump(meta, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    (run_dir / "metadata.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 6) Report
    # Notes: Currently HTML-only to keep the first version minimal and dependency-light.
    if config.report.output_format != "html":
        raise ValueError("report.output_format currently supports: html")

    charts = build_basic_charts(df_clean)
    render_html_report(
        out_path=run_dir / "eda_report.html",
        title=config.report.title,
        metadata=meta,
        session_df=df_clean,
        user_df=user,
        charts=charts,
        sample_rows=config.report.include_sample_rows,
    )

    return run_dir
