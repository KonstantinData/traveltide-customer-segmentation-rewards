"""Segmentation evaluation tests (TT-021)."""

from __future__ import annotations

import pandas as pd

from traveltide.segmentation.evaluation import (
    DBSCANConfig,
    EvaluationConfig,
    build_decision_report,
    compare_algorithms,
    compute_silhouette,
    decision_report_to_markdown,
    run_k_sweep,
    run_seed_sweep,
)


def _sample_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "user_id": [101, 102, 103, 104, 105],
            "avg_page_clicks": [10, 12, 50, 48, 47],
            "avg_base_fare_usd": [120.0, 115.0, 380.0, 400.0, 395.0],
        }
    )


def test_compute_silhouette_handles_single_cluster() -> None:
    features = pd.DataFrame({"f1": [0.0, 1.0], "f2": [1.0, 2.0]})
    score = compute_silhouette(features, [0, 0])

    assert score is None


def test_run_k_sweep_returns_metrics() -> None:
    df = _sample_data()
    config = EvaluationConfig(
        features=["avg_page_clicks", "avg_base_fare_usd"],
        random_state=7,
    )

    results = run_k_sweep(df, config, k_values=[1, 2, 3])

    assert results["k"].tolist() == [1, 2, 3]
    assert results.loc[0, "status"].startswith("invalid")
    assert results.loc[1, "silhouette"] is not None
    assert results.loc[2, "inertia"] is not None


def test_compare_algorithms_returns_rows() -> None:
    df = _sample_data()
    config = EvaluationConfig(
        features=["avg_page_clicks", "avg_base_fare_usd"],
        random_state=7,
    )

    comparison = compare_algorithms(
        df,
        config,
        kmeans_k=2,
        dbscan_config=DBSCANConfig(eps=1.2, min_samples=2),
    )

    assert comparison["algorithm"].tolist() == ["kmeans", "dbscan"]
    assert comparison.loc[0, "inertia"] is not None
    assert 0.0 <= comparison.loc[1, "noise_pct"] <= 1.0


def test_decision_report_to_markdown() -> None:
    df = _sample_data()
    config = EvaluationConfig(
        features=["avg_page_clicks", "avg_base_fare_usd"],
        random_state=7,
    )

    sweep = run_k_sweep(df, config, k_values=[2])
    seed_sweep = run_seed_sweep(df, config, k=2, seeds=[7, 11])
    report = build_decision_report(
        chosen_k=2,
        k_sweep=sweep,
        silhouette_score=sweep.loc[0, "silhouette"],
        seed_sweep=seed_sweep,
        rationale="Aligns with reward-perk strategy.",
        notes=["Silhouette confirms separation."],
    )

    markdown = decision_report_to_markdown(report)

    assert "Segmentation k Decision Report" in markdown
    assert "**Chosen k:** 2" in markdown
    assert "Stability (Seed Sweep)" in markdown
    assert "k Sweep" in markdown


def test_run_seed_sweep_returns_metrics() -> None:
    df = _sample_data()
    config = EvaluationConfig(
        features=["avg_page_clicks", "avg_base_fare_usd"],
        random_state=7,
    )

    results = run_seed_sweep(df, config, k=2, seeds=[7, 11])

    assert results["seed"].tolist() == [7, 11]
    assert results["inertia"].notna().all()
    assert results["ari_to_reference"].iloc[0] == 1.0
