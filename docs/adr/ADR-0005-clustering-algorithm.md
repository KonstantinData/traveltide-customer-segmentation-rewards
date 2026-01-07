# ADR-0005: Clustering algorithm choice (KMeans vs DBSCAN)

**Status:** Accepted
**Date:** 2026-01-03

## Context

The segmentation pipeline requires a clustering algorithm that supports
actionable, repeatable customer segments for rewards design. Two candidates
were evaluated:

- **KMeans**: centroid-based clustering with a predefined number of clusters.
- **DBSCAN**: density-based clustering that can label noise/outliers.

We compared both methods on the same scaled feature space using:

- number of clusters produced
- silhouette score (when valid)
- share of customers labeled as noise (DBSCAN)

## Decision

We select **KMeans** as the primary segmentation algorithm. DBSCAN remains a
diagnostic comparison for outlier sensitivity, not the production model.

## Rationale

- KMeans reliably yields the fixed number of segments required by the rewards
  program.
- DBSCAN results are highly sensitive to `eps`/`min_samples` and frequently
  either collapse into a single cluster or label large portions of the cohort
  as noise, reducing actionability.
- KMeans provides stable centroids that can be interpreted and monitored over
  time, supporting marketing narratives and perk assignment.

## Consequences

- The segmentation pipeline and evaluation tooling prioritize KMeans metrics.
- DBSCAN comparisons are used to sanity-check density/outlier effects but do
  not drive final segment assignments.
