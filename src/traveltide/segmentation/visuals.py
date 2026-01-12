"""Plotting helpers for k-robust segmentation visuals (TT-025)."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def _ensure_outdir(outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)


def _save_or_stub(fig: plt.Figure, path: Path, has_data: bool) -> None:
    if not has_data:
        fig.text(
            0.5,
            0.5,
            "No valid data to plot",
            ha="center",
            va="center",
            fontsize=12,
        )
        fig.set_facecolor("white")
        fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_k_sweep(
    k_sweep: pd.DataFrame,
    *,
    outdir: Path,
    chosen_k: int | None = None,
) -> dict[str, Path]:
    """Create inertia + silhouette plots for a k sweep."""

    _ensure_outdir(outdir)

    required = {"k", "inertia", "silhouette", "status"}
    missing = required - set(k_sweep.columns)
    if missing:
        missing_display = ", ".join(sorted(missing))
        raise ValueError(f"k_sweep missing required columns: {missing_display}")

    ok_rows = k_sweep[k_sweep["status"] == "ok"].copy()
    ok_rows["k"] = pd.to_numeric(ok_rows["k"], errors="coerce")
    ok_rows["inertia"] = pd.to_numeric(ok_rows["inertia"], errors="coerce")
    ok_rows["silhouette"] = pd.to_numeric(ok_rows["silhouette"], errors="coerce")
    ok_rows = ok_rows.dropna(subset=["k"])

    outputs: dict[str, Path] = {}

    fig, ax = plt.subplots(figsize=(6, 4))
    has_inertia = not ok_rows["inertia"].dropna().empty
    if has_inertia:
        ax.plot(ok_rows["k"], ok_rows["inertia"], marker="o")
        ax.set_xlabel("k")
        ax.set_ylabel("inertia")
        ax.set_title("K-Means inertia by k")
        ax.grid(True, linestyle="--", alpha=0.4)
        if chosen_k is not None:
            ax.axvline(chosen_k, color="tab:red", linestyle="--", alpha=0.7)
    inertia_path = outdir / "k_sweep_inertia.png"
    _save_or_stub(fig, inertia_path, has_inertia)
    outputs["k_sweep_inertia"] = inertia_path

    fig, ax = plt.subplots(figsize=(6, 4))
    has_silhouette = not ok_rows["silhouette"].dropna().empty
    if has_silhouette:
        ax.plot(ok_rows["k"], ok_rows["silhouette"], marker="o")
        ax.set_xlabel("k")
        ax.set_ylabel("silhouette")
        ax.set_title("Silhouette score by k")
        ax.grid(True, linestyle="--", alpha=0.4)
        if chosen_k is not None:
            ax.axvline(chosen_k, color="tab:red", linestyle="--", alpha=0.7)
    silhouette_path = outdir / "k_sweep_silhouette.png"
    _save_or_stub(fig, silhouette_path, has_silhouette)
    outputs["k_sweep_silhouette"] = silhouette_path

    return outputs


def plot_seed_sweep(seed_sweep: pd.DataFrame, *, outdir: Path) -> dict[str, Path]:
    """Create seed stability plots for a fixed k."""

    _ensure_outdir(outdir)

    required = {"seed", "silhouette", "ari_to_reference"}
    missing = required - set(seed_sweep.columns)
    if missing:
        missing_display = ", ".join(sorted(missing))
        raise ValueError(f"seed_sweep missing required columns: {missing_display}")

    seed_rows = seed_sweep.copy()
    seed_rows["seed"] = pd.to_numeric(seed_rows["seed"], errors="coerce")
    seed_rows["silhouette"] = pd.to_numeric(seed_rows["silhouette"], errors="coerce")
    seed_rows["ari_to_reference"] = pd.to_numeric(
        seed_rows["ari_to_reference"], errors="coerce"
    )
    seed_rows = seed_rows.dropna(subset=["seed"])
    seed_rows = seed_rows.sort_values("seed")

    outputs: dict[str, Path] = {}

    fig, ax = plt.subplots(figsize=(6, 4))
    has_silhouette = not seed_rows["silhouette"].dropna().empty
    if has_silhouette:
        ax.plot(seed_rows["seed"], seed_rows["silhouette"], marker="o")
        ax.set_xlabel("seed")
        ax.set_ylabel("silhouette")
        ax.set_title("Silhouette score by seed")
        ax.grid(True, linestyle="--", alpha=0.4)
    silhouette_path = outdir / "seed_sweep_silhouette.png"
    _save_or_stub(fig, silhouette_path, has_silhouette)
    outputs["seed_sweep_silhouette"] = silhouette_path

    fig, ax = plt.subplots(figsize=(6, 4))
    has_ari = not seed_rows["ari_to_reference"].dropna().empty
    if has_ari:
        ax.plot(seed_rows["seed"], seed_rows["ari_to_reference"], marker="o")
        ax.set_xlabel("seed")
        ax.set_ylabel("ARI to reference")
        ax.set_title("Seed stability (ARI)")
        ax.grid(True, linestyle="--", alpha=0.4)
    ari_path = outdir / "seed_sweep_ari.png"
    _save_or_stub(fig, ari_path, has_ari)
    outputs["seed_sweep_ari"] = ari_path

    return outputs


def write_k_robust_visuals(
    *,
    k_sweep: pd.DataFrame,
    seed_sweep: pd.DataFrame | None,
    outdir: Path,
    chosen_k: int | None = None,
) -> dict[str, Path]:
    """Write the k-robustness plot artifacts and return their paths."""

    _ensure_outdir(outdir)

    outputs = plot_k_sweep(k_sweep, outdir=outdir, chosen_k=chosen_k)
    if seed_sweep is not None:
        outputs.update(plot_seed_sweep(seed_sweep, outdir=outdir))
    return outputs
