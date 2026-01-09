# Artifacts: Local Outputs & Reproducible Runs

This document describes how **local, reproducible artifacts** are produced in this repository. It focuses on **what is generated**, **how it is generated**, and **where outputs live** so new contributors can trace the full end-to-end flow from raw data to final segmentation outputs.

> Scope note: The workflow is **local-only**. The pipeline reads raw data files stored in the repo and writes derived outputs under `artifacts/`.

---

## 1) Purpose of the `artifacts/` directory

`artifacts/` is the **versioned output hub** for everything produced by analysis and modeling pipelines. It is intentionally separated from raw inputs (`data/`) and source code (`src/`).

### What lives here

Typical outputs include:

- **EDA outputs**: versioned run directories (tables, reports, metadata). Stored under `artifacts/eda/<run_id>/`. See `src/traveltide/eda/pipeline.py`.【F:src/traveltide/eda/pipeline.py†L1-L228】
- **Feature tables**: customer-level feature datasets used for modeling. Stored under `artifacts/outputs/`. See `src/traveltide/features/pipeline.py`.【F:src/traveltide/features/pipeline.py†L1-L74】
- **Segmentation outputs**: segment assignments, summaries, and evaluation reports. Stored under `artifacts/outputs/segments/`. See `src/traveltide/segmentation/run.py`.【F:src/traveltide/segmentation/run.py†L1-L98】
- **Perks mapping outputs**: customer-to-perk mapping CSV. Stored under `artifacts/outputs/perks/`. See `src/traveltide/perks/mapping.py`.【F:src/traveltide/perks/mapping.py†L1-L50】
- **Presentation assets**: figures exported from notebooks (e.g., step 4). Stored under `artifacts/step4_presentation/`. See `notebooks/04_presentation_assets.ipynb`.【F:notebooks/04_presentation_assets.ipynb†L13-L49】
- **Review-only examples**: `artifacts/example_run/` is a synthetic, static sample of the expected EDA output structure. It is **not** produced by the pipeline. See `artifacts/example_run/README.md`.【F:artifacts/example_run/README.md†L1-L27】
- **Gallery snapshots**: lightweight, committed SVGs for quick review (e.g., `artifacts/gallery`).【F:README.md†L74-L80】

### What should *not* live here

- **Raw inputs** (use `data/` instead).【F:data/README.md†L28-L46】
- **Secrets or credentials** (never store in repo).【F:SECURITY.md†L29-L29】
- **Source code** or configuration files (use `src/` and `config/`).
- **Large, irreproducible binaries** unless explicitly needed for review (prefer lightweight summaries).

---

## 2) Data origin and assumptions

### Data sources

The pipeline uses **local raw files** committed under `data/`.

- Expected raw tables:
  - `data/users_full.csv`
  - `data/sessions_full.csv`
  - `data/flights_full.csv`
  - `data/hotels_full.csv`【F:data/README.md†L28-L43】
- The loader resolves table paths using `data/<table>.csv` or `data/<table>_full.csv`. See `traveltide.data.raw_loader`.【F:src/traveltide/data/raw_loader.py†L31-L75】

### Formats and schema expectations

- Default raw format is **CSV**, parsed with pandas. See `load_table_from_raw` in `raw_loader.py`.【F:src/traveltide/data/raw_loader.py†L77-L94】
- The EDA session-level extract requires a stable set of columns defined in `traveltide.eda.extract`. Missing columns are created as `NA` to preserve schema stability across runs.【F:src/traveltide/eda/extract.py†L24-L112】
- Key assumptions:
  - Primary keys: `users.user_id`, `sessions.session_id`, `flights.trip_id`, `hotels.trip_id`.【F:data/README.md†L50-L66】
  - Join path: `users → sessions → flights/hotels` via `user_id` and `trip_id`.【F:data/README.md†L58-L62】
  - Cohort filter is based on `sign_up_date` (default: 2022).【F:config/eda.yaml†L5-L13】【F:src/traveltide/eda/extract.py†L132-L154】

### Timezones and typing

- Session timestamps are normalized to UTC in EDA preprocessing and cleaning steps. User birthdate/sign-up date are treated as local (tz-naive) for cohort and tenure calculations. See `add_derived_columns` and the cleaned table coercion helpers in `traveltide.eda.preprocess`.【F:src/traveltide/eda/preprocess.py†L23-L164】
- Feature engineering also explicitly normalizes timestamps and computes age/tenure with timezone conversions. See `run_features` in `traveltide.features.pipeline`.【F:src/traveltide/features/pipeline.py†L13-L57】

---

## 3) End-to-end pipeline overview

### High-level flow

```
Raw data (data/*.csv)
  → EDA extraction & cleaning
  → EDA artifacts (tables + metadata + report)
  → Feature engineering (customer-level)
  → Segmentation + evaluation outputs
  → Perk mapping + presentation assets
```

