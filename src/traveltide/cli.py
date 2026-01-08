"""CLI entry point for the TravelTide repository.

Notes:
- This script provides a single, stable command surface (`python -m traveltide ...`) for reproducibility.
- It intentionally stays thin: it routes to well-defined subcommands (e.g., Step 1 EDA artifact generation)
  while keeping business logic inside dedicated modules (e.g., `traveltide.eda`).
- This design supports CI automation, consistent local execution, and discoverability for reviewers.
"""

import argparse
import os
from pathlib import Path
from typing import Sequence

from traveltide import __version__
from traveltide.eda import run_eda
from traveltide.eda.dq_report import cmd_dq_report
from traveltide.features.pipeline import run_features
from traveltide.reports.executive_summary import cmd_executive_summary
from traveltide.reports.final_report import cmd_final_report


def build_parser() -> argparse.ArgumentParser:
    # Notes: Defines the CLI contract (commands + arguments) and keeps UX consistent across environments.
    parser = argparse.ArgumentParser(
        prog="traveltide",
        description=(
            "TravelTide customer segmentation & rewards (P0 scaffold). "
            "This CLI is intentionally minimal and exists for reproducibility and navigation."
        ),
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    # Notes: Subcommand registry for discoverable CLI navigation.
    sub = parser.add_subparsers(dest="command", required=False)

    # Notes: Project/environment info command (diagnostics / reproducibility support).
    info = sub.add_parser("info", help="Show project and environment info.")
    info.add_argument(
        "--show-env",
        action="store_true",
        help="Also print relevant environment variables (redacted if missing).",
    )

    # Notes: Reserved placeholder for a future end-to-end pipeline entrypoint (kept stable for roadmap).
    run = sub.add_parser("run", help="Golden path placeholder (not implemented yet).")
    run.add_argument(
        "--mode",
        default="golden-path",
        help="Execution mode placeholder (reserved for future pipeline modes).",
    )

    # Notes: TT-012 reproducible EDA report generator (artifact emitter).
    eda = sub.add_parser("eda", help="Generate the Step 1 (EDA) report artifact.")
    eda.add_argument(
        "--config",
        default=str(Path("config") / "eda.yaml"),
        help="Path to EDA YAML config (default: config/eda.yaml).",
    )
    eda.add_argument(
        "--outdir",
        default=str(Path("artifacts") / "eda"),
        help="Base output directory for versioned EDA artifacts (default: artifacts/eda).",
    )

    dq = sub.add_parser("dq-report", help="Generate the Data Quality report (TT-015).")
    dq.add_argument(
        "--artifacts-base",
        default=str(Path("artifacts") / "eda"),
        help="Base directory containing timestamped EDA runs.",
    )
    dq.add_argument(
        "--out",
        default=str(Path("reports") / "dq_report.md"),
        help="Path to the markdown file to write.",
    )

    exec_summary = sub.add_parser(
        "exec-summary", help="Generate the Step 3 executive summary PDF (TT-034)."
    )
    exec_summary.add_argument(
        "--source",
        default=str(
            Path("docs") / "step3_insights_strategy" / "step3_summary_report.md"
        ),
        help="Markdown source file containing the executive summary section.",
    )
    exec_summary.add_argument(
        "--out",
        default=str(Path("reports") / "executive_summary.pdf"),
        help="Path to the PDF file to write.",
    )

    final_report = sub.add_parser(
        "final-report", help="Generate the final report PDF (TT-035)."
    )
    final_report.add_argument(
        "--source",
        default=str(Path("docs") / "step4_presentation" / "final_report.md"),
        help="Markdown source file containing the final report content.",
    )
    final_report.add_argument(
        "--out",
        default=str(Path("reports") / "final_report.pdf"),
        help="Path to the PDF file to write.",
    )
    final_report.add_argument(
        "--max-pages",
        default=3,
        type=int,
        help="Maximum number of pages allowed for the final report.",
    )

    features = sub.add_parser(
        "features", help="Generate customer-level features from sessions_clean."
    )
    features.add_argument(
        "--config",
        default=str(Path("config") / "features.yaml"),
        help="Path to features YAML config (default: config/features.yaml).",
    )
    features.add_argument(
        "--outdir",
        default=str(Path("data") / "features"),
        help="Output directory for customer features (default: data/features).",
    )

    return parser


def cmd_info(show_env: bool) -> int:
    # Notes: Prints minimal versioning/runtime context to help debugging and ensure reproducibility.
    print("TravelTide Customer Segmentation & Rewards")
    print(f"Version: {__version__}")
    if show_env:
        db_url = os.getenv("TRAVELTIDE_DATABASE_URL", "")
        print("TRAVELTIDE_DATABASE_URL:", "<set>" if db_url else "<not set>")
    return 0


def cmd_run(mode: str) -> int:
    # Notes: Provides a stable placeholder command so automation/docs can reference it before implementation.
    print("Golden path placeholder: pipeline not implemented yet.")
    print(f"Requested mode: {mode}")
    return 0


def cmd_eda(config_path: str, outdir: str) -> int:
    # Notes: Executes TT-012 EDA pipeline and prints artifact locations for fast navigation.
    run_dir = run_eda(config_path=config_path, outdir=outdir)
    print(f"EDA artifact written to: {run_dir}")
    print(f"Report: {run_dir / 'eda_report.html'}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    # Notes: Entrypoint dispatcher — parses argv and routes to the correct subcommand implementation.
    parser = build_parser()
    args = parser.parse_args(argv)

    # Notes: "info" command routing.
    if args.command == "info":
        return cmd_info(show_env=bool(args.show_env))

    # Notes: "run" command routing.
    if args.command == "run":
        return cmd_run(mode=str(args.mode))

    # Notes: "eda" command routing.
    if args.command == "eda":
        return cmd_eda(config_path=str(args.config), outdir=str(args.outdir))

    if args.command == "dq-report":
        return cmd_dq_report(
            artifacts_base=Path(args.artifacts_base),
            out=Path(args.out),
        )

    if args.command == "exec-summary":
        return cmd_executive_summary(
            source=Path(args.source),
            out=Path(args.out),
        )

    if args.command == "final-report":
        return cmd_final_report(
            source=Path(args.source),
            out=Path(args.out),
            max_pages=int(args.max_pages),
        )

    if args.command == "features":
        out_path = run_features(config_path=str(args.config), outdir=str(args.outdir))
        print(f"Customer features written to: {out_path}")
        return 0

    # Notes: Default behavior (no subcommand): show help to keep UX self-documenting.
    parser.print_help()
    return 0
