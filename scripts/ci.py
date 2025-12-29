"""
CI parity script.

Single Source of Truth:
- This script is the canonical CI command used by GitHub Actions.
- It runs formatting check, lint, and tests in a fixed, deterministic order.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from typing import Iterable


def run(cmd: list[str]) -> None:
    print(f"\n$ {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def main(argv: list[str] | None = None) -> int:
    python = sys.executable

    # Ensure required tools are available (installed via extras [dev]).
    if shutil.which("ruff") is None:
        # ruff is typically available as a console script; also runnable as `python -m ruff`.
        print("WARNING: ruff not found on PATH; attempting `python -m ruff` instead.")

    commands: Iterable[list[str]] = [
        [python, "-m", "ruff", "format", "--check", "."],
        [python, "-m", "ruff", "check", "."],
        [python, "-m", "pytest"],
    ]

    for cmd in commands:
        run(cmd)

    print("\nOK: CI checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
