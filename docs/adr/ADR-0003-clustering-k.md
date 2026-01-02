# ADR-0003: Choice of number of clusters (k)

**Status:** Accepted
**Date:** 2026-01-02

## Context

The rewards program requires assigning each customer a **primary perk**.
Marketing strategy defines five hypothesized perk categories.

## Decision

For K-Means clustering, we fix:

- **k = 5 clusters**

Clustering quality is evaluated via silhouette score and post-hoc interpretability.

## Rationale

- k aligns directly with the five reward-perk hypotheses
- Ensures one dominant perk per segment
- Avoids over-segmentation that would dilute marketing actionability

Alternative values of k were considered but rejected due to:
- reduced business interpretability
- overlap between resulting clusters

## Consequences

- Clustering is business-constrained rather than purely data-driven
- DBSCAN is explored as a qualitative comparison but not the primary model
