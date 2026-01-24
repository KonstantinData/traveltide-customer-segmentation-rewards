"""End-to-end pipeline orchestration for TravelTide runs."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _timestamp_slug() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def _build_run_dir(base_dir: Path, run_id: str | None) -> Path:
    base_dir.mkdir(parents=True, exist_ok=True)

    if run_id:
        candidate = base_dir / run_id
    else:
        candidate = base_dir / _timestamp_slug()

    if not candidate.exists():
        candidate.mkdir(parents=True, exist_ok=False)
        return candidate

    suffix = _timestamp_slug()
    fallback = base_dir / f"{candidate.name}-{suffix}"
    fallback.mkdir(parents=True, exist_ok=False)
    return fallback


def run_end_to_end(
    *,
    mode: str,
    seed: int | None,
    run_id: str | None,
    outdir: str,
) -> Path:
    """Create a run directory and capture metadata for a pipeline run."""

    run_dir = _build_run_dir(Path(outdir), run_id)
    metadata: dict[str, Any] = {
        "mode": mode,
        "seed": seed,
        "run_id": run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    metadata_path = run_dir / "run_metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return run_dir
