"""End-to-end pipeline orchestration for TravelTide runs."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from traveltide.eda import run_eda
from traveltide.features.pipeline import run_features
from traveltide.perks.mapping import write_customer_perks
from traveltide.segmentation.run import run_segmentation_job


def _timestamp_slug() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def _build_run_dir(base_dir: Path, run_id: str | None) -> Path:
    base_dir.mkdir(parents=True, exist_ok=True)

    if run_id:
        candidate = base_dir / run_id
    else:
        candidate = base_dir / _timestamp_slug()

    if not candidate.exists():
        candidate.mkdir(parents=True, exist_ok=False)
        return candidate

    suffix = _timestamp_slug()
    fallback = base_dir / f"{candidate.name}-{suffix}"
    fallback.mkdir(parents=True, exist_ok=False)
    return fallback


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _ensure_latest_link(base_dir: Path, run_dir: Path) -> None:
    latest_dir = base_dir / "latest"
    if latest_dir.exists() or latest_dir.is_symlink():
        if latest_dir.is_symlink():
            latest_dir.unlink()
        else:
            shutil.rmtree(latest_dir)
    try:
        latest_dir.symlink_to(run_dir.resolve(), target_is_directory=True)
    except OSError:
        shutil.copytree(run_dir, latest_dir)


def _prepare_sample_eda(step1_dir: Path) -> Path:
    sample_source = (
        _repo_root()
        / "artifacts"
        / "example_run"
        / "eda"
        / "20240101_000000Z"
    )
    if not sample_source.exists():
        raise FileNotFoundError(
            f"Sample EDA source not found at {sample_source}. "
            "Run the full pipeline or update artifacts/example_run."
        )
    run_dir = step1_dir / sample_source.name
    if run_dir.exists():
        shutil.rmtree(run_dir)
    shutil.copytree(sample_source, run_dir)

    data_dir = run_dir / "data"
    sessions_csv = data_dir / "sessions_clean_sample.csv"
    users_csv = data_dir / "users_agg_sample.csv"
    if sessions_csv.exists():
        sessions_df = pd.read_csv(sessions_csv)
        sessions_df.to_parquet(data_dir / "sessions_clean.parquet", index=False)
    if users_csv.exists():
        users_df = pd.read_csv(users_csv)
        users_df.to_parquet(data_dir / "users_agg.parquet", index=False)

    _ensure_latest_link(step1_dir, run_dir)
    return run_dir


def _copy_report(report_path: Path, reports_dir: Path, target_name: str) -> None:
    if report_path.exists():
        reports_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(report_path, reports_dir / target_name)


def run_end_to_end(
    *,
    mode: str,
    seed: int | None,
    run_id: str | None,
    outdir: str,
    eda_config: str,
    features_config: str,
    segmentation_config: str,
    perks_config: str,
) -> Path:
    """Execute the end-to-end pipeline and capture metadata for a run."""

    run_dir = _build_run_dir(Path(outdir), run_id)
    step1_dir = run_dir / "step1_eda"
    step2_dir = run_dir / "step2_feature_engineering"
    step3_dir = run_dir / "step3_segmentation"
    step4_dir = run_dir / "step4_perks"
    reports_dir = _repo_root() / "reports"
    mart_dir = _repo_root() / "data" / "mart"

    if mode == "sample":
        step1_dir.mkdir(parents=True, exist_ok=True)
        eda_run_dir = _prepare_sample_eda(step1_dir)
    else:
        step1_dir.mkdir(parents=True, exist_ok=True)
        eda_run_dir = run_eda(config_path=eda_config, outdir=str(step1_dir))

    features_cfg = yaml.safe_load(Path(features_config).read_text(encoding="utf-8"))
    sessions_clean_path = eda_run_dir / "data" / "sessions_clean.parquet"
    if not sessions_clean_path.exists():
        sessions_clean_path = step1_dir / "latest" / "data" / "sessions_clean.parquet"
    features_cfg["input"]["sessions_clean_path"] = str(sessions_clean_path)
    step2_data_dir = step2_dir / "data"
    step2_data_dir.mkdir(parents=True, exist_ok=True)
    features_cfg["output"]["customer_features_path"] = str(
        step2_data_dir / "customer_features.parquet"
    )
    features_cfg_path = step2_dir / "config" / "features.yaml"
    features_cfg_path.parent.mkdir(parents=True, exist_ok=True)
    features_cfg_path.write_text(
        yaml.safe_dump(features_cfg, sort_keys=False), encoding="utf-8"
    )
    features_path = run_features(config_path=str(features_cfg_path))

    segmentation_cfg = yaml.safe_load(
        Path(segmentation_config).read_text(encoding="utf-8")
    )
    segmentation_cfg["input"]["customer_features_path"] = str(features_path)
    segmentation_cfg["output"]["outdir"] = str(step3_dir)
    segmentation_cfg_path = step3_dir / "config" / "segmentation.yaml"
    segmentation_cfg_path.parent.mkdir(parents=True, exist_ok=True)
    segmentation_cfg_path.write_text(
        yaml.safe_dump(segmentation_cfg, sort_keys=False), encoding="utf-8"
    )
    segmentation_outdir = run_segmentation_job(config_path=str(segmentation_cfg_path))

    step4_dir.mkdir(parents=True, exist_ok=True)
    perks_path = write_customer_perks(
        assignments_path=str(segmentation_outdir / "segment_assignments.parquet"),
        config_path=perks_config,
        out_path=str(step4_dir / "customer_perks.csv"),
    )

    mart_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(perks_path, mart_dir / "customer_perk_assignments.csv")

    eda_report_path = eda_run_dir / "reports" / "eda_report.html"
    if not eda_report_path.exists():
        eda_report_path = eda_run_dir / "eda_report.html"
    _copy_report(eda_report_path, reports_dir, "eda_report.html")
    _copy_report(
        segmentation_outdir / "decision_report.md",
        reports_dir,
        "segmentation_decision_report.md",
    )

    metadata: dict[str, Any] = {
        "mode": mode,
        "seed": seed,
        "run_id": run_id,
        "configs": {
            "eda": eda_config,
            "features": features_config,
            "segmentation": segmentation_config,
            "perks": perks_config,
        },
        "outputs": {
            "run_dir": str(run_dir),
            "eda_run_dir": str(eda_run_dir),
            "customer_features": str(features_path),
            "segmentation_dir": str(segmentation_outdir),
            "perks_csv": str(perks_path),
            "mart_perks_csv": str(mart_dir / "customer_perk_assignments.csv"),
            "reports_dir": str(reports_dir),
        },
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    metadata_path = run_dir / "run_metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return run_dir
