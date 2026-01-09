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

import pandas as pd
import yaml

from traveltide.contracts.eda import (
    SESSION_CLEAN_SCHEMA,
    SESSION_RAW_SCHEMA,
    USER_AGGREGATE_SCHEMA,
)
from traveltide.data import load_bronze_tables

from .config import load_config
from .extract import extract_session_level, extract_table_row_counts
from .preprocess import (
    add_derived_columns,
    aggregate_user_level,
    apply_validity_rules,
    build_metadata,
    remove_outliers,
)
from .report import (
    build_basic_charts,
    correlation_pairs,
    data_overview,
    derive_hypotheses,
    derive_key_insights,
    descriptive_stats_table,
    missingness_table,
    render_html_report,
)
from .workflow import annotate_steps, load_workflow, workflow_to_dict


def _timestamp_slug() -> str:
    # Notes: Generates a stable UTC timestamp folder name to version artifacts deterministically.
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def _coerce_columns(
    df: pd.DataFrame,
    *,
    datetime_cols: tuple[str, ...] = (),
    numeric_cols: tuple[str, ...] = (),
) -> pd.DataFrame:
    out = df.copy()
    for col in datetime_cols:
        if col in out.columns:
            out[col] = pd.to_datetime(out[col], errors="coerce", utc=True)
    for col in numeric_cols:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


def _build_silver_tables() -> dict[str, pd.DataFrame]:
    tables = load_bronze_tables(["users", "sessions", "flights", "hotels"])
    sessions = _coerce_columns(
        tables["sessions"],
        datetime_cols=("session_start", "session_end"),
        numeric_cols=("user_id", "page_clicks"),
    )
    users = _coerce_columns(
        tables["users"],
        datetime_cols=("birthdate", "sign_up_date"),
        numeric_cols=("user_id",),
    )
    flights = _coerce_columns(
        tables["flights"],
        datetime_cols=("departure_time", "return_time"),
        numeric_cols=("seats", "checked_bags", "base_fare_usd"),
    )
    hotels = _coerce_columns(
        tables["hotels"],
        datetime_cols=("check_in_time", "check_out_time"),
        numeric_cols=("nights", "rooms", "hotel_per_room_usd"),
    )
    return {
        "sessions": sessions,
        "users": users,
        "flights": flights,
        "hotels": hotels,
    }


