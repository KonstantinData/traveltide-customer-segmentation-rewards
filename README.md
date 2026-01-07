# TravelTide — Customer Segmentation & Data-Driven Rewards

This repository is an end-to-end analytics case study for **TravelTide** (an e-booking startup). It is structured to be **portfolio-ready** and **reproducible** (clone → venv → install → run), with clear narrative documentation and a CLI entry point.

---

## Case study

### Problem

TravelTide is growing quickly, but customer loyalty is uneven. The business hypothesis is that **different customer archetypes respond to different incentives**, so a single blanket offer is suboptimal.

This project answers two practical business questions:

1) **Which distinct customer segments exist, based on observed browsing and booking behavior?**
2) **How should TravelTide tailor a rewards/perks program to increase sign-ups, retention, and customer lifetime value (CLV)?**

### Approach

**Analytical workflow**

1) **Exploration & data quality**
   - Validate schema expectations and join keys
   - Handle missingness/outliers
   - Define analysis population and exclusions (if needed)
2) **Feature engineering (customer-level)**
   - Aggregate session behavior into stable customer features (e.g., discount affinity, research intensity)
   - Aggregate booking behavior into stable customer features (e.g., spend levels, trip structure)
   - Produce a single customer-level table suitable for clustering
3) **Segmentation**
   - Scale/normalize features appropriately
   - Fit clustering (e.g., k-means / alternatives) and select `k` with quantitative + qualitative checks
   - Profile clusters into interpretable segments
4) **Rewards/perks strategy**
   - Translate segment behavior into a targeted reward hypothesis
   - Define success metrics (e.g., rewards sign-up conversion, retention uplift, incremental CLV)
   - Recommend rollout: pilot + A/B test + measurement plan

**Segment-to-reward framing (example, to validate with final profiles)**

- **Cost optimizers:** respond to *exclusive discounts / targeted offers*
- **Efficiency-focused travelers:** respond to *friction reduction + upgrades* (faster booking/experience improvements)
- **Flexibility seekers:** respond to *free cancellation / flexibility guarantees*

**Data architecture (layer model)**

- **Bronze (S3)** → raw, unmodified source data (not stored in repo)
- **Silver (`data/`)** → cleaned, validated Parquet tables
- **Gold (`data/features/`, `data/cohort/`, `reports/`)** → features, cohorts, KPIs, and reports

**Repository layout (golden path)**

- `src/traveltide/` — Python package + CLI entry point (`python -m traveltide`)
- `tests/` — automated checks (CI runs `pytest -q`)
- `docs/` — narrative documentation by project step + ADRs
- `notebooks/` — supporting notebooks (not the long-term source of truth)
- `scripts/` — one-off utilities / experiments
- `artifacts/` — generated outputs (exports, charts, tables)

**Definition of Done + Quality rubric**

- **Definition of Done:** [`docs/definition_of_done.md`](docs/definition_of_done.md)
- **Excellence Scorecard:** [`docs/excellence_scorecard.md`](docs/excellence_scorecard.md)

### Results (current)

- **Reproducible Step 1 EDA artifact generator** is implemented (TT-012), producing a versioned report and cleaned tables under `artifacts/`.
- **Project scaffold + CI baseline** (packaging, CLI entry point, lint/test hooks) is in place.

Future steps will finalize feature engineering, clustering, and segment-driven rewards strategy.

---

## How to run

### Prerequisites

- Python **3.12.x**
- Access to the TravelTide Postgres database (via `TRAVELTIDE_DATABASE_URL`)

### Setup (local venv)

```bash
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

**Windows PowerShell**

```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation scripts (current session only):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### CLI (golden path)

```bash
python -m traveltide --help
```

### Generate EDA artifacts (TT-012)

```bash
python -m traveltide eda --config config/eda.yaml --outdir artifacts/eda
```

### Outputs

Generated outputs go under `artifacts/`, for example:

- exported customer-level feature tables (CSV/Parquet)
- segment profiles (tables + plots)
- presentation assets (figures for slides/report)

### Quality gates (CI/local)

```bash
pytest -q
python -m ruff check .
python -m ruff format --check .
```

---

## Data source (high level)

The TravelTide dataset is hosted in a PostgreSQL database and organized around four core tables:

- `users` — user demographic / account attributes
- `sessions` — browsing sessions (behavioral events; e.g., clicks, discounts surfaced, cancellation intent)
- `flights` — purchased flight attributes (pricing, discounts, trip structure)
- `hotels` — purchased hotel stays (pricing, discounts, stay structure)

Credentials/connection details must **not** be committed to Git. Use environment variables (and optionally a local `.env` file, which is gitignored) when you implement data access.

---

## License

MIT License (see `LICENSE`).
