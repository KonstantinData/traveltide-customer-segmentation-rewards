"""EDA config smoke tests (TT-012).

Notes:
- These tests intentionally avoid database access to keep CI fast and deterministic.
- The purpose is to prevent accidental YAML breakage or config contract drift.
"""

from __future__ import annotations

from pathlib import Path

from traveltide.eda.config import load_config


def test_eda_config_loads() -> None:
    # Notes: Ensures the repo-shipped YAML remains valid and maps to the typed config model.
    cfg = load_config(Path("config") / "eda.yaml")
    assert cfg.cohort.sign_up_date_start
    assert cfg.cohort.sign_up_date_end

    # Notes: Keep the first implementation stable: only HTML is supported for now.
    assert cfg.report.output_format == "html"
