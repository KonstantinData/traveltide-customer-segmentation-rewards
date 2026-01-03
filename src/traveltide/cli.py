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

    # Notes: Default behavior (no subcommand): show help to keep UX self-documenting.
    parser.print_help()
    return 0
