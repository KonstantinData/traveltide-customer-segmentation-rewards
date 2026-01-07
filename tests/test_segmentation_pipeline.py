"""Segmentation pipeline tests (TT-020)."""

from __future__ import annotations

import pandas as pd

from traveltide.segmentation.pipeline import PCAConfig, SegmentationConfig, run_segmentation


def _sample_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "user_id": [101, 102, 103, 104],
            "avg_page_clicks": [10, 12, 50, 48],
            "avg_base_fare_usd": [120.0, 115.0, 380.0, 400.0],
        }
    )


def test_run_segmentation_scaling_kmeans() -> None:
    df = _sample_data()
    config = SegmentationConfig(
        features=["avg_page_clicks", "avg_base_fare_usd"],
        n_clusters=2,
        random_state=7,
    )

    assignments, artifacts = run_segmentation(df, config)

    assert assignments["user_id"].tolist() == [101, 102, 103, 104]
    assert assignments["segment"].between(0, 1).all()
    assert artifacts.pca is None
    assert artifacts.transformed_features.shape == (4, 2)


def test_run_segmentation_with_pca() -> None:
    df = _sample_data()
    config = SegmentationConfig(
        features=["avg_page_clicks", "avg_base_fare_usd"],
        n_clusters=2,
        random_state=7,
        pca=PCAConfig(n_components=1),
    )

    assignments, artifacts = run_segmentation(df, config)

    assert assignments["segment"].between(0, 1).all()
    assert artifacts.pca is not None
    assert artifacts.transformed_features.shape == (4, 1)
