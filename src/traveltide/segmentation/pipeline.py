"""Segmentation pipeline (scaling + KMeans + optional PCA) (TT-020)."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


@dataclass(frozen=True)
class PCAConfig:
    """Optional PCA settings for dimensionality reduction."""

    n_components: int | float


@dataclass(frozen=True)
class SegmentationConfig:
    """Configuration for the segmentation pipeline."""

    features: list[str]
    n_clusters: int
    random_state: int | None = 42
    n_init: int = 10
    pca: PCAConfig | None = None


@dataclass(frozen=True)
class SegmentationArtifacts:
    """Artifacts emitted by the segmentation pipeline."""

    scaler: StandardScaler
    pca: PCA | None
    model: KMeans
    feature_columns: list[str]
    transformed_features: pd.DataFrame


def _validate_features(df: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    missing = [col for col in features if col not in df.columns]
    if missing:
        missing_display = ", ".join(missing)
        raise KeyError(f"Missing feature columns: {missing_display}")

    feature_df = df[features].apply(pd.to_numeric, errors="coerce")
    null_mask = feature_df.isna().any()
    if null_mask.any():
        bad_cols = ", ".join(feature_df.columns[null_mask].tolist())
        raise ValueError(f"Features contain missing values after coercion: {bad_cols}")

    return feature_df


def run_segmentation(
    df: pd.DataFrame,
    config: SegmentationConfig,
    *,
    id_column: str | None = "user_id",
) -> tuple[pd.DataFrame, SegmentationArtifacts]:
    """Run scaling + optional PCA + KMeans and return segment assignments."""

    feature_df = _validate_features(df, config.features)

    scaler = StandardScaler()
    scaled = scaler.fit_transform(feature_df)
    scaled_df = pd.DataFrame(
        scaled,
        columns=[f"scaled_{col}" for col in config.features],
        index=df.index,
    )

    pca_model: PCA | None = None
    transformed_df = scaled_df
    if config.pca is not None:
        pca_model = PCA(n_components=config.pca.n_components)
        transformed = pca_model.fit_transform(scaled_df)
        transformed_df = pd.DataFrame(
            transformed,
            columns=[f"pc_{idx + 1}" for idx in range(transformed.shape[1])],
            index=df.index,
        )

    kmeans = KMeans(
        n_clusters=config.n_clusters,
        random_state=config.random_state,
        n_init=config.n_init,
    )
    labels = kmeans.fit_predict(transformed_df)

    if id_column is None:
        assignments = pd.DataFrame({"segment": labels}, index=df.index)
    else:
        if id_column not in df.columns:
            raise KeyError(f"Missing id column: {id_column}")
        assignments = pd.DataFrame(
            {id_column: df[id_column].to_numpy(), "segment": labels},
            index=df.index,
        )

    artifacts = SegmentationArtifacts(
        scaler=scaler,
        pca=pca_model,
        model=kmeans,
        feature_columns=list(transformed_df.columns),
        transformed_features=transformed_df,
    )
    return assignments, artifacts
