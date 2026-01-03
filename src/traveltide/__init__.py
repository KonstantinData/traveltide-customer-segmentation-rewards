"""Step 1 (EDA) pipeline.

Notes:
- This package provides a reproducible EDA generator for TT-012.
- It is designed to be runnable headlessly (CLI/CI) and to emit versioned artifacts.
"""

from __future__ import annotations

__all__ = ["run_eda"]

from .pipeline import run_eda
