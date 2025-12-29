import argparse
import os
from typing import Sequence

from traveltide import __version__


def build_parser() -> argparse.ArgumentParser:
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

    sub = parser.add_subparsers(dest="command", required=False)

    info = sub.add_parser("info", help="Show project and environment info.")
    info.add_argument(
        "--show-env",
        action="store_true",
        help="Also print relevant environment variables (redacted if missing).",
    )

    return parser


def cmd_info(show_env: bool) -> int:
    print("TravelTide Customer Segmentation & Rewards")
    print(f"Version: {__version__}")
    if show_env:
        db_url = os.getenv("TRAVELTIDE_DATABASE_URL", "")
        print("TRAVELTIDE_DATABASE_URL:", "<set>" if db_url else "<not set>")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "info":
        return cmd_info(show_env=bool(args.show_env))

    # Default behavior: show help for friendly UX.
    parser.print_help()
    return 0