### Stage ownership (modules and entry points)

1. **EDA extraction + cleaning**
   - Orchestrator: `traveltide.eda.pipeline.run_eda` (`src/traveltide/eda/pipeline.py`).【F:src/traveltide/eda/pipeline.py†L1-L228】
   - Raw input loader: `traveltide.data.raw_loader` (`src/traveltide/data/raw_loader.py`).【F:src/traveltide/data/raw_loader.py†L1-L109】
   - Cleaning/validation/outlier policy: `src/traveltide/eda/preprocess.py`.【F:src/traveltide/eda/preprocess.py†L23-L593】
   - Output contract reference: `docs/eda/data-dictionary.md`.【F:docs/eda/data-dictionary.md†L1-L216】

2. **Feature engineering**
   - Orchestrator: `traveltide.features.pipeline.run_features` (`src/traveltide/features/pipeline.py`).【F:src/traveltide/features/pipeline.py†L13-L74】
   - Input source: `artifacts/eda/latest/data/sessions_clean.parquet` (configured in `config/features.yaml`).【F:config/features.yaml†L1-L9】

3. **Segmentation + evaluation**
   - Orchestrator: `traveltide.segmentation.run.run_segmentation_job` (`src/traveltide/segmentation/run.py`).【F:src/traveltide/segmentation/run.py†L1-L98】
   - Uses evaluation helpers for k/seed sweeps and DBSCAN comparison. See `src/traveltide/segmentation/evaluation.py`.【F:src/traveltide/segmentation/evaluation.py†L1-L246】

4. **Perks mapping**
   - Orchestrator: `traveltide.perks.mapping.write_customer_perks` (`src/traveltide/perks/mapping.py`).【F:src/traveltide/perks/mapping.py†L33-L50】
   - Mapping configuration: `config/perks.yaml`.【F:config/perks.yaml†L1-L17】

5. **Presentation assets (optional)**
   - Notebook-driven outputs: `notebooks/04_presentation_assets.ipynb` exports figures into `artifacts/step4_presentation/`.【F:notebooks/04_presentation_assets.ipynb†L13-L49】

---

## 4) Intermediate steps & artifact structure

### EDA runs: `artifacts/eda/<run_id>/`

The EDA pipeline emits a **timestamped run directory** to keep runs auditable. The `latest/` symlink (or copy) points to the most recent run for convenience. See `_timestamp_slug` and `latest` handling in `src/traveltide/eda/pipeline.py`.【F:src/traveltide/eda/pipeline.py†L33-L226】

Structure (key folders/files):

```
artifacts/eda/<run_id>/
├─ data/
│  ├─ sessions_clean.parquet
│  ├─ users_agg.parquet
│  ├─ cleaned/
│  │  ├─ sessions_cleaned.parquet
│  │  ├─ users_cleaned.parquet
│  │  ├─ flights_cleaned.parquet
│  │  └─ hotels_cleaned.parquet
│  └─ transformed/
│     ├─ sessions_transformed.parquet
│     ├─ users_transformed.parquet
│     ├─ flights_transformed.parquet
│     └─ hotels_transformed.parquet
├─ exploratory/
│  ├─ transform_experiments.json
│  └─ clustering/
│     ├─ kmeans_metrics.csv
│     ├─ dbscan_metrics.csv
│     ├─ kmeans_pca.png
│     ├─ dbscan_pca.png
│     └─ clustering_summary.json
├─ metadata.yaml
├─ metadata.json
└─ eda_report.html
```

**Category descriptions**

- **`data/sessions_clean.parquet`**
  - *What it is:* Cleaned, session-level dataset enriched with user and trip attributes plus derived session metrics.
  - *Produced by:* `run_eda` → `add_derived_columns`, `apply_validity_rules`, `remove_outliers` in `preprocess.py`.
  - *Used for:* Feature engineering and downstream analysis. See `docs/eda/data-dictionary.md`.【F:src/traveltide/eda/pipeline.py†L98-L184】【F:src/traveltide/eda/preprocess.py†L145-L520】【F:docs/eda/data-dictionary.md†L10-L216】

- **`data/users_agg.parquet`**
  - *What it is:* First-pass user-level aggregation (one row per user).
  - *Produced by:* `aggregate_user_level` in `preprocess.py`.
  - *Used for:* Exploratory analysis; quick sanity checks in EDA. See `docs/eda/data-dictionary.md`.【F:src/traveltide/eda/preprocess.py†L508-L559】【F:docs/eda/data-dictionary.md†L90-L149】

- **`data/cleaned/*.parquet`**
  - *What it is:* Type-stable, cleaned raw tables (no derived columns).
  - *Produced by:* `clean_*_table` functions in `preprocess.py`.
  - *Used for:* Clean baseline snapshots and audit of raw-to-clean transformations.【F:src/traveltide/eda/pipeline.py†L182-L219】【F:src/traveltide/eda/preprocess.py†L23-L83】

