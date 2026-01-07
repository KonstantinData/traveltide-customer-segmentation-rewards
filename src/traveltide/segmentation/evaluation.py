"""Segmentation evaluation helpers (TT-021)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, silhouette_score
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
class DBSCANConfig:
    """Configuration for DBSCAN comparison runs."""

    eps: float = 0.5
    min_samples: int = 5
    metric: str = "euclidean"


@dataclass(frozen=True)
class DecisionReport:
    """Summary of the selected k and supporting evidence."""

    chosen_k: int
    silhouette_score: float | None
    k_sweep: pd.DataFrame
    seed_sweep: pd.DataFrame | None
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


def _summarize_labels(labels: Sequence[int]) -> tuple[int, float]:
    label_set = set(labels)
    n_clusters = len(label_set) - (1 if -1 in label_set else 0)
    n_samples = len(labels)
    noise_count = sum(label == -1 for label in labels)
    noise_pct = noise_count / n_samples if n_samples else 0.0
    return n_clusters, noise_pct


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


def run_seed_sweep(
    df: pd.DataFrame,
    config: EvaluationConfig,
    *,
    k: int,
    seeds: Iterable[int],
) -> pd.DataFrame:
    """Evaluate KMeans stability across random seeds."""

    seed_list = list(seeds)
    if not seed_list:
        raise ValueError("seeds must include at least one value")

    if k < 2:
        raise ValueError("k must be at least 2")

    transformed_df = _prepare_features(df, config)
    n_samples = transformed_df.shape[0]
    if k >= n_samples:
        raise ValueError("k must be < n_samples")

    results: list[dict[str, object]] = []
    reference_labels: Sequence[int] | None = None
    for seed in seed_list:
        kmeans = KMeans(
            n_clusters=k,
            random_state=seed,
            n_init=config.n_init,
        )
        labels = kmeans.fit_predict(transformed_df)
        silhouette = compute_silhouette(transformed_df, labels)
        if reference_labels is None:
            reference_labels = labels
            ari = 1.0
        else:
            ari = float(adjusted_rand_score(reference_labels, labels))
        results.append(
            {
                "seed": seed,
                "inertia": float(kmeans.inertia_),
                "silhouette": silhouette,
                "ari_to_reference": ari,
            }
        )

    return pd.DataFrame(results)


def compare_algorithms(
    df: pd.DataFrame,
    config: EvaluationConfig,
    *,
    kmeans_k: int,
    dbscan_config: DBSCANConfig | None = None,
) -> pd.DataFrame:
    """Compare KMeans and DBSCAN outcomes on the same feature set."""

    if kmeans_k < 2:
        raise ValueError("kmeans_k must be at least 2")

    transformed_df = _prepare_features(df, config)
    results: list[dict[str, object]] = []

    kmeans = KMeans(
        n_clusters=kmeans_k,
        random_state=config.random_state,
        n_init=config.n_init,
    )
    kmeans_labels = kmeans.fit_predict(transformed_df)
    kmeans_clusters, _ = _summarize_labels(kmeans_labels)
    results.append(
        {
            "algorithm": "kmeans",
            "n_clusters": kmeans_clusters,
            "noise_pct": 0.0,
            "silhouette": compute_silhouette(transformed_df, kmeans_labels),
            "inertia": float(kmeans.inertia_),
        }
    )

    dbscan_settings = dbscan_config or DBSCANConfig()
    dbscan = DBSCAN(
        eps=dbscan_settings.eps,
        min_samples=dbscan_settings.min_samples,
        metric=dbscan_settings.metric,
    )
    dbscan_labels = dbscan.fit_predict(transformed_df)
    dbscan_clusters, dbscan_noise_pct = _summarize_labels(dbscan_labels)
    silhouette = None
    if dbscan_clusters >= 2:
        non_noise_mask = dbscan_labels != -1
        if non_noise_mask.sum() >= 2:
            silhouette = compute_silhouette(
                transformed_df.loc[non_noise_mask], dbscan_labels[non_noise_mask]
            )
    results.append(
        {
            "algorithm": "dbscan",
            "n_clusters": dbscan_clusters,
            "noise_pct": dbscan_noise_pct,
            "silhouette": silhouette,
            "inertia": None,
        }
    )

    return pd.DataFrame(results)


def build_decision_report(
    *,
    chosen_k: int,
    k_sweep: pd.DataFrame,
    silhouette_score: float | None,
    seed_sweep: pd.DataFrame | None = None,
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
        seed_sweep=seed_sweep,
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

    k_headers = list(report.k_sweep.columns)
    k_header_row = "| " + " | ".join(k_headers) + " |"
    k_divider_row = "| " + " | ".join(["---"] * len(k_headers)) + " |"
    k_body_rows = [
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

    if report.seed_sweep is not None:
        seed_headers = list(report.seed_sweep.columns)
        seed_header_row = "| " + " | ".join(seed_headers) + " |"
        seed_divider_row = "| " + " | ".join(["---"] * len(seed_headers)) + " |"
        seed_body_rows = [
            "| " + " | ".join(format_cell(value) for value in row) + " |"
            for row in report.seed_sweep.itertuples(index=False, name=None)
        ]

        lines.append("## Stability (Seed Sweep)")
        lines.append("Reference seed is the first row in the table.")
        lines.append("")
        lines.append(seed_header_row)
        lines.append(seed_divider_row)
        lines.extend(seed_body_rows)
        lines.append("")

    lines.append("## k Sweep")
    lines.append(k_header_row)
    lines.append(k_divider_row)
    lines.extend(k_body_rows)
    lines.append("")

    return "\n".join(lines)
