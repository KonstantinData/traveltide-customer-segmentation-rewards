"""Report rendering utilities for the Step 1 (EDA) artifact (TT-012).

Notes:
- Renders a standalone HTML report (portable, easy to review in GitHub and locally).
- Charts are embedded as base64 PNG to avoid external file dependencies.
- The report is designed for quick stakeholder review: shapes, missingness, previews, core distributions.
"""

from __future__ import annotations

import base64
import io
from pathlib import Path
from typing import Any, Iterable

import matplotlib.pyplot as plt
import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape


def _fig_to_base64() -> str:
    # Notes: Serializes the current matplotlib figure to a base64 PNG for HTML embedding.
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    plt.close()  # Notes: Close to prevent memory growth in repeated runs.
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")


def build_basic_charts(df: pd.DataFrame) -> dict[str, str]:
    """Build a small set of universally useful EDA charts.

    Notes:
    - Keep chart types simple and widely interpretable (histograms).
    - Avoid style dependencies; matplotlib defaults keep outputs stable.
    - Only generate charts when the relevant columns exist and have data.
    """

    charts: dict[str, str] = {}

    if "page_clicks" in df.columns:
        # Notes: Distribution of engagement per session; important for cohort + behavior sanity checks.
        s = pd.to_numeric(df["page_clicks"], errors="coerce").dropna()
        if not s.empty:
            plt.figure()
            plt.hist(s, bins=40)
            plt.title("Session page clicks (distribution)")
            plt.xlabel("page_clicks")
            plt.ylabel("count")
            charts["page_clicks_hist"] = _fig_to_base64()

    if "session_duration_sec" in df.columns:
        # Notes: Quick data quality check (negative durations are suspicious).
        s = pd.to_numeric(df["session_duration_sec"], errors="coerce").dropna()
        s = s[s >= 0]
        if not s.empty:
            plt.figure()
            plt.hist(s, bins=40)
            plt.title("Session duration (seconds)")
            plt.xlabel("seconds")
            plt.ylabel("count")
            charts["session_duration_hist"] = _fig_to_base64()

    if "base_fare_usd" in df.columns:
        # Notes: Core economic distribution; supports price-sensitivity hypotheses.
        s = pd.to_numeric(df["base_fare_usd"], errors="coerce").dropna()
        if not s.empty:
            plt.figure()
            plt.hist(s, bins=40)
            plt.title("Flight base fare (USD)")
            plt.xlabel("USD")
            plt.ylabel("count")
            charts["base_fare_hist"] = _fig_to_base64()

    return charts


def dataframe_preview_html(df: pd.DataFrame, n: int) -> str:
    # Notes: Produces an HTML preview table for quick inspection without opening parquet files.
    return df.head(n).to_html(index=False, escape=True)


def missingness_table(df: pd.DataFrame) -> pd.DataFrame:
    """Return missingness summary sorted by missing % descending.

    Notes:
    - Missingness is a first-class EDA output; it frequently drives cleaning decisions.
    - Sorting by missingness helps reviewers focus on the highest-impact columns first.
    """

    total = len(df)
    miss = df.isna().sum().sort_values(ascending=False)

    out = pd.DataFrame(
        {
            "missing": miss,
            "missing_pct": (miss / total * 100.0).round(2) if total else 0.0,
            "dtype": df.dtypes.astype(str),
        }
    )
    return out.reset_index(names=["column"])


def data_overview(df: pd.DataFrame) -> dict[str, Any]:
    """Return a compact data overview for reporting."""

    numeric = df.select_dtypes(include="number")
    ranges = {
        col: {"min": float(numeric[col].min()), "max": float(numeric[col].max())}
        for col in numeric.columns
        if numeric[col].notna().any()
    }
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "numeric_ranges": ranges,
    }


def descriptive_stats_table(df: pd.DataFrame) -> list[dict[str, Any]]:
    """Return descriptive statistics for numeric columns."""

    numeric = df.select_dtypes(include="number")
    if numeric.empty:
        return []

    stats = numeric.agg(["mean", "median", "min", "max", "std"]).T
    stats = stats.round(4)
    stats.reset_index(inplace=True)
    stats.rename(columns={"index": "column"}, inplace=True)
    return stats.to_dict(orient="records")


