"""Segmentation job runner (TT-026)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

from .evaluation import (
    DBSCANConfig,
    EvaluationConfig,
    build_decision_report,
    compare_algorithms,
    decision_report_to_markdown,
    run_k_sweep,
    run_seed_sweep,
)
from .pipeline import PCAConfig, SegmentationConfig, run_segmentation


def _build_pca_config(pca_section: dict[str, object]) -> PCAConfig | None:
    if not pca_section.get("enabled", False):
        return None
    return PCAConfig(n_components=pca_section["n_components"])


def _build_dbscan_config(dbscan_section: dict[str, object]) -> DBSCANConfig | None:
    if not dbscan_section.get("enabled", False):
        return None
    settings = {key: value for key, value in dbscan_section.items() if key != "enabled"}
    return DBSCANConfig(**settings)


def _extract_silhouette(k_sweep: pd.DataFrame, chosen_k: int) -> float | None:
    matches = k_sweep.loc[k_sweep["k"] == chosen_k, "silhouette"]
    if matches.empty:
        return None
    value = matches.iloc[0]
    if pd.isna(value):
        return None
    return float(value)


def run_segmentation_job(config_path: str) -> Path:
    """Run the segmentation pipeline from a YAML configuration file."""

    cfg = yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))
    df = pd.read_parquet(cfg["input"]["customer_features_path"])

    segmentation_cfg = cfg["segmentation"]
    pca_cfg = _build_pca_config(segmentation_cfg.get("pca", {}))

    eval_cfg = EvaluationConfig(
        features=segmentation_cfg["features"],
        pca=pca_cfg,
    )

    k_sweep = run_k_sweep(df, eval_cfg, k_values=segmentation_cfg["k_sweep"])
    seed_sweep = run_seed_sweep(
        df,
        eval_cfg,
        k=segmentation_cfg["chosen_k"],
        seeds=segmentation_cfg["seed_sweep"],
    )

    dbscan_cfg = _build_dbscan_config(segmentation_cfg.get("dbscan", {}))
    compare_df = compare_algorithms(
        df,
        eval_cfg,
        kmeans_k=segmentation_cfg["chosen_k"],
        dbscan_config=dbscan_cfg,
    )

    seg_cfg = SegmentationConfig(
        features=segmentation_cfg["features"],
        n_clusters=segmentation_cfg["chosen_k"],
        pca=pca_cfg,
    )
    assignments, _ = run_segmentation(df, seg_cfg, id_column="user_id")

    outdir = Path(cfg["output"]["outdir"])
    outdir.mkdir(parents=True, exist_ok=True)

    assignments.to_parquet(outdir / "segment_assignments.parquet", index=False)
    summary = (
        df.merge(assignments, on="user_id").groupby("segment").mean(numeric_only=True)
    )
    counts = assignments["segment"].value_counts().rename("n_users")
    summary = summary.join(counts)
    summary.to_parquet(outdir / "segment_summary.parquet")

    report = build_decision_report(
        chosen_k=segmentation_cfg["chosen_k"],
        silhouette_score=_extract_silhouette(k_sweep, segmentation_cfg["chosen_k"]),
        k_sweep=k_sweep,
        seed_sweep=seed_sweep,
        rationale=(
            "Chosen k based on silhouette + interpretability + persona stability."
        ),
        notes=[f"DBSCAN comparison: {compare_df.to_dict(orient='records')}"],
    )
    (outdir / "decision_report.md").write_text(
        decision_report_to_markdown(report),
        encoding="utf-8",
    )

    return outdir
