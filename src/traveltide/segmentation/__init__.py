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
    run_seed_sweep,
)
from .pipeline import (
    PCAConfig,
    SegmentationArtifacts,
    SegmentationConfig,
    run_segmentation,
)
from .visuals import plot_k_sweep, plot_seed_sweep, write_k_robust_visuals

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
    "plot_k_sweep",
    "plot_seed_sweep",
    "run_k_sweep",
    "run_seed_sweep",
    "run_segmentation",
    "write_k_robust_visuals",
]
