# Description: Exploratory clustering experiments for EDA reporting.
"""Exploratory clustering experiments for EDA reporting.

Notes:
- This module is exploratory only and must never influence production segmentation.
- It evaluates lightweight K-Means and DBSCAN trials with simple metrics.
- Results are persisted under the EDA run's exploratory artifacts directory.
"""

from __future__ import annotations

import base64
import io
import json
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


def _fig_to_base64() -> str:
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")


def _candidate_numeric_columns(df: pd.DataFrame) -> list[str]:
    numeric_cols = df.select_dtypes(include="number").columns
    candidates: list[str] = []
    for col in numeric_cols:
        lowered = col.lower()
        if lowered == "id" or lowered.endswith("_id") or lowered.startswith("id_"):
            continue
        candidates.append(col)
    return candidates


def _select_features(
    df: pd.DataFrame,
    *,
    max_missing_pct: float,
    min_unique: int,
) -> tuple[list[str], dict[str, Any]]:
    candidates = _candidate_numeric_columns(df)
    if not candidates:
        return [], {
            "max_missing_pct": max_missing_pct,
            "min_unique": min_unique,
            "excluded_id_like": True,
        }

    total = len(df)
    selected: list[str] = []
    for col in candidates:
        series = pd.to_numeric(df[col], errors="coerce")
        missing_pct = float(series.isna().mean()) if total else 1.0
        unique_count = int(series.nunique(dropna=True))
        if missing_pct > max_missing_pct:
            continue
        if unique_count < min_unique:
            continue
        selected.append(col)

    criteria = {
        "max_missing_pct": max_missing_pct,
        "min_unique": min_unique,
        "excluded_id_like": True,
        "candidate_numeric": candidates,
        "imputation": "median",
        "scaling": "standard",
    }
    return selected, criteria


def _prepare_matrix(
    df: pd.DataFrame, features: list[str]
) -> tuple[np.ndarray, pd.DataFrame]:
    subset = df[features].copy()
    for col in features:
        series = pd.to_numeric(subset[col], errors="coerce")
        median = series.median()
        subset[col] = series.fillna(median)
    scaled = StandardScaler().fit_transform(subset.values)
    return scaled, subset


def _kmeans_trials(
    matrix: np.ndarray,
    *,
    ks: list[int],
    random_state: int,
) -> list[dict[str, Any]]:
    metrics: list[dict[str, Any]] = []
    for k in ks:
        if matrix.shape[0] <= k:
            continue
        model = KMeans(n_clusters=k, n_init="auto", random_state=random_state)
        labels = model.fit_predict(matrix)
        label_count = int(len(set(labels)))
        silhouette = None
        if label_count > 1:
            silhouette = float(silhouette_score(matrix, labels))
        cluster_sizes = pd.Series(labels).value_counts().to_dict()
        metrics.append(
            {
                "k": k,
                "inertia": float(model.inertia_),
                "silhouette": silhouette,
                "label_count": label_count,
                "cluster_sizes": cluster_sizes,
            }
        )
    return metrics


def _dbscan_trials(
    matrix: np.ndarray,
    *,
    eps_values: list[float],
    min_samples_values: list[int],
) -> list[dict[str, Any]]:
    metrics: list[dict[str, Any]] = []
    for eps in eps_values:
        for min_samples in min_samples_values:
            model = DBSCAN(eps=eps, min_samples=min_samples)
            labels = model.fit_predict(matrix)
            unique_labels = set(labels)
            n_clusters = len([label for label in unique_labels if label != -1])
            noise_ratio = float(np.mean(labels == -1)) if labels.size else 0.0
            cluster_sizes = (
                pd.Series(labels[labels != -1]).value_counts().to_dict()
                if labels.size
                else {}
            )
            metrics.append(
                {
                    "eps": eps,
                    "min_samples": min_samples,
                    "n_clusters": n_clusters,
                    "noise_ratio": noise_ratio,
                    "cluster_sizes": cluster_sizes,
                }
            )
    return metrics


def _select_kmeans(metrics: list[dict[str, Any]]) -> dict[str, Any] | None:
    valid = [m for m in metrics if m.get("silhouette") is not None]
    if not valid:
        return None
    return max(valid, key=lambda m: m["silhouette"])


def _select_dbscan(metrics: list[dict[str, Any]]) -> dict[str, Any] | None:
    valid = [m for m in metrics if m.get("n_clusters", 0) > 1]
    if not valid:
        return None
    return max(valid, key=lambda m: (m["n_clusters"], -m["noise_ratio"]))


def _plot_clusters(
    matrix: np.ndarray,
    labels: np.ndarray,
    *,
    title: str,
    out_path: Path,
    relative_to: Path,
) -> dict[str, str]:
    pca = PCA(n_components=2, random_state=42)
    coords = pca.fit_transform(matrix)
    plt.figure()
    unique_labels = np.unique(labels)
    for label in unique_labels:
        mask = labels == label
        color = "#999999" if label == -1 else None
        plt.scatter(
            coords[mask, 0],
            coords[mask, 1],
            s=18,
            alpha=0.75,
            label=f"cluster {label}" if label != -1 else "noise",
            c=color,
        )
    plt.title(title)
    plt.xlabel("PCA 1")
    plt.ylabel("PCA 2")
    plt.legend(loc="best", fontsize=8)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, format="png", bbox_inches="tight", dpi=150)
    base64_img = _fig_to_base64()
    return {
        "path": str(out_path.relative_to(relative_to)),
        "base64": base64_img,
    }


