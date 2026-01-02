# Definition of Done (DoD)

This document defines what “Done” means for this repository: for day-to-day engineering work (PRs/issues) and for the four project phases (EDA → Features → Segmentation → Presentation).

## Why this exists

Segmentation projects are open-ended by nature. A clear DoD prevents scope drift, keeps quality consistent, and makes the project recruiter-friendly (reproducible + reviewable).

---

## Repo-level DoD (applies to every PR/issue)

A change is **Done** when all are true:

### Reproducibility

- The canonical local workflow still works: **clone → venv → install → run**.
- No secrets committed (e.g., `.env` stays gitignored). Any new config is documented.

### Quality gates

- `pytest -q` passes.
- `python -m ruff check .` passes.
- `python -m ruff format --check .` passes.
- CI is green on the default branch (where applicable).

### Documentation

- README and/or docs updated if usage, outputs, or interfaces changed.
- Non-trivial decisions are captured as an ADR (see `docs/adr/`) when triggered.

**ADR trigger rule (use ADR if one applies):**

- New dependency or major version change
- New data contract (new columns, new cohort rules, new feature definitions)
- New CLI command / interface change
- New evaluation approach (e.g., algorithm choice, KPI definition)

### Evidence (required in PR description)

Include either:

- the exact terminal output (preferred), or
- screenshots if terminal output is not practical.

Minimum evidence block:

```text
pytest -q
python -m ruff check .
python -m ruff format --check .
python -m traveltide --help
```
