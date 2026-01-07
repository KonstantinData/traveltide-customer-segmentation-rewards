"""Executive summary PDF generator (TT-034).

Notes:
- Extracts the executive summary section from a markdown report.
- Renders a single-page PDF for stakeholder sharing.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


@dataclass(frozen=True)
class ExecutiveSummary:
    title: str
    bullets: list[str]


def _extract_title(lines: list[str]) -> str:
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    return "Executive summary"


def _extract_exec_summary(lines: list[str]) -> list[str]:
    in_summary = False
    bullets: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            in_summary = stripped.lower() == "## executive summary"
            continue
        if stripped.startswith("# "):
            in_summary = False
            continue
        if in_summary and stripped.startswith("- "):
            bullets.append(stripped[2:].strip())
        elif in_summary and stripped:
            bullets.append(stripped)
    if not bullets:
        raise ValueError("No executive summary bullets found in source markdown.")
    return bullets


def build_executive_summary(source: Path) -> ExecutiveSummary:
    """Build the executive summary content from a markdown file."""

    lines = source.read_text(encoding="utf-8").splitlines()
    return ExecutiveSummary(
        title=_extract_title(lines),
        bullets=_extract_exec_summary(lines),
    )


def write_executive_summary_pdf(summary: ExecutiveSummary, out_path: Path) -> None:
    """Write the executive summary as a single-page PDF."""

    out_path.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=letter,
        title=summary.title,
        author="TravelTide",
        topMargin=54,
        bottomMargin=54,
        leftMargin=54,
        rightMargin=54,
    )

    story = [
        Paragraph(summary.title, styles["Title"]),
        Spacer(1, 16),
        Paragraph("Executive summary", styles["Heading2"]),
        Spacer(1, 8),
    ]

    bullet_items = [
        ListItem(Paragraph(bullet, styles["BodyText"]), leftIndent=12)
        for bullet in summary.bullets
    ]
    story.append(
        ListFlowable(
            bullet_items,
            bulletType="bullet",
            start="circle",
            leftIndent=16,
            bulletFontName=styles["BodyText"].fontName,
        )
    )

    doc.build(story)


def cmd_executive_summary(*, source: Path, out: Path) -> int:
    summary = build_executive_summary(source)
    write_executive_summary_pdf(summary, out)
    print(f"Executive summary PDF written to: {out}")
    return 0
