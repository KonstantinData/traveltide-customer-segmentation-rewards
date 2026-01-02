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

## How We Define Done

This project uses an explicit Definition of Done and an Excellence Scorecard to ensure consistent, portfolio-grade quality across all phases.

- **Definition of Done (repo + phase level):**See [`docs/definition_of_done.md`](docs/definition_of_done.md)
- **Excellence Scorecard (quality rubric):**
  See [`docs/excellence_scorecard.md`](docs/excellence_scorecard.md)

These documents answer one question unambiguously:
**“Is this work done?”**

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

<pre class="overflow-visible! px-0!" data-start="5563" data-end="5603"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-powershell"><span><span>py </span><span>-3</span><span>.</span><span>126</span><span></span><span>-m</span><span> venv venv
</span></span></code></div></div></pre>

### 2) Activate venv

**Windows PowerShell**

<pre class="overflow-visible! px-0!" data-start="5651" data-end="5696"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-powershell"><span><span>.\venv\Scripts\Activate.ps1
</span></span></code></div></div></pre>

If PowerShell blocks activation scripts (current session only):

<pre class="overflow-visible! px-0!" data-start="5763" data-end="5839"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-powershell"><span><span>Set-ExecutionPolicy</span><span></span><span>-Scope</span><span></span><span>Process</span><span></span><span>-ExecutionPolicy</span><span> Bypass
</span></span></code></div></div></pre>

**macOS / Linux**

<pre class="overflow-visible! px-0!" data-start="5860" data-end="5896"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>source</span><span> venv/bin/activate
</span></span></code></div></div></pre>

### 3) Install dependencies + install package (editable)

<pre class="overflow-visible! px-0!" data-start="5956" data-end="6072"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
</span></span></code></div></div></pre>

### 4) Sanity check (expected to pass)

<pre class="overflow-visible! px-0!" data-start="6114" data-end="6218"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python -m traveltide --</span><span>help</span><span>
pytest -q
python -m ruff check .
python -m ruff format --check .
</span></span></code></div></div></pre>

### 5) Deactivate

<pre class="overflow-visible! px-0!" data-start="6239" data-end="6261"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>deactivate
</span></span></code></div></div></pre>

---

## Using the CLI

The CLI is the intended “golden path” entry point:

<pre class="overflow-visible! px-0!" data-start="6338" data-end="6377"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python -m traveltide --</span><span>help</span><span>
</span></span></code></div></div></pre>

Note: At the moment, CLI commands are placeholders; the pipeline will be wired in as the project progresses.

---

## Outputs

Generated outputs should go under `artifacts/`, for example:

* exported customer-level feature tables (CSV/Parquet)
* segment profiles (tables + plots)
* presentation assets (figures for slides/report)

---

## Quality gates (CI/local)

The repository enforces a minimal baseline:

* `pytest` for tests
* `ruff` for lint/format checks
* `pip-audit` for dependency auditing

Run the same checks locally as CI:

<pre class="overflow-visible! px-0!" data-start="6917" data-end="6993"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(--spacing(9)+var(--header-height))] @w-xl/main:top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pytest -q
python -m ruff check .
python -m ruff format --check .
</span></span></code></div></div></pre>

---

## License

MIT License (see `LICENSE`).
