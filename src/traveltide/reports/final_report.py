"""Final report PDF generator (TT-035).

Notes:
- Renders a concise markdown report into a PDF deliverable.
- Enforces a maximum page count to keep the final report stakeholder-friendly.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


@dataclass(frozen=True)
class FinalReport:
    title: str
    markdown: str


class _CountingCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.page_count = 0

    def showPage(self) -> None:
        self.page_count += 1
        super().showPage()

    def save(self) -> None:
        if self.page_count == 0:
            self.page_count = 1
        else:
            self.page_count += 1
        super().save()


def _format_inline(text: str) -> str:
    pattern = re.compile(r"(\*\*.+?\*\*|\*.+?\*)")
    parts: list[str] = []
    cursor = 0
    for match in pattern.finditer(text):
        if match.start() > cursor:
            parts.append(escape(text[cursor : match.start()]))
        token = match.group(0)
        if token.startswith("**"):
            parts.append(f"<b>{escape(token[2:-2])}</b>")
        else:
            parts.append(f"<i>{escape(token[1:-1])}</i>")
        cursor = match.end()
    if cursor < len(text):
        parts.append(escape(text[cursor:]))
    return "".join(parts)


def _is_table_separator(row: list[str]) -> bool:
    for cell in row:
        cleaned = cell.replace(":", "").replace("-", "").strip()
        if cleaned:
            return False
    return True


def _parse_table(lines: list[str], start: int) -> tuple[Table, int]:
    rows: list[list[str]] = []
    idx = start
    while idx < len(lines) and lines[idx].strip().startswith("|"):
        row = [cell.strip() for cell in lines[idx].strip().strip("|").split("|")]
        rows.append(row)
        idx += 1
    if len(rows) >= 2 and _is_table_separator(rows[1]):
        rows.pop(1)
    styles = getSampleStyleSheet()
    table = Table(
        [
            [Paragraph(_format_inline(cell), styles["BodyText"]) for cell in row]
            for row in rows
        ],
        hAlign="LEFT",
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2F4F6C")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table, idx


def _markdown_to_story(markdown: str) -> list:
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="Heading1Custom",
            parent=styles["Heading1"],
            spaceAfter=12,
        )
    )
    story: list = []
    lines = markdown.splitlines()
    idx = 0
    while idx < len(lines):
        line = lines[idx].rstrip()
        stripped = line.strip()
        if not stripped:
            idx += 1
            continue

        if stripped.startswith("# "):
            story.append(Paragraph(_format_inline(stripped[2:]), styles["Title"]))
            story.append(Spacer(1, 12))
            idx += 1
            continue

        if stripped.startswith("## "):
            story.append(Paragraph(_format_inline(stripped[3:]), styles["Heading2"]))
            story.append(Spacer(1, 6))
            idx += 1
            continue

        if stripped.startswith("### "):
            story.append(Paragraph(_format_inline(stripped[4:]), styles["Heading3"]))
            story.append(Spacer(1, 4))
            idx += 1
            continue

        if stripped.startswith("|"):
            table, idx = _parse_table(lines, idx)
            story.append(table)
            story.append(Spacer(1, 10))
            continue

        if stripped.startswith("- "):
            bullets: list[str] = []
            while idx < len(lines):
                current = lines[idx].strip()
                if not current.startswith("- "):
                    break
                bullets.append(current[2:].strip())
                idx += 1
            list_items = [
                ListItem(Paragraph(_format_inline(bullet), styles["BodyText"]))
                for bullet in bullets
            ]
            story.append(
                ListFlowable(
                    list_items,
                    bulletType="bullet",
                    leftIndent=12,
                    bulletFontName=styles["BodyText"].fontName,
                )
            )
            story.append(Spacer(1, 8))
            continue

        paragraph_lines = [stripped]
        idx += 1
        while idx < len(lines):
            next_line = lines[idx].strip()
            if not next_line or next_line.startswith(("#", "-", "|")):
                break
            paragraph_lines.append(next_line)
            idx += 1
        paragraph_text = " ".join(paragraph_lines)
        story.append(Paragraph(_format_inline(paragraph_text), styles["BodyText"]))
        story.append(Spacer(1, 8))

    return story


def build_final_report(source: Path) -> FinalReport:
    """Load the final report markdown content."""

    markdown = source.read_text(encoding="utf-8")
    title = "Final report"
    for line in markdown.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break
    return FinalReport(title=title, markdown=markdown)


def write_final_report_pdf(
    report: FinalReport,
    out_path: Path,
    *,
    max_pages: int = 3,
) -> None:
    """Write the final report to PDF, enforcing a maximum page count."""

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=letter,
        title=report.title,
        author="TravelTide",
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
    )

    page_tracker: dict[str, _CountingCanvas] = {}

    def _canvas_factory(*args, **kwargs) -> _CountingCanvas:
        new_canvas = _CountingCanvas(*args, **kwargs)
        page_tracker["canvas"] = new_canvas
        return new_canvas

    story = _markdown_to_story(report.markdown)
    doc.build(story, canvasmaker=_canvas_factory)

    canvas_instance = page_tracker.get("canvas")
    if canvas_instance is None:
        raise RuntimeError("Unable to determine page count for the final report.")
    if canvas_instance.page_count > max_pages:
        out_path.unlink(missing_ok=True)
        raise ValueError(
            f"Final report exceeds {max_pages} pages ({canvas_instance.page_count} pages)."
        )


def cmd_final_report(*, source: Path, out: Path, max_pages: int) -> int:
    report = build_final_report(source)
    write_final_report_pdf(report, out, max_pages=max_pages)
    print(f"Final report PDF written to: {out}")
    return 0