- **`data/transformed/*.parquet`**
  - *What it is:* Cleaned tables plus lightweight derived metrics (e.g., session duration, trip duration).
  - *Produced by:* `transform_*_table` helpers in `preprocess.py`.
  - *Used for:* Descriptive exploration and report stats.【F:src/traveltide/eda/pipeline.py†L208-L224】【F:src/traveltide/eda/preprocess.py†L91-L144】

- **`metadata.yaml` / `metadata.json`**
  - *What it is:* Run metadata including config snapshot, row counts, validity checks, and outlier impacts.
  - *Produced by:* `build_metadata` in `preprocess.py` and persisted in `run_eda`.
  - *Used for:* Reproducibility and data quality reporting (DQ report generation reads this).【F:src/traveltide/eda/preprocess.py†L562-L593】【F:src/traveltide/eda/pipeline.py†L226-L268】

- **`eda_report.html`**
  - *What it is:* Standalone EDA report with charts and tables embedded as base64.
  - *Produced by:* `render_html_report` in `report.py`.
  - *Used for:* Rapid review in browser or GitHub without opening notebooks.【F:src/traveltide/eda/report.py†L1-L226】【F:src/traveltide/eda/pipeline.py†L266-L305】

- **`exploratory/transform_experiments.json`**
  - *What it is:* Summary of exploratory scaling/feature-derivation experiments.
  - *Produced by:* `run_transform_experiments` in `transform_experiments.py`.
  - *Used for:* Hypothesis generation (not production features).【F:src/traveltide/eda/transform_experiments.py†L1-L186】

- **`exploratory/clustering/*`**
  - *What it is:* Experimental clustering trials (K-Means and DBSCAN) with metrics, plots, and JSON summary.
  - *Produced by:* `run_clustering_exploration` in `clustering_explore.py`.
  - *Used for:* EDA hypothesis only (explicitly non-production).【F:src/traveltide/eda/clustering_explore.py†L1-L258】

### Feature engineering: `artifacts/outputs/`

```
artifacts/outputs/
└─ customer_features.parquet
```

- *What it is:* One row per user with aggregated behavioral features for modeling.
- *Produced by:* `run_features` in `src/traveltide/features/pipeline.py` using config in `config/features.yaml`.
- *Used for:* Segmentation model input (`segmentation.yaml`).【F:src/traveltide/features/pipeline.py†L13-L74】【F:config/features.yaml†L1-L39】【F:config/segmentation.yaml†L1-L27】

### Segmentation outputs: `artifacts/outputs/segments/`

```
artifacts/outputs/segments/
├─ segment_assignments.parquet
├─ segment_summary.parquet
└─ decision_report.md
```

- *Produced by:* `run_segmentation_job` in `src/traveltide/segmentation/run.py`.
- *Used for:* Persona interpretation and perks mapping.【F:src/traveltide/segmentation/run.py†L55-L98】

### Perks mapping: `artifacts/outputs/perks/`

```
artifacts/outputs/perks/
└─ customer_perks.csv
```

- *Produced by:* `write_customer_perks` in `src/traveltide/perks/mapping.py`.
- *Used for:* Business-friendly export of persona + perk recommendations per user.【F:src/traveltide/perks/mapping.py†L33-L50】

---

## 5) Local reproducibility (no CLI walkthrough)

This repository is designed for **local execution**. You can trigger runs through an IDE run configuration, a notebook, or an orchestration script—without relying on shell commands in documentation.

Recommended local run order:

1. **EDA run**
   - Entry point: `traveltide.eda.pipeline.run_eda`.
   - Config: `config/eda.yaml` plus `eda.yml` workflow metadata.
   - Output: `artifacts/eda/<run_id>/` and `artifacts/eda/latest/`.

2. **DQ report (optional)**
   - Entry point: `traveltide.eda.dq_report.cmd_dq_report`.
   - Input: latest EDA `metadata.yaml` under `artifacts/eda/latest/`.
   - Output: markdown report under `reports/` (not in `artifacts/`).

3. **Feature engineering**
   - Entry point: `traveltide.features.pipeline.run_features`.
   - Config: `config/features.yaml` (expects `artifacts/eda/latest/data/sessions_clean.parquet`).
   - Output: `artifacts/outputs/customer_features.parquet`.

4. **Segmentation**
   - Entry point: `traveltide.segmentation.run.run_segmentation_job`.
   - Config: `config/segmentation.yaml`.
   - Output: `artifacts/outputs/segments/`.

5. **Perks mapping**
   - Entry point: `traveltide.perks.mapping.write_customer_perks`.
   - Config: `config/perks.yaml`.
   - Input: `artifacts/outputs/segments/segment_assignments.parquet`.
   - Output: `artifacts/outputs/perks/customer_perks.csv`.

