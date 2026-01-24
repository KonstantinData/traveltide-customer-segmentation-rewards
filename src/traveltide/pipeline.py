"""End-to-end pipeline orchestration for TravelTide runs."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

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


def run_end_to_end(
    *,
    mode: str,
    seed: int | None,
    run_id: str | None,
    eda_config: str,
    features_config: str,
    segmentation_config: str,
    perks_config: str,
) -> Path:
    """Execute the full end-to-end pipeline and return the run directory."""

    run_dir = _build_run_dir(Path("artifacts") / "runs", run_id)

    # Create metadata
    metadata: dict[str, Any] = {
        "mode": mode,
        "seed": seed,
        "run_id": run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "configs": {
            "eda": eda_config,
            "features": features_config,
            "segmentation": segmentation_config,
            "perks": perks_config,
        },
    }

    # Step 1: EDA
    print("Running EDA pipeline...")
    eda_outdir = run_eda(config_path=eda_config, outdir=str(run_dir / "eda"))
    metadata["eda_output"] = str(eda_outdir)

    # Step 2: Features
    print("Running feature engineering...")
    features_outdir = run_features(
        config_path=features_config, outdir=str(run_dir / "features")
    )
    metadata["features_output"] = str(features_outdir)

    # Create a temporary segmentation config that points to the correct features file
    import tempfile

    import yaml

    with open(segmentation_config, "r") as f:
        seg_config = yaml.safe_load(f)

    # Update the input path to point to the features file we just created
    seg_config["input"]["customer_features_path"] = str(features_outdir)

    # Write temporary config
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(seg_config, f)
        temp_seg_config = f.name

    try:
        # Step 3: Segmentation
        print("Running segmentation...")
        segmentation_outdir = run_segmentation_job(config_path=temp_seg_config)
        metadata["segmentation_output"] = str(segmentation_outdir)

        # Step 4: Perks
        print("Running perks mapping...")
        perks_output = write_customer_perks(
            assignments_path=str(segmentation_outdir / "segment_assignments.parquet"),
            config_path=perks_config,
            out_path=str(run_dir / "perks" / "customer_perks.csv"),
        )
        metadata["perks_output"] = str(perks_output)

    finally:
        # Clean up temporary config
        import os

        os.unlink(temp_seg_config)

    # Copy key outputs to standard locations
    print("Copying outputs to standard locations...")

    # Create mart directory
    mart_dir = Path("data") / "mart"
    mart_dir.mkdir(parents=True, exist_ok=True)

    # Copy customer perk assignments to mart
    if perks_output.exists():
        import shutil

        shutil.copy2(perks_output, mart_dir / "customer_perk_assignments.csv")

    # Save metadata
    metadata_path = run_dir / "run_metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    return run_dir
