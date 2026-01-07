"""Report generation utilities for executive summaries and stakeholder artifacts."""

from .executive_summary import (
    ExecutiveSummary,
    build_executive_summary,
    cmd_executive_summary,
    write_executive_summary_pdf,
)

__all__ = [
    "ExecutiveSummary",
    "build_executive_summary",
    "cmd_executive_summary",
    "write_executive_summary_pdf",
]
