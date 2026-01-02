# ADR-0004: Analysis artifacts and structure

**Status:** Accepted
**Date:** 2026-01-02

## Context

The project must be:
- reviewable without executing code
- reproducible end-to-end
- suitable as a portfolio artifact

## Decision

The following artifacts are mandatory:

- Jupyter notebooks, ordered by project phase:
  - 01_exploration.ipynb
  - 02_feature_engineering.ipynb
  - 03_segmentation.ipynb
  - 04_presentation_assets.ipynb
- A final CSV assigning users to perks
- A README explaining structure and execution
- ADRs documenting key analytical decisions

## Rationale

- Mirrors real-world analytics workflows
- Separates exploration, modeling, and communication
- Enables technical and non-technical review

## Consequences

- No single “mega-notebook”
- All major transformations must be explainable in markdown or ADRs
- Artifacts are treated as first-class deliverables
