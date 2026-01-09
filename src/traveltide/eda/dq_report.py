# Description: Data Quality (DQ) report generator for EDA artifacts.
"""Data Quality (DQ) report generator for TT-015.

Notes:
- Generates a markdown DQ report with before/after counts based on the *latest* EDA artifact metadata.
- The DQ report is an audit artifact: it explains what changed, why it changed, and how much data was affected.
- This module is intentionally I/O-light: it renders markdown from a metadata payload produced by the EDA pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


# Notes: Encapsulates before/after row impact for a single rule.
@dataclass(frozen=True)
class RuleImpact:
    """Single rule impact snapshot."""

    rows_before: int
    rows_after: int
    rows_removed: int

    @property
    def impact_pct(self) -> float:
        return (
            0.0
            if self.rows_before == 0
            else (self.rows_removed / self.rows_before) * 100.0
        )


def _fmt_int(n: int) -> str:
    return f"{int(n):,}".replace(",", "_")


def _fmt_pct(x: float) -> str:
    return f"{x:.2f}%"


# Notes: Load the most recent EDA run metadata payload.
def load_metadata(run_dir: Path) -> dict[str, Any]:
    """Load EDA run metadata from a run directory."""
    path = run_dir / "metadata.yaml"
    if not path.exists():
        raise FileNotFoundError(f"metadata.yaml not found in: {run_dir}")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


# Notes: Resolve the latest timestamped EDA run directory.
def find_latest_run(artifacts_base: Path) -> Path:
    """Find the latest timestamped EDA run directory within artifacts_base."""
    if not artifacts_base.exists():
        raise FileNotFoundError(f"Artifacts base directory not found: {artifacts_base}")
    runs = [p for p in artifacts_base.iterdir() if p.is_dir()]
    if not runs:
        raise FileNotFoundError(f"No run directories found in: {artifacts_base}")
    # Notes: run dirs are created as ISO-ish timestamps; lexicographic sort works.
    return sorted(runs)[-1]


# Notes: Convert metadata into a markdown audit report.
def render_dq_report_md(meta: dict[str, Any]) -> str:
    """Render a markdown DQ report from EDA metadata."""

    rows = meta.get("rows", {})
    n_raw = int(rows.get("session_level_raw", 0))
    n_valid = int(rows.get("session_level_after_validity", n_raw))
    n_clean = int(rows.get("session_level_clean", n_valid))

    validity: dict[str, Any] = meta.get("validity_rules", {}) or {}
    outliers: dict[str, Any] = meta.get("outliers", {}) or {}
    validation_checks: dict[str, Any] = meta.get("validation_checks", {}) or {}

    def _loss_pct(before: int, after: int) -> float:
        return 0.0 if before == 0 else ((before - after) / before) * 100.0

    def _render_rules_table(title: str, rules: dict[str, Any]) -> str:
        if not rules:
            return f"## {title}\n\nNo rules applied.\n\n"
        lines = [f"## {title}\n\n"]
        lines.append(
            "| Rule | Rows before | Rows after | Rows removed | Impact (%) |\n"
        )
        lines.append(
            "|------|------------:|-----------:|-------------:|-----------:|\n"
        )
        for name, ri in rules.items():
            r = RuleImpact(
                rows_before=int(ri.get("rows_before", 0)),
                rows_after=int(ri.get("rows_after", 0)),
                rows_removed=int(ri.get("rows_removed", 0)),
            )
            lines.append(
                "| {rule} | {before} | {after} | {removed} | {pct} |\n".format(
                    rule=name,
                    before=_fmt_int(r.rows_before),
                    after=_fmt_int(r.rows_after),
                    removed=_fmt_int(r.rows_removed),
                    pct=_fmt_pct(r.impact_pct),
                )
            )
        lines.append("\n")
        return "".join(lines)

    def _render_validation_checks(checks: dict[str, Any]) -> str:
        if not checks:
            return (
                "## Validity & consistency checks\n\nNo additional checks recorded.\n\n"
            )

        lines = ["## Validity & consistency checks\n\n"]
        lines.append(
            "| Check | Type | Details | Invalid/flagged rows | Decision | Rationale |\n"
        )
        lines.append(
            "|------|------|---------|---------------------:|----------|-----------|\n"
        )

        duplicates = checks.get("duplicates", {}) or {}
        if duplicates:
            status = duplicates.get("status", "evaluated")
            keys = duplicates.get("keys") or []
            detail = (
                f"keys: {', '.join(keys)}"
                if keys
                else duplicates.get("reason", "Missing key columns.")
            )
            invalid = (
                "N/A"
                if status == "skipped"
                else _fmt_int(int(duplicates.get("rows_in_duplicate_groups", 0)))
            )
            lines.append(
                "| Duplicate sessions | duplicates | {detail} | {invalid} | {decision} | {rationale} |\n".format(
                    detail=detail,
                    invalid=invalid,
                    decision=duplicates.get("decision", ""),
                    rationale=duplicates.get("rationale", ""),
                )
            )

        range_checks = checks.get("range_checks", {}) or {}
        for name, entry in range_checks.items():
            status = entry.get("status", "evaluated")
            invalid = (
                "N/A"
                if status == "skipped"
                else _fmt_int(int(entry.get("invalid_count", 0)))
            )
            detail = f"range: {entry.get('min_allowed')} to {entry.get('max_allowed')}"
            lines.append(
                "| {name} | range | {detail} | {invalid} | {decision} | {rationale} |\n".format(
                    name=name,
                    detail=detail,
                    invalid=invalid,
                    decision=entry.get("decision", ""),
                    rationale=entry.get("rationale", ""),
                )
            )

        logical_checks = checks.get("logical_checks", {}) or {}
        for name, entry in logical_checks.items():
            status = entry.get("status", "evaluated")
            invalid = (
                "N/A"
                if status == "skipped"
                else _fmt_int(int(entry.get("invalid_count", 0)))
            )
            detail = entry.get("comparison", "")
            lines.append(
                "| {name} | logical | {detail} | {invalid} | {decision} | {rationale} |\n".format(
                    name=name,
                    detail=detail,
                    invalid=invalid,
                    decision=entry.get("decision", ""),
                    rationale=entry.get("rationale", ""),
                )
            )

        lines.append("\n")
        return "".join(lines)

    md = []
    md.append("# Data Quality Report — Validity, Consistency, and Outlier Handling\n")
    md.append("## Context\n")
    md.append(
        "This report documents the quantitative impact of validity checks and outlier rules defined for the EDA pipeline.\n"
    )
    md.append(
        "All counts refer to **cohort-scoped** session-level data extracted by the Step-1 EDA pipeline.\n"
    )
    md.append("\n---\n\n")
    md.append("## Overview\n")
    md.append("| Stage | Rows | Data loss |\n|------|------:|----------:|\n")
    md.append(
        f"| Raw (cohort-scoped extract) | {_fmt_int(n_raw)} | {_fmt_pct(0.0)} |\n"
    )
    md.append(
        f"| After validity rules | {_fmt_int(n_valid)} | {_fmt_pct(_loss_pct(n_raw, n_valid))} |\n"
    )
    md.append(
        f"| After outlier removal (clean) | {_fmt_int(n_clean)} | {_fmt_pct(_loss_pct(n_raw, n_clean))} |\n\n"
    )
    md.append("---\n\n")

    md.append(_render_rules_table("Validity rules", validity))
    md.append(_render_validation_checks(validation_checks))
    md.append(_render_rules_table("Outlier rules", outliers))

    nights = meta.get("invalid_hotel_nights", {}) or {}
    if nights:
        policy = str(nights.get("policy", "recompute"))
        md.append("## Hotel nights anomaly handling\n\n")
        md.append(f"Policy: `{policy}` for `nights <= 0`.\n\n")
        md.append("| Metric | Count |\n|------|------:|\n")
        md.append(
            f"| Rows with invalid nights detected | {_fmt_int(int(nights.get('invalid_detected', 0)))} |\n"
        )
        if policy == "drop":
            md.append(
                f"| Rows dropped | {_fmt_int(int(nights.get('dropped_rows', 0)))} |\n"
            )
        else:
            md.append(
                f"| Rows successfully recomputed | {_fmt_int(int(nights.get('recomputed_success', 0)))} |\n"
            )
            md.append(
                f"| Rows still missing after recompute | {_fmt_int(int(nights.get('still_missing', 0)))} |\n"
            )
        md.append("\n---\n\n")

    md.append("## Reproducibility\n")
    md.append(
        "Re-run the Step-1 EDA pipeline and regenerate this report from the resulting `metadata.yaml`.\n"
    )
    md.append("\nGenerated by `python -m traveltide dq-report`.\n")
    return "".join(md)


# Notes: Persist the rendered report to disk.
def write_dq_report(out_path: Path, md: str) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")


# Notes: CLI entrypoint for generating the DQ report.
def cmd_dq_report(*, artifacts_base: Path, out: Path) -> int:
    run_dir = find_latest_run(artifacts_base)
    meta = load_metadata(run_dir)
    md = render_dq_report_md(meta)
    write_dq_report(out, md)
    print(f"DQ report written to: {out}")
    return 0
