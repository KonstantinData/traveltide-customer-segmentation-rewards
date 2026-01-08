from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

from traveltide.perks.mapping import map_perks


def test_map_perks_merges_segments(tmp_path: Path):
    assignments = pd.DataFrame(
        {
            "user_id": [101, 102],
            "segment": [1, 2],
        }
    )
    assignments_path = tmp_path / "assignments.parquet"
    assignments.to_parquet(assignments_path, index=False)

    mapping = {
        "mapping": {
            "1": {"persona_name": "Deal Seekers", "primary_perk": "Discounts"},
            "2": {"persona_name": "Explorers", "primary_perk": "Upgrades"},
        }
    }
    config_path = tmp_path / "perks.yaml"
    config_path.write_text(yaml.safe_dump(mapping), encoding="utf-8")

    perks = map_perks(str(assignments_path), str(config_path))

    assert list(perks.columns) == [
        "user_id",
        "segment",
        "persona_name",
        "primary_perk",
    ]
    assert perks.loc[perks["user_id"] == 101, "persona_name"].iloc[0] == "Deal Seekers"
