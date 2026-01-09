# Description: Orchestrated EDA pipeline for Step 1 artifacts.
"""Orchestrated EDA pipeline for Step 1 (TT-012).

Notes:
- This module is the single orchestration entrypoint for generating the EDA artifact directory.
- It wires together config loading, DB extraction, preprocessing, aggregation, metadata persistence,
  and report rendering.
- The artifact directory is versioned by timestamp to ensure runs are comparable and auditable.
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import yaml

from traveltide.contracts.eda import (
    SESSION_CLEAN_SCHEMA,
    SESSION_RAW_SCHEMA,
    USER_AGGREGATE_SCHEMA,
)

from .clustering_explore import run_clustering_exploration
from .config import load_config
from .extract import (
    extract_eda_tables,
    extract_session_level_full,
    extract_table_row_counts,
    filter_session_level,
)
from .preprocess import (
    add_derived_columns,
    aggregate_user_level,
    apply_validity_rules,
    build_metadata,
    clean_flights_table,
    clean_hotels_table,
    clean_sessions_table,
    clean_users_table,
    remove_outliers,
    transform_flights_table,
    transform_hotels_table,
    transform_sessions_table,
    transform_users_table,
)
from .report import (
    build_basic_charts,
    build_validation_summary,
    correlation_pairs,
    data_overview,
    derive_hypotheses,
    derive_key_insights,
    descriptive_stats_table,
    missingness_table,
    render_html_report,
)
from .transform_experiments import run_transform_experiments
from .workflow import annotate_steps, load_workflow, workflow_to_dict


# Notes: Create deterministic UTC run directory names.
def _timestamp_slug() -> str:
    # Notes: Generates a stable UTC timestamp folder name to version artifacts deterministically.
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


# Notes: Orchestrate extraction, cleaning, aggregation, and report generation.
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
    cleaned_dir = data_dir / "cleaned"
    transformed_dir = data_dir / "transformed"
    cleaned_dir.mkdir(parents=True, exist_ok=True)
    transformed_dir.mkdir(parents=True, exist_ok=True)

    # 1) Extract
    # Notes: Capture raw DB scale and the unfiltered extraction dataset for exploration.
    row_counts = extract_table_row_counts()
    raw_full = extract_session_level_full()
    raw_full = SESSION_RAW_SCHEMA.validate(raw_full, lazy=True)

    # Notes: Apply cohort/extraction filters only after exploration is assembled.
    raw = filter_session_level(raw_full, config)
    raw = SESSION_RAW_SCHEMA.validate(raw, lazy=True)

    # 2) Preprocess (full dataset for exploration/reporting)
    # Notes: Derive consistent columns, then apply anomaly fixes and outlier removal.
    full_df = add_derived_columns(raw_full)
    (
        full_df_valid,
        full_validity_rules,
        full_invalid_hotel_nights_meta,
        full_validation_checks,
    ) = apply_validity_rules(full_df, config)
    full_df_clean, full_outlier_rules = remove_outliers(full_df_valid, config)
    full_df_clean = SESSION_CLEAN_SCHEMA.validate(full_df_clean, lazy=True)

    # 2b) Preprocess (cohort-scoped dataset for downstream artifacts)
    cohort_df = add_derived_columns(raw)
    (
        cohort_df_valid,
        cohort_validity_rules,
        cohort_invalid_hotel_nights_meta,
        cohort_validation_checks,
    ) = apply_validity_rules(cohort_df, config)
    cohort_df_clean, cohort_outlier_rules = remove_outliers(cohort_df_valid, config)
    cohort_df_clean = SESSION_CLEAN_SCHEMA.validate(cohort_df_clean, lazy=True)

    # 3) Aggregate (full dataset for exploration)
    # Notes: Create a first customer-level table; deeper feature engineering comes later.
    user = aggregate_user_level(full_df_clean)
    user = USER_AGGREGATE_SCHEMA.validate(user, lazy=True)

    # 3b) Aggregate (cohort-scoped dataset for artifacts)
    cohort_user = aggregate_user_level(cohort_df_clean)
    cohort_user = USER_AGGREGATE_SCHEMA.validate(cohort_user, lazy=True)

    # 3a) EDA summaries for workflow steps and reporting
    overview = data_overview(raw_full)
    session_missing = missingness_table(full_df_clean)
    correlations = correlation_pairs(full_df_clean)
    session_stats = descriptive_stats_table(full_df_clean)
    user_stats = descriptive_stats_table(user)
    key_insights = derive_key_insights(
        session_missing, full_outlier_rules, correlations
    )
    hypotheses = derive_hypotheses(correlations)
    charts = build_basic_charts(full_df_clean)
    validation_summary = build_validation_summary(
        {"validation_checks": full_validation_checks}
    )
    transform_experiments = run_transform_experiments(
        session_df=full_df_clean,
        out_dir=run_dir,
    )
    clustering_exploration = run_clustering_exploration(
        session_df=full_df_clean,
        user_df=user,
        out_dir=run_dir,
    )
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
                "Visualization charts embedded in the EDA report.",
                "Exploratory clustering diagnostics (hypothesis-only) included.",
            ],
            "relationship_analysis": [
                f"Top correlations computed: {len(correlations)} pairs."
            ],
            "key_insights": key_insights,
            "hypothesis_generation": hypotheses,
            "exploratory_transformations": [
                "Exploratory scaling and feature derivations captured; no downstream changes."
            ],
        },
    )

    # 4) Persist data artifacts
    # Notes: Parquet is efficient and preserves dtypes; artifacts are used by later steps.
    session_path = data_dir / "sessions_clean.parquet"
    user_path = data_dir / "users_agg.parquet"
    cohort_df_clean.to_parquet(session_path, index=False)
    cohort_user.to_parquet(user_path, index=False)

    # 4a) Cleaned + transformed artifacts
    raw_tables = extract_eda_tables()
    cleaned_tables = {
        "sessions": clean_sessions_table(raw_tables["sessions"]),
        "users": clean_users_table(raw_tables["users"]),
        "flights": clean_flights_table(raw_tables["flights"]),
        "hotels": clean_hotels_table(raw_tables["hotels"]),
    }
    cleaned_tables["flights"].to_parquet(
        cleaned_dir / "flights_cleaned.parquet", index=False
    )
    cleaned_tables["hotels"].to_parquet(
        cleaned_dir / "hotels_cleaned.parquet", index=False
    )
    cleaned_tables["sessions"].to_parquet(
        cleaned_dir / "sessions_cleaned.parquet", index=False
    )
    cleaned_tables["users"].to_parquet(
        cleaned_dir / "users_cleaned.parquet", index=False
    )

    transform_flights_table(cleaned_tables["flights"]).to_parquet(
        transformed_dir / "flights_transformed.parquet", index=False
    )
    transform_hotels_table(cleaned_tables["hotels"]).to_parquet(
        transformed_dir / "hotels_transformed.parquet", index=False
    )
    transform_sessions_table(cleaned_tables["sessions"]).to_parquet(
        transformed_dir / "sessions_transformed.parquet", index=False
    )
    transform_users_table(cleaned_tables["users"]).to_parquet(
        transformed_dir / "users_transformed.parquet", index=False
    )

    # 5) Metadata
    # Notes: Persist config + row counts + outlier impact as audit trail.
    meta = build_metadata(
        config=config,
        row_counts=row_counts,
        n_rows_raw=int(len(raw)),
        n_rows_raw_full=int(len(raw_full)),
        n_rows_after_validity=int(len(cohort_df_valid)),
        n_rows_clean=int(len(cohort_df_clean)),
        validity_rules=cohort_validity_rules,
        outlier_rules=cohort_outlier_rules,
        invalid_hotel_nights_meta=cohort_invalid_hotel_nights_meta,
        validation_checks=cohort_validation_checks,
    )
    meta["workflow"] = {
        "definition": workflow_to_dict(workflow),
        "overview": overview,
        "steps": workflow_steps,
    }
    meta["exploratory_transformations"] = transform_experiments
    meta["clustering_exploration"] = clustering_exploration["metadata"]
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
        session_df=full_df_clean,
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
        validation_summary=validation_summary,
        transform_experiments=transform_experiments,
        clustering_exploration=clustering_exploration["report"],
    )

    latest_dir = base / "latest"
    if latest_dir.exists() or latest_dir.is_symlink():
        if latest_dir.is_symlink():
            latest_dir.unlink()
        else:
            shutil.rmtree(latest_dir)
    try:
        latest_dir.symlink_to(run_dir, target_is_directory=True)
    except OSError:
        shutil.copytree(run_dir, latest_dir)

    return run_dir