def run_clustering_exploration(
    *,
    session_df: pd.DataFrame,
    user_df: pd.DataFrame,
    out_dir: Path,
    max_rows: int = 5000,
) -> dict[str, Any]:
    """Run exploratory clustering experiments and persist outputs."""

    exploratory_dir = out_dir / "exploratory" / "clustering"
    exploratory_dir.mkdir(parents=True, exist_ok=True)

    selected_source = "users_agg"
    features, criteria = _select_features(user_df, max_missing_pct=0.25, min_unique=3)
    data_df = user_df
    if len(features) < 2:
        selected_source = "sessions_clean"
        features, criteria = _select_features(
            session_df, max_missing_pct=0.25, min_unique=3
        )
        data_df = session_df

    if len(features) < 2 or data_df.empty:
        summary = {
            "notes": "Exploratory clustering only; hypotheses, not production results.",
            "status": "skipped",
            "reason": "Insufficient numeric features for clustering.",
            "source_table": selected_source,
            "feature_criteria": criteria,
            "feature_columns": features,
        }
        output_path = exploratory_dir / "clustering_summary.json"
        output_path.write_text(
            json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return {
            "metadata": {
                **summary,
                "artifact_path": str(output_path.relative_to(out_dir)),
            },
            "report": {
                **summary,
                "artifact_path": str(output_path.relative_to(out_dir)),
            },
        }

    working_df = data_df[features].copy()
    sampled = False
    if len(working_df) > max_rows:
        working_df = working_df.sample(n=max_rows, random_state=42)
        sampled = True

    matrix, _ = _prepare_matrix(working_df, features)

    kmeans_metrics = _kmeans_trials(matrix, ks=[3, 4, 5], random_state=42)
    kmeans_selected = _select_kmeans(kmeans_metrics)
    kmeans_plot = None
    kmeans_labels = None
    if kmeans_selected:
        model = KMeans(n_clusters=kmeans_selected["k"], n_init="auto", random_state=42)
        kmeans_labels = model.fit_predict(matrix)
        kmeans_plot = _plot_clusters(
            matrix,
            kmeans_labels,
            title=f"K-Means PCA (k={kmeans_selected['k']})",
            out_path=exploratory_dir / "kmeans_pca.png",
            relative_to=out_dir,
        )

    dbscan_metrics = _dbscan_trials(
        matrix,
        eps_values=[0.5, 1.0, 1.5],
        min_samples_values=[5, 10],
    )
    dbscan_selected = _select_dbscan(dbscan_metrics)
    dbscan_plot = None
    dbscan_labels = None
    if dbscan_selected:
        model = DBSCAN(
            eps=dbscan_selected["eps"],
            min_samples=dbscan_selected["min_samples"],
        )
        dbscan_labels = model.fit_predict(matrix)
        dbscan_plot = _plot_clusters(
            matrix,
            dbscan_labels,
            title=(
                "DBSCAN PCA "
                f"(eps={dbscan_selected['eps']}, min_samples={dbscan_selected['min_samples']})"
            ),
            out_path=exploratory_dir / "dbscan_pca.png",
            relative_to=out_dir,
        )

    kmeans_metrics_df = pd.DataFrame(kmeans_metrics)
    dbscan_metrics_df = pd.DataFrame(dbscan_metrics)
    kmeans_csv = exploratory_dir / "kmeans_metrics.csv"
    dbscan_csv = exploratory_dir / "dbscan_metrics.csv"
    kmeans_metrics_df.to_csv(kmeans_csv, index=False)
    dbscan_metrics_df.to_csv(dbscan_csv, index=False)

    summary = {
        "notes": "Exploratory clustering only; hypotheses, not production results.",
        "status": "completed",
        "source_table": selected_source,
        "feature_criteria": criteria,
        "feature_columns": features,
        "n_rows": int(len(working_df)),
        "n_features": int(len(features)),
        "sampled": sampled,
        "max_rows": max_rows,
        "kmeans": {
            "metrics": kmeans_metrics,
            "selected": kmeans_selected,
        },
        "dbscan": {
            "metrics": dbscan_metrics,
            "selected": dbscan_selected,
        },
        "artifacts": {
            "kmeans_metrics_csv": str(kmeans_csv.relative_to(out_dir)),
            "dbscan_metrics_csv": str(dbscan_csv.relative_to(out_dir)),
        },
    }
    output_path = exploratory_dir / "clustering_summary.json"
    output_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    report_payload = {
        **summary,
        "artifact_path": str(output_path.relative_to(out_dir)),
        "plots": {
            "kmeans": kmeans_plot,
            "dbscan": dbscan_plot,
        },
    }

    return {
        "metadata": {**summary, "artifact_path": str(output_path.relative_to(out_dir))},
        "report": report_payload,
    }
