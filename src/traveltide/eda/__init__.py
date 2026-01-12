# Description: Step 1 (EDA) package namespace and public entrypoints.
"""Step 1 (EDA) package.

Notes:
- Exposes the public pipeline entrypoint used by the CLI.
- Internal modules are intentionally separated (config/extract/preprocess/report/pipeline) for clarity.
"""

from __future__ import annotations

__all__ = ["run_eda"]

# Notes: Public API re-export to keep CLI import stable even if internal structure evolves.
from .pipeline import run_eda
