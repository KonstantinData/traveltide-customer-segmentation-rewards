# Description: Typed EDA configuration model and loader.
"""EDA configuration loader and typed config model (TT-012).

Notes:
- This module defines a strict, version-controlled configuration contract for Step 1 (EDA).
- The YAML config is treated as the single source of truth for cohort selection, cleaning policies,
  outlier rules, and report rendering parameters.
- Strong typing + explicit required keys make EDA runs reproducible and prevent silent config drift
  across machines, CI, and future project steps.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


# Notes: Cohort rules used to scope the EDA dataset.
@dataclass(frozen=True)
class CohortConfig:
    """Cohort selection rules.

    Notes:
    - Cohorts control tenure effects (customers need comparable time on platform).
    - Defaults follow the course guidance: users signed up during calendar year 2022.
    """

    sign_up_date_start: str
    sign_up_date_end: str


# Notes: Extraction settings for the session-level dataset.
@dataclass(frozen=True)
class ExtractionConfig:
    """Data extraction controls.

    Notes:
    - Allows limiting extraction for runtime control without changing query logic elsewhere.
    - All extraction constraints must remain centrally defined here to keep runs comparable.
    """

    session_start_min: str | None
    min_sessions: int | None
    min_page_clicks: int | None


# Notes: Cleaning policies for known data anomalies.
@dataclass(frozen=True)
class CleaningConfig:
    """Cleaning policies for known anomalies.

    Notes:
    - Encodes explicit decisions on how to handle data issues (e.g., invalid hotel nights).
    - Keeping policies in config ensures the same behavior in local runs and CI.
    """

    invalid_hotel_nights_policy: str


# Notes: Outlier detection parameters for EDA filtering.
@dataclass(frozen=True)
class OutliersConfig:
    """Outlier detection/removal settings.

    Notes:
    - Outlier removal is applied prior to aggregation to avoid distorted averages.
    - This configuration does not attempt to be "perfect"; it is meant to be explicit and auditable.
    """

    method: str
    iqr_multiplier: float
    zscore_threshold: float
    columns: list[str]


# Notes: Report rendering configuration for EDA outputs.
@dataclass(frozen=True)
class ReportConfig:
    """Report rendering settings.

    Notes:
    - Report settings belong in config so artifacts can be regenerated identically later.
    - PDF support can be added later; the config contract remains stable.
    """

    title: str
    output_format: str
    include_sample_rows: int


# Notes: Top-level container for all EDA configuration sections.
@dataclass(frozen=True)
class EDAConfig:
    """Top-level EDA configuration object.

    Notes:
    - This is the single object passed into extraction/preprocessing/reporting stages.
    - It is intentionally rigid: changes to config structure should be treated as breaking changes.
    """

    cohort: CohortConfig
    extraction: ExtractionConfig
    cleaning: CleaningConfig
    outliers: OutliersConfig
    report: ReportConfig


# Notes: Require config keys and fail fast on missing values.
def _get(d: dict[str, Any], key: str) -> Any:
    # Notes: Central helper to enforce required keys and fail fast with a clear error message.
    if key not in d:
        raise KeyError(f"Missing required config key: {key}")
    return d[key]


# Notes: Read, validate, and normalize EDA configuration.
def load_config(path: str | Path) -> EDAConfig:
    """Load EDA configuration from YAML.

    Notes:
    - Enforces YAML structure and required keys to avoid silent defaults.
    - Normalizes selected string values to lowercase for predictable comparisons.
    """

    # Notes: Always read YAML as UTF-8 and validate it is a mapping at the top level.
    p = Path(path)
    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError("EDA config must be a YAML mapping")

    # Notes: Extract nested sections explicitly; missing keys raise immediately via _get().
    cohort = _get(data, "cohort")
    extraction = _get(data, "extraction")
    cleaning = _get(data, "cleaning")
    outliers = _get(data, "outliers")
    report = _get(data, "report")

    # Notes: Build the typed config. Conversions are explicit to avoid type ambiguity downstream.
    return EDAConfig(
        cohort=CohortConfig(
            sign_up_date_start=str(_get(cohort, "sign_up_date_start")),
            sign_up_date_end=str(_get(cohort, "sign_up_date_end")),
        ),
        extraction=ExtractionConfig(
            # Notes: Optional constraint; can be null in YAML to disable session_start filtering.
            session_start_min=extraction.get("session_start_min"),
            min_sessions=(
                int(extraction.get("min_sessions"))
                if extraction.get("min_sessions") is not None
                else None
            ),
            min_page_clicks=(
                int(extraction.get("min_page_clicks"))
                if extraction.get("min_page_clicks") is not None
                else None
            ),
        ),
        cleaning=CleaningConfig(
            # Notes: Normalized to lowercase to ensure comparisons are stable across YAML styles.
            invalid_hotel_nights_policy=str(
                _get(cleaning, "invalid_hotel_nights_policy")
            ).lower(),
        ),
        outliers=OutliersConfig(
            # Notes: Normalize method to lowercase; thresholds are numeric and explicitly cast.
            method=str(_get(outliers, "method")).lower(),
            iqr_multiplier=float(_get(outliers, "iqr_multiplier")),
            zscore_threshold=float(_get(outliers, "zscore_threshold")),
            columns=[str(c) for c in _get(outliers, "columns")],
        ),
        report=ReportConfig(
            # Notes: Output format normalized to lowercase for stable branching in rendering logic.
            title=str(_get(report, "title")),
            output_format=str(_get(report, "output_format")).lower(),
            include_sample_rows=int(_get(report, "include_sample_rows")),
        ),
    )
