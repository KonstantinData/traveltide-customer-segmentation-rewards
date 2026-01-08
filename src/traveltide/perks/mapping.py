"""Perks mapping helpers."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml


def load_mapping(config_path: str) -> pd.DataFrame:
    """Load the segment-to-perk mapping from YAML."""

    cfg = yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))
    rows = [
        {"segment": int(seg), **values}
        for seg, values in cfg["mapping"].items()
    ]
    return pd.DataFrame(rows)


def map_perks(assignments_path: str, config_path: str) -> pd.DataFrame:
    """Map segment assignments to persona names and perks."""

    assignments = pd.read_parquet(assignments_path)
    mapping = load_mapping(config_path)
    perks = assignments.merge(mapping, on="segment", how="left")
    return perks[["user_id", "segment", "persona_name", "primary_perk"]]


def write_customer_perks(
    assignments_path: str,
    config_path: str,
    out_path: str,
) -> Path:
    """Write the customer perks CSV and return the output path."""

    df = map_perks(assignments_path, config_path)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    return out
