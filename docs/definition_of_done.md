# Definition of Done (DoD)

This document defines what “Done” means for the TravelTide customer segmentation & rewards project.
It applies to **all repository changes**, **all analytical phases**, and **all portfolio-facing deliverables**.

The goal is to eliminate ambiguity, prevent scope drift, and ensure a reproducible,
defensible, and recruiter-ready end-to-end project.

---

## Repo-level Definition of Done (applies to every PR / Issue)

A change is considered **Done** when **all** of the following criteria are met.

### 1. Reproducibility

- The local quickstart remains correct:
  - clone repository
  - create virtual environment
  - install dependencies
  - run checks successfully
- No secrets are committed.
- `.env` files remain gitignored.
- Configuration and required environment assumptions are documented.

---

### 2. Quality Gates

All quality gates must pass:

- `pytest -q`
- `python -m ruff check .`
- `python -m ruff format --check .`
- CI is green on the default branch (if applicable).

---

### 3. Documentation

- README or relevant docs are updated if behavior, usage, or assumptions change.
- Non-trivial decisions are documented.
- ADRs are used when introducing:
  - a new dependency
  - a new data contract
  - a new interface
  - a structural architectural change

---

### 4. Evidence

- The PR description includes evidence for key checks:
  - exact command output
  - logs or screenshots (where appropriate)
- Evidence must be sufficient for a reviewer to verify correctness without rerunning everything.

---

## Phase-level Definition of Done (Portfolio Outcomes)

In addition to the repo-level Definition of Done, each analytical phase is only considered
**Done** when it produces the minimum expected artifacts below and is reviewable end-to-end.

---

### Phase 1 — Exploration (EDA)

**Objective:** Establish a defensible understanding of the data, cohort, and data quality.

**Done when all are true:**

- Data schema, joins, and grain are explicitly documented.
- Cohort definition is stated and justified (who is included/excluded and why).
- Data quality issues (e.g. missing values, anomalies, outliers) are identified and
  handling decisions documented.
- Key assumptions and known limitations are explicitly written down.

**Minimum outputs:**

- Documented schema and join logic.
- EDA notes (tables/plots) sufficient to justify downstream feature choices.
- Session-level or intermediate tables exported to `artifacts/`
  *or* reproducible queries documented.

---

### Phase 2 — Feature Engineering

**Objective:** Create a clean, customer-level dataset suitable for segmentation.

**Done when all are true:**

- A single customer-level table exists (one row per user).
- Feature definitions are documented:
  - what the feature measures
  - how it is calculated
  - why it matters
- Feature leakage and temporal consistency are considered and addressed.
- Data types and value ranges are validated.

**Minimum outputs:**

- Customer-level feature dataset (CSV or Parquet).
- Feature dictionary (column, definition, rationale).
- Notes on excluded or discarded features.

---

### Phase 3 — Segmentation

**Objective:** Produce interpretable, defensible customer segments with business relevance.

**Done when all are true:**

- Segmentation or clustering approach is selected and justified
  (including scaling and parameter choices).
- Number of segments is explained and not arbitrary.
- Segment profiles are described in plain language.
- Segment-to-perk hypotheses are documented and traceable to segment behavior.

**Minimum outputs:**

- Segment assignment table.
- Segment summary tables and/or plots.
- Written segment profiles with clear differentiators.

---

### Phase 4 — Presentation

**Objective:** Deliver a stakeholder-ready narrative with clear business implications.

**Done when all are true:**

- Executive summary clearly communicates:
  - problem
  - approach
  - segments
  - recommendations
- KPIs for measuring impact are defined and tied to business outcomes.
- Rollout or validation plan exists (e.g. pilot, A/B test).
- Narrative is understandable without reading the code.

**Minimum outputs:**

- One-page executive summary.
- Slide deck or equivalent presentation artifact.
- KPI definitions and measurement plan.

---

## How to Use This Definition of Done

- Apply the **repo-level DoD** to every PR and issue.
- Apply the **phase-level DoD** at the end of each analytical phase.
- Use this document together with the Excellence Scorecard to answer one question quickly:

**“Is this work done?”**

If the answer cannot be determined in under 60 seconds,
the work is not done.

---