def correlation_pairs(df: pd.DataFrame, *, top_n: int = 10) -> list[dict[str, Any]]:
    """Return top absolute correlation pairs for numeric columns."""

    numeric = df.select_dtypes(include="number")
    if numeric.shape[1] < 2:
        return []

    corr = numeric.corr().abs()
    pairs = []
    cols = list(corr.columns)
    for i, col_a in enumerate(cols):
        for col_b in cols[i + 1 :]:
            value = corr.loc[col_a, col_b]
            if pd.notna(value):
                pairs.append({"col_a": col_a, "col_b": col_b, "corr": float(value)})
    pairs.sort(key=lambda r: r["corr"], reverse=True)
    return pairs[:top_n]


def derive_key_insights(
    missingness: pd.DataFrame,
    outlier_rules: dict[str, Any],
    correlations: Iterable[dict[str, Any]],
) -> list[str]:
    """Create a short, data-driven insights list from EDA artifacts."""

    insights: list[str] = []

    if not missingness.empty:
        top = missingness.iloc[0]
        insights.append(
            f"Highest missingness: {top['column']} ({top['missing_pct']}% missing)."
        )

    if outlier_rules:
        most_removed = max(
            outlier_rules.items(), key=lambda item: item[1].rows_removed
        )
        insights.append(
            f"Most outliers removed: {most_removed[0]} ({most_removed[1].rows_removed} rows)."
        )

    if correlations:
        strongest = correlations[0]
        insights.append(
            "Strongest numeric association: "
            f"{strongest['col_a']} vs {strongest['col_b']} (|corr|={strongest['corr']:.2f})."
        )

    return insights


def derive_hypotheses(correlations: Iterable[dict[str, Any]], *, top_n: int = 3) -> list[str]:
    """Generate lightweight hypothesis candidates based on correlations."""

    hypotheses = []
    for pair in list(correlations)[:top_n]:
        hypotheses.append(
            "Investigate relationship between "
            f"{pair['col_a']} and {pair['col_b']} (|corr|={pair['corr']:.2f})."
        )
    return hypotheses


def render_html_report(
    *,
    out_path: Path,
    title: str,
    metadata: dict[str, Any],
    session_df: pd.DataFrame,
    user_df: pd.DataFrame,
    charts: dict[str, str],
    sample_rows: int,
    workflow: dict[str, Any],
    workflow_steps: list[dict[str, Any]],
    overview: dict[str, Any],
    session_stats: list[dict[str, Any]],
    user_stats: list[dict[str, Any]],
    correlations: list[dict[str, Any]],
    key_insights: list[str],
    hypotheses: list[str],
) -> None:
    """Render the EDA report as a standalone HTML file.

    Notes:
    - Uses Jinja2 template to keep layout separate from Python logic.
    - All dependencies are embedded (charts as base64, previews inline).
    """

    # Notes: Initialize template environment with autoescaping for safety.
    env = Environment(
        loader=FileSystemLoader(str(Path(__file__).parent / "templates")),
        autoescape=select_autoescape(["html"]),
    )
    tpl = env.get_template("eda_report.html.j2")

    # Notes: Build a compact template payload to keep the HTML stable and predictable.
    html = tpl.render(
        title=title,
        metadata=metadata,
        workflow=workflow,
        workflow_steps=workflow_steps,
        overview=overview,
        session_shape=session_df.shape,
        user_shape=user_df.shape,
        session_missing=missingness_table(session_df).to_dict(orient="records"),
        user_missing=missingness_table(user_df).to_dict(orient="records"),
        session_sample=dataframe_preview_html(session_df, sample_rows),
        user_sample=dataframe_preview_html(user_df, sample_rows),
        charts=charts,
        session_stats=session_stats,
        user_stats=user_stats,
        correlations=correlations,
        key_insights=key_insights,
        hypotheses=hypotheses,
    )

    # Notes: Write as UTF-8 for portability; output becomes part of the artifact directory.
    out_path.write_text(html, encoding="utf-8")
