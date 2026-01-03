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
from typing import Any

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


def render_html_report(
    *,
    out_path: Path,
    title: str,
    metadata: dict[str, Any],
    session_df: pd.DataFrame,
    user_df: pd.DataFrame,
    charts: dict[str, str],
    sample_rows: int,
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
        session_shape=session_df.shape,
        user_shape=user_df.shape,
        session_missing=missingness_table(session_df).to_dict(orient="records"),
        user_missing=missingness_table(user_df).to_dict(orient="records"),
        session_sample=dataframe_preview_html(session_df, sample_rows),
        user_sample=dataframe_preview_html(user_df, sample_rows),
        charts=charts,
    )

    # Notes: Write as UTF-8 for portability; output becomes part of the artifact directory.
    out_path.write_text(html, encoding="utf-8")
