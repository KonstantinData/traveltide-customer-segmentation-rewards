from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pandas as pd
import yaml

from traveltide.eda.config import (
    CleaningConfig,
    CohortConfig,
    EDAConfig,
    ExtractionConfig,
    OutliersConfig,
    ReportConfig,
)
from traveltide.eda.dq_report import RuleImpact, render_dq_report_md
from traveltide.eda.preprocess import build_metadata, remove_outliers


def _make_config() -> EDAConfig:
    return EDAConfig(
        cohort=CohortConfig(
            sign_up_date_start="2022-01-01",
            sign_up_date_end="2022-12-31",
        ),
        extraction=ExtractionConfig(session_start_min=None),
        cleaning=CleaningConfig(invalid_hotel_nights_policy="recompute"),
        outliers=OutliersConfig(
            method="iqr",
            iqr_multiplier=1.5,
            zscore_threshold=5.0,
            columns=["page_clicks", "base_fare_usd"],
        ),
        report=ReportConfig(
            title="Test",
            output_format="html",
            include_sample_rows=5,
        ),
    )


def test_remove_outliers_returns_rule_impacts() -> None:
    df = pd.DataFrame(
        {
            "page_clicks": [1, 2, 3, 4, 100],
            "base_fare_usd": [10, 12, 11, 13, 12],
        }
    )
    config = _make_config()

    cleaned, rules = remove_outliers(df, config)

    assert len(cleaned) == 4
    assert set(rules.keys()) == {"page_clicks", "base_fare_usd"}
    clicks = rules["page_clicks"]
    assert clicks.rows_before == 5
    assert clicks.rows_after == 4
    assert clicks.rows_removed == 1
    fares = rules["base_fare_usd"]
    assert fares.rows_before == 4
    assert fares.rows_after == 4
    assert fares.rows_removed == 0


def test_build_metadata_renders_dq_report() -> None:
    config = _make_config()
    validity_rules = {
        "invalid_hotel_nights": RuleImpact(
            rows_before=100, rows_after=95, rows_removed=5
        )
    }
    outlier_rules = {
        "page_clicks": RuleImpact(rows_before=95, rows_after=90, rows_removed=5)
    }
    meta = build_metadata(
        config=config,
        row_counts={"sessions": 100},
        n_rows_raw=100,
        n_rows_after_validity=95,
        n_rows_clean=90,
        validity_rules=validity_rules,
        outlier_rules=outlier_rules,
        invalid_hotel_nights_meta={
            "policy": "recompute",
            "invalid_detected": 6,
            "recomputed_success": 4,
            "still_missing": 2,
        },
    )
    md = render_dq_report_md(meta)
    assert "Validity rules" in md
    assert "Outlier rules" in md
    assert "invalid_hotel_nights" in md
    assert "page_clicks" in md
    assert "Rows with invalid nights detected" in md
    assert "90" in md


def test_cli_dq_report_generates_markdown(tmp_path: Path) -> None:
    artifacts_base = tmp_path / "artifacts" / "eda"
    run_dir = artifacts_base / "20240101_000000Z"
    run_dir.mkdir(parents=True)
    meta = {
        "rows": {
            "session_level_raw": 10,
            "session_level_after_validity": 10,
            "session_level_clean": 9,
        },
        "validity_rules": {},
        "outliers": {},
    }
    (run_dir / "metadata.yaml").write_text(
        yaml.safe_dump(meta, sort_keys=False), encoding="utf-8"
    )

    out_path = tmp_path / "reports" / "dq_report.md"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "traveltide",
            "dq-report",
            "--artifacts-base",
            str(artifacts_base),
            "--out",
            str(out_path),
        ],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )

    assert result.returncode == 0
    assert out_path.exists()
    assert "# Data Quality Report" in out_path.read_text(encoding="utf-8")
