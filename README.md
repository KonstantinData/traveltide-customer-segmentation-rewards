# TravelTide Customer Segmentation & Rewards

Portfolio-style Mastery Project: customer segmentation for TravelTide and a data-driven rewards/perks mapping.

## Repository layout (golden path)

- `src/traveltide/` — Python package + CLI entry point (`python -m traveltide`)
- `tests/` — automated checks (CI runs `pytest -q`)
- `docs/` — narrative by project step + architecture decisions (ADR)
  - `docs/step1_exploration/`
  - `docs/step2_features_segmentation/`
  - `docs/step3_insights_strategy/`
  - `docs/step4_presentation/`
  - `docs/adr/`
- `notebooks/` — optional analysis notebooks (supporting, not the source of truth)
- `scripts/` — one-off utilities / demos
- `artifacts/` — generated outputs (exports, charts, tables). The folder is versioned, contents are generally ignored.

## How to run (placeholder)

```bash
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .

python -m traveltide --help
python -m pytest -q

# Optional local quality gates (same as CI)
python -m ruff check .
python -m ruff format --check .
```