6. **Presentation assets (optional)**
   - Notebook: `notebooks/04_presentation_assets.ipynb`.
   - Output: `artifacts/step4_presentation/` figures for slide decks/reporting.

### Configuration files that influence outputs

- `config/eda.yaml`: cohort boundaries, outlier rules, hotel-nights handling, report options.【F:config/eda.yaml†L1-L33】
- `eda.yml`: EDA workflow definition embedded into metadata and report.【F:eda.yml†L1-L49】
- `config/features.yaml`: feature aggregation rules and session-level input path.【F:config/features.yaml†L1-L39】
- `config/segmentation.yaml`: feature list + clustering evaluation parameters.【F:config/segmentation.yaml†L1-L27】
- `config/perks.yaml`: persona/perk mapping for segment IDs.【F:config/perks.yaml†L1-L17】

### Local prerequisites to verify

- **Raw data exists** under `data/` and matches expected column names. See `data/README.md`.【F:data/README.md†L28-L109】
- **Consistent Python environment** (dependencies in `requirements.txt` / `pyproject.toml`).
- **Filesystem access** to write under `artifacts/` (no shared network requirements).

---

## 6) Data quality & typical pitfalls

These are the most common failure or drift scenarios when regenerating artifacts locally:

### 1) Missing columns or schema drift

- **Symptom:** EDA extraction or segmentation raises errors for missing columns.
- **Why:** `traveltide.eda.extract` expects a stable session-level column list; segmentation expects configured feature columns to exist. See `_SESSION_LEVEL_COLUMNS` and `_validate_features`.【F:src/traveltide/eda/extract.py†L24-L112】【F:src/traveltide/segmentation/pipeline.py†L46-L76】
- **Detection:** Missingness appears in `metadata.yaml`, or errors are raised during feature/segmentation steps.

### 2) Timezone mismatches (tz-aware vs tz-naive)

- **Symptom:** Negative or nonsensical `session_duration_sec`, or tenure/age computations that look wrong.
- **Why:** Session timestamps are parsed in UTC, while signup/birthdate are treated as naive in several steps. Mixed timezone sources can skew deltas. See `add_derived_columns` and feature pipeline time derivations.【F:src/traveltide/eda/preprocess.py†L145-L183】【F:src/traveltide/features/pipeline.py†L13-L57】
- **Detection:** Outlier/validity summaries in `metadata.yaml` and EDA report sections flag anomalies.

### 3) Invalid hotel night values

- **Symptom:** `nights <= 0` or missing after recomputation.
- **Why:** Known raw anomaly; policy is controlled by `config/eda.yaml` (`recompute` vs `drop`). See `fix_invalid_hotel_nights` and `apply_validity_rules`.【F:config/eda.yaml†L15-L20】【F:src/traveltide/eda/preprocess.py†L184-L446】
- **Detection:** `metadata.yaml` includes invalid night counts and applied policy; DQ report summarizes impact.

### 4) Outlier policy removing too much data

- **Symptom:** Large row drops after outlier filtering.
- **Why:** IQR/Z-score thresholds configured in `config/eda.yaml` can be overly strict if distributions change. See `remove_outliers`.【F:config/eda.yaml†L21-L33】【F:src/traveltide/eda/preprocess.py†L444-L505】
- **Detection:** Row counts and per-column removal counts in `metadata.yaml`.

### Known limitations

- Exploratory clustering and transformation outputs are **non-production** and are **not** used by segmentation pipelines. They are intended only for EDA and hypothesis generation.【F:src/traveltide/eda/clustering_explore.py†L1-L12】【F:src/traveltide/eda/transform_experiments.py†L1-L13】
- The EDA report is currently **HTML-only** (no PDF export).【F:src/traveltide/eda/pipeline.py†L266-L276】

---

## Quick reference: artifacts map

| Stage | Primary outputs | Location |
| --- | --- | --- |
| EDA run | Cleaned + transformed tables, session/user aggregates, metadata, HTML report | `artifacts/eda/<run_id>/`【F:src/traveltide/eda/pipeline.py†L65-L305】 |
| Features | Customer-level feature table | `artifacts/outputs/customer_features.parquet`【F:src/traveltide/features/pipeline.py†L58-L74】 |
| Segmentation | Assignments, summary, decision report | `artifacts/outputs/segments/`【F:src/traveltide/segmentation/run.py†L72-L98】 |
| Perks | Persona + perk mapping | `artifacts/outputs/perks/customer_perks.csv`【F:src/traveltide/perks/mapping.py†L33-L50】 |
| Presentation | Slide/report assets | `artifacts/step4_presentation/`【F:notebooks/04_presentation_assets.ipynb†L13-L49】 |
