# ADR-0001: Project dependencies

**Status:** Accepted
**Date:** 2026-01-02

## Context

The project must be:
- reproducible on any machine
- aligned between local execution and CI
- limited to industry-standard analytics tooling

## Decision

The project uses the following dependencies:

- Python 3.12.x
- pandas
- numpy
- scikit-learn
- matplotlib / seaborn
- jupyter
- ruff (linting & formatting)
- pytest (minimal test scaffold)

Dependencies are declared in `requirements.txt`.
Execution relies on an editable install (`pip install -e .`).

## Rationale

- Python + sklearn is the industry default for customer segmentation
- Minimal dependency set avoids overfitting the toolchain
- Ruff ensures consistent code quality with low overhead
- Editable installs guarantee identical behavior between CLI, notebooks and CI

## Consequences

- Advanced ML libraries (e.g. xgboost, torch) are intentionally excluded
- Visualization is limited to static plots (no BI tooling)
- Dependency upgrades require a new ADR if they affect results
