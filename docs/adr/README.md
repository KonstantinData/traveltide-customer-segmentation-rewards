# Architecture & Analysis Decision Records (ADR)

This directory documents **material decisions** made during the TravelTide
Customer Segmentation & Rewards project.

We use ADRs to ensure:

- transparency of analytical and technical choices
- reproducibility of results
- reviewer- and recruiter-friendly reasoning

## ADR Format

Each ADR follows this structure:

- **Status**: Proposed | Accepted | Superseded
- **Context**: Problem or decision trigger
- **Decision**: What we decided
- **Rationale**: Why this decision was taken
- **Consequences**: Trade-offs, limitations, follow-ups
- **Date**

## Scope of ADRs in this project

ADRs cover:

- analytical methodology (e.g. cohort definition, clustering choices)
- technical stack and dependencies
- structural artifacts required for reproducibility

Minor implementation details are intentionally excluded.

## Index

- ADR-0001 — Project dependencies
- ADR-0002 — Customer cohort definition
- ADR-0003 — Choice of number of clusters (k)
- ADR-0004 — Required analysis artifacts
- ADR-0005 — Clustering algorithm choice (KMeans vs DBSCAN)
