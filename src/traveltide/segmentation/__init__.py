"""Segmentation utilities for TravelTide (Step 3)."""

from __future__ import annotations

from .evaluation import (
    DBSCANConfig,
    DecisionReport,
    EvaluationConfig,
    build_decision_report,
    compare_algorithms,
    compute_silhouette,
    decision_report_to_markdown,
    run_k_sweep,
)
from .pipeline import (
    PCAConfig,
    SegmentationArtifacts,
    SegmentationConfig,
    run_segmentation,
)

__all__ = [
    "DecisionReport",
    "DBSCANConfig",
    "EvaluationConfig",
    "PCAConfig",
    "SegmentationArtifacts",
    "SegmentationConfig",
    "build_decision_report",
    "compare_algorithms",
    "compute_silhouette",
    "decision_report_to_markdown",
    "run_k_sweep",
    "run_segmentation",
]
