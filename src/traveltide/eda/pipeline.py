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

from traveltide.contracts.eda import (
    SESSION_CLEAN_SCHEMA,
    SESSION_RAW_SCHEMA,
    USER_AGGREGATE_SCHEMA,
)

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
    descriptive_stats_table,
    derive_hypotheses,
    derive_key_insights,
    missingness_table,
    render_html_report,
)
from .workflow import annotate_steps, load_workflow, workflow_to_dict


def _timestamp_slug() -> str:
    # Notes: Generates a stable UTC timestamp folder name to version artifacts deterministically.
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


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
            "visualization": [
                "Visualization charts embedded in the EDA report."
            ],
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
