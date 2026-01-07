"""Segmentation evaluation helpers (TT-021)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

from .pipeline import PCAConfig, _validate_features


@dataclass(frozen=True)
class EvaluationConfig:
    """Configuration for evaluating clustering outcomes."""

    features: list[str]
    random_state: int | None = 42
    n_init: int = 10
    pca: PCAConfig | None = None


@dataclass(frozen=True)
class DecisionReport:
    """Summary of the selected k and supporting evidence."""

    chosen_k: int
    silhouette_score: float | None
    k_sweep: pd.DataFrame
    rationale: str
    notes: list[str]


def _validate_evaluation_config(config: EvaluationConfig, n_features: int) -> None:
    if not config.features:
        raise ValueError("EvaluationConfig.features must include at least one column")

    if config.n_init < 1:
        raise ValueError("EvaluationConfig.n_init must be at least 1")

    if config.pca is None:
        return

    n_components = config.pca.n_components
    if isinstance(n_components, float):
        if not 0 < n_components <= 1:
            raise ValueError("PCA n_components as float must be in (0, 1]")
    else:
        if n_components < 1:
            raise ValueError("PCA n_components must be at least 1")
        if n_components > n_features:
            raise ValueError("PCA n_components cannot exceed feature count")


def _prepare_features(df: pd.DataFrame, config: EvaluationConfig) -> pd.DataFrame:
    feature_df = _validate_features(df, config.features)
    _validate_evaluation_config(config, n_features=feature_df.shape[1])

    scaler = StandardScaler()
    scaled = scaler.fit_transform(feature_df)
    scaled_df = pd.DataFrame(
        scaled,
        columns=[f"scaled_{col}" for col in config.features],
        index=df.index,
    )

    if config.pca is None:
        return scaled_df

    pca_model = PCA(n_components=config.pca.n_components)
    transformed = pca_model.fit_transform(scaled_df)
    return pd.DataFrame(
        transformed,
        columns=[f"pc_{idx + 1}" for idx in range(transformed.shape[1])],
        index=df.index,
    )


def compute_silhouette(features: pd.DataFrame, labels: Sequence[int]) -> float | None:
    """Compute a silhouette score, returning None when invalid."""

    if len(labels) < 2:
        return None

    if len(set(labels)) < 2:
        return None

    return float(silhouette_score(features, labels))


def run_k_sweep(
    df: pd.DataFrame,
    config: EvaluationConfig,
    *,
    k_values: Iterable[int],
) -> pd.DataFrame:
    """Evaluate multiple k values using inertia + silhouette."""

    k_list = list(k_values)
    if not k_list:
        raise ValueError("k_values must include at least one candidate")

    transformed_df = _prepare_features(df, config)
    n_samples = transformed_df.shape[0]

    results: list[dict[str, object]] = []
    for k in k_list:
        if k < 2:
            results.append(
                {
                    "k": k,
                    "inertia": None,
                    "silhouette": None,
                    "status": "invalid: k must be at least 2",
                }
            )
            continue

        if k >= n_samples:
            results.append(
                {
                    "k": k,
                    "inertia": None,
                    "silhouette": None,
                    "status": "invalid: k must be < n_samples",
                }
            )
            continue

        kmeans = KMeans(
            n_clusters=k,
            random_state=config.random_state,
            n_init=config.n_init,
        )
        labels = kmeans.fit_predict(transformed_df)
        silhouette = compute_silhouette(transformed_df, labels)
        status = "ok" if silhouette is not None else "invalid: single cluster"
        results.append(
            {
                "k": k,
                "inertia": float(kmeans.inertia_),
                "silhouette": silhouette,
                "status": status,
            }
        )

    return pd.DataFrame(results)


def build_decision_report(
    *,
    chosen_k: int,
    k_sweep: pd.DataFrame,
    silhouette_score: float | None,
    rationale: str,
    notes: list[str] | None = None,
) -> DecisionReport:
    """Build a decision report object for segmentation k selection."""

    if notes is None:
        notes = []

    return DecisionReport(
        chosen_k=chosen_k,
        silhouette_score=silhouette_score,
        k_sweep=k_sweep,
        rationale=rationale,
        notes=notes,
    )


def decision_report_to_markdown(report: DecisionReport) -> str:
    """Render a decision report as markdown for sharing."""

    def format_float(value: float | None) -> str:
        if value is None:
            return "n/a"
        return f"{value:.4f}"

    def format_cell(value: object) -> str:
        if isinstance(value, float):
            return format_float(value)
        if value is None:
            return "n/a"
        return str(value)

    headers = list(report.k_sweep.columns)
    header_row = "| " + " | ".join(headers) + " |"
    divider_row = "| " + " | ".join(["---"] * len(headers)) + " |"
    body_rows = [
        "| " + " | ".join(format_cell(value) for value in row) + " |"
        for row in report.k_sweep.itertuples(index=False, name=None)
    ]

    lines = [
        "# Segmentation k Decision Report",
        "",
        f"**Chosen k:** {report.chosen_k}",
        f"**Silhouette score:** {format_float(report.silhouette_score)}",
        "",
        "## Rationale",
        report.rationale,
        "",
    ]

    if report.notes:
        lines.append("## Notes")
        lines.extend([f"- {note}" for note in report.notes])
        lines.append("")

    lines.append("## k Sweep")
    lines.append(header_row)
    lines.append(divider_row)
    lines.extend(body_rows)
    lines.append("")

    return "\n".join(lines)
