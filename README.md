# TravelTide — Customer Segmentation & Data-Driven Rewards

This repository contains an end-to-end analytics project for **TravelTide** (an e-booking startup) that answers two practical business questions:

1) **Which distinct customer segments exist, based on observed browsing and booking behavior?**  
2) **How should TravelTide tailor a rewards/perks program to increase sign-ups, retention, and customer lifetime value (CLV)?**

The intended outcome is a **portfolio-ready** deliverable that is reproducible (clone → venv → install → run), clearly documented, and easy to review.

---

## What you will find here

### Core deliverables (project intent)
- **Exploration (EDA):** understand TravelTide’s customer journey and data quality
- **Feature engineering:** produce a customer-level “enriched” table suitable for segmentation
- **Segmentation:** cluster customers into interpretable segments and profile them
- **Rewards strategy:** map each segment to a tailored perk/reward hypothesis and success metrics

### Repository layout (golden path)
- `src/traveltide/` — Python package + CLI entry point (`python -m traveltide`)
- `tests/` — automated checks (CI runs `pytest -q`)
- `docs/` — narrative documentation by project step + architecture decisions (ADR)
  - `docs/step1_exploration/`
  - `docs/step2_features_segmentation/`
  - `docs/step3_insights_strategy/`
  - `docs/step4_presentation/`
  - `docs/adr/`
- `notebooks/` — supporting notebooks (optional; not the long-term source of truth)
- `scripts/` — one-off utilities / experiments
- `artifacts/` — generated outputs (exports, charts, tables). The folder is versioned; generated contents are typically ignored.

---

## Project status

This repository currently provides the **project scaffold + CI baseline** (packaging, CLI entry point, lint/tests hooks).  
The analytical pipeline (data extraction → feature engineering → clustering → reporting) is designed to be implemented iteratively in subsequent issues/steps.

---

## Business context (problem framing)

TravelTide is growing quickly, but customer loyalty is uneven. The business hypothesis is that **different customer archetypes respond to different incentives**, so a single blanket offer is suboptimal.

This project therefore:
- segments customers using behavioral signals, and
- proposes a rewards/perks program that is **personalized by segment** and can be tested via **pilot + A/B experimentation**.

---

## Data source (high level)

The TravelTide dataset is hosted in a PostgreSQL database and organized around four core tables:
- `users` — user demographic / account attributes
- `sessions` — browsing sessions (behavioral events; e.g., clicks, discounts surfaced, cancellation intent)
- `flights` — purchased flight attributes (pricing, discounts, trip structure)
- `hotels` — purchased hotel stays (pricing, discounts, stay structure)

Credentials/connection details must **not** be committed to Git. Use environment variables (and optionally a local `.env` file, which is gitignored) when you implement data access.

---

## Methodology (how the project is approached)

The project follows an industry-style flow:

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

---

## Segment-to-reward framing (example)

A practical mapping (to be validated with your final segment profiles) is:

- **Cost optimizers:** respond to *exclusive discounts / targeted offers*  
- **Efficiency-focused travelers:** respond to *friction reduction + upgrades* (faster booking/experience improvements)  
- **Flexibility seekers:** respond to *free cancellation / flexibility guarantees*  

Your final project should justify the mapping with segment evidence and propose measurable KPIs.

---

## Quickstart (local venv)

### Prerequisites
- Python **3.12.x** (project standard)

### 1) Create venv
```bash
python -m venv venv
```

If `python` does not point to your Python 3.12 interpreter on Windows, use:
```powershell
py -3.12 -m venv venv
```

### 2) Activate venv

**Windows PowerShell**
```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation scripts (current session only):
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**macOS / Linux**
```bash
source venv/bin/activate
```

### 3) Install dependencies + install package (editable)
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

### 4) Sanity check (expected to pass)
```bash
python -m traveltide --help
pytest -q
python -m ruff check .
python -m ruff format --check .
```

### 5) Deactivate
```bash
deactivate
```

---

## Using the CLI

The CLI is the intended “golden path” entry point:

```bash
python -m traveltide --help
```

Note: At the moment, CLI commands are placeholders; the pipeline will be wired in as the project progresses.

---

## Outputs

Generated outputs should go under `artifacts/`, for example:
- exported customer-level feature tables (CSV/Parquet)
- segment profiles (tables + plots)
- presentation assets (figures for slides/report)

---

## Quality gates (CI/local)

The repository enforces a minimal baseline:
- `pytest` for tests
- `ruff` for lint/format checks
- `pip-audit` for dependency auditing

Run the same checks locally as CI:

```bash
pytest -q
python -m ruff check .
python -m ruff format --check .
```

---

## License

MIT License (see `LICENSE`).

---