def _transform_sessions(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "session_start" in out.columns and "session_end" in out.columns:
        out["session_duration_sec"] = (
            out["session_end"] - out["session_start"]
        ).dt.total_seconds()
    return out


def _transform_users(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "birthdate" in out.columns:
        today = datetime.utcnow().date()
        out["age_years"] = (
            pd.to_datetime(today) - pd.to_datetime(out["birthdate"])
        ).dt.days / 365.25
    if "sign_up_date" in out.columns:
        today = datetime.utcnow().date()
        out["tenure_days"] = (
            pd.to_datetime(today) - pd.to_datetime(out["sign_up_date"])
        ).dt.days
    return out


def _transform_flights(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "departure_time" in out.columns and "return_time" in out.columns:
        out["trip_duration_hours"] = (
            out["return_time"] - out["departure_time"]
        ).dt.total_seconds() / 3600.0
    return out


def _transform_hotels(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "check_in_time" in out.columns and "check_out_time" in out.columns:
        out["stay_duration_nights"] = (
            out["check_out_time"] - out["check_in_time"]
        ).dt.total_seconds() / 86400.0
    return out


def run_eda(*, config_path: str, outdir: str) -> Path:
    """Run the Step 1 EDA pipeline and write a versioned artifact directory.

    Notes:
    - Returns the created run directory for CLI printing and automation.
    - Failure should be loud (exceptions) to avoid producing partial/untrustworthy artifacts.
    """

    # Notes: Load config + workflow once and pass typed config through the pipeline for determinism.
    config = load_config(config_path)
    workflow = load_workflow(Path("eda.yml"))

    # Notes: Create a new versioned artifact directory per run; fail if it already exists.
    base = Path(outdir)
    run_dir = base / _timestamp_slug()
    run_dir.mkdir(parents=True, exist_ok=False)

    # Notes: Keep data artifacts separate from report/metadata within the run directory.
    data_dir = run_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    silver_dir = data_dir / "silver"
    gold_dir = data_dir / "gold"
    silver_dir.mkdir(parents=True, exist_ok=True)
    gold_dir.mkdir(parents=True, exist_ok=True)

    # 1) Extract
    # Notes: Capture raw DB scale and then cohort-filtered extraction dataset.
    row_counts = extract_table_row_counts()
    raw = extract_session_level(config)
    raw = SESSION_RAW_SCHEMA.validate(raw, lazy=True)

    # 2) Preprocess
    # Notes: Derive consistent columns, then apply anomaly fixes and outlier removal.
    df = add_derived_columns(raw)
    df_valid, validity_rules, invalid_hotel_nights_meta = apply_validity_rules(
        df, config
    )
    df_clean, outlier_rules = remove_outliers(df_valid, config)
    df_clean = SESSION_CLEAN_SCHEMA.validate(df_clean, lazy=True)

    # 3) Aggregate
    # Notes: Create a first customer-level table; deeper feature engineering comes later.
    user = aggregate_user_level(df_clean)
    user = USER_AGGREGATE_SCHEMA.validate(user, lazy=True)

    # 3a) EDA summaries for workflow steps and reporting
    overview = data_overview(raw)
    session_missing = missingness_table(df_clean)
    correlations = correlation_pairs(df_clean)
    session_stats = descriptive_stats_table(df_clean)
    user_stats = descriptive_stats_table(user)
    key_insights = derive_key_insights(session_missing, outlier_rules, correlations)
    hypotheses = derive_hypotheses(correlations)
    charts = build_basic_charts(df_clean)
    workflow_steps = annotate_steps(
        workflow,
        outputs={
            "objective_definition": [
                "Scope defined in config/eda.yaml cohort parameters."
            ],
            "data_overview": [
                f"Rows: {overview['rows']}; Columns: {overview['columns']}."
            ],
            "data_quality_check": [
                f"Missingness captured for {len(session_missing)} session columns."
            ],
            "outlier_analysis": [
                f"Outlier method: {config.outliers.method}; columns: {', '.join(config.outliers.columns)}."
            ],
            "descriptive_statistics": [
                f"Computed stats for {len(session_stats)} session numeric columns."
            ],
            "distribution_analysis": [
                f"Distribution charts: {', '.join(charts.keys()) or 'none'}."
            ],
            "visualization": ["Visualization charts embedded in the EDA report."],
            "relationship_analysis": [
                f"Top correlations computed: {len(correlations)} pairs."
            ],
            "key_insights": key_insights,
            "hypothesis_generation": hypotheses,
        },
    )

    # 4) Persist data artifacts
    # Notes: Parquet is efficient and preserves dtypes; artifacts are used by later steps.
    session_path = data_dir / "sessions_clean.parquet"
    user_path = data_dir / "users_agg.parquet"
    df_clean.to_parquet(session_path, index=False)
    user.to_parquet(user_path, index=False)

    # 4a) Silver + Gold layer artifacts
    silver_tables = _build_silver_tables()
    silver_tables["flights"].to_parquet(
        silver_dir / "flights_cleaned.parquet", index=False
    )
    silver_tables["hotels"].to_parquet(
        silver_dir / "hotels_cleaned.parquet", index=False
    )
    silver_tables["sessions"].to_parquet(
        silver_dir / "sessions_cleaned.parquet", index=False
    )
    silver_tables["users"].to_parquet(
        silver_dir / "users_cleaned.parquet", index=False
    )

    _transform_flights(silver_tables["flights"]).to_parquet(
        gold_dir / "flights_transformed.parquet", index=False
    )
    _transform_hotels(silver_tables["hotels"]).to_parquet(
        gold_dir / "hotels_transformed.parquet", index=False
    )
    _transform_sessions(silver_tables["sessions"]).to_parquet(
        gold_dir / "sessions_transformed.parquet", index=False
    )
    _transform_users(silver_tables["users"]).to_parquet(
        gold_dir / "users_transformed.parquet", index=False
    )

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
    meta["workflow"] = {
        "definition": workflow_to_dict(workflow),
        "overview": overview,
        "steps": workflow_steps,
    }
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

    render_html_report(
        out_path=run_dir / "eda_report.html",
        title=config.report.title,
        metadata=meta,
        session_df=df_clean,
        user_df=user,
        charts=charts,
        sample_rows=config.report.include_sample_rows,
        workflow=workflow_to_dict(workflow),
        workflow_steps=workflow_steps,
        overview=overview,
        session_stats=session_stats,
        user_stats=user_stats,
        correlations=correlations,
        key_insights=key_insights,
        hypotheses=hypotheses,
    )

    return run_dir
