from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

from traveltide.segmentation.run import run_segmentation_job


def test_run_segmentation_job_outputs(tmp_path: Path):
    df = pd.DataFrame(
        {
            "user_id": [1, 2, 3, 4, 5, 6],
            "feature_a": [0.1, 0.2, 0.15, 1.0, 1.1, 0.9],
            "feature_b": [10, 11, 9, 30, 29, 31],
        }
    )
    features_path = tmp_path / "customer_features.parquet"
    df.to_parquet(features_path, index=False)

    config = {
        "input": {"customer_features_path": str(features_path)},
        "segmentation": {
            "features": ["feature_a", "feature_b"],
            "k_sweep": [2],
            "seed_sweep": [1],
            "chosen_k": 2,
            "pca": {"enabled": False},
            "dbscan": {"enabled": False},
        },
        "output": {"outdir": str(tmp_path / "out")},
    }
    config_path = tmp_path / "segmentation.yaml"
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")

    outdir = run_segmentation_job(str(config_path))

    assignments_path = outdir / "segment_assignments.parquet"
    summary_path = outdir / "segment_summary.parquet"

    assert assignments_path.is_file()
    assert summary_path.is_file()

    assignments = pd.read_parquet(assignments_path)
    assert {"user_id", "segment"}.issubset(assignments.columns)
