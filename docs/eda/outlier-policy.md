# Outlier Policy — TravelTide Customer Segmentation

## Purpose

This document defines a project-wide, reproducible policy for detecting and handling
outliers and invalid values in the TravelTide dataset.

The goal is to prevent statistical distortion of aggregations and clustering results
while maintaining analytical transparency and auditability.

---

## Scope

Applies to:

- Cohort-scoped data only (see ADR-0002)
- Numeric, behavior-relevant fields used for aggregation or modeling

Does not apply to:

- Algorithm-internal robustness (e.g. DBSCAN noise handling)
- Post-clustering filtering

---

## Guiding Principles

1. **Transparency over convenience** No silent row removal.
2. **Conservative filtering** Prefer robust statistics over distributional assumptions.
3. **Reproducibility** All rules must be deterministic and re-runnable from raw data.
4. **Business plausibility**
   Thresholds must make sense in the TravelTide domain.

---

## Detection Methods

### 1. IQR-Based Outlier Detection (Default)

Used for skewed or unknown distributions.

Definition:

- IQR = Q3 − Q1
- Lower bound = Q1 − 1.5 × IQR
- Upper bound = Q3 + 1.5 × IQR

Rationale:

- Robust against skew and heavy tails
- No normality assumption

---

### 2. Validity Rules (Domain Constraints)

Applied where values are logically impossible and handled explicitly.

Current implementation:

- `nights <= 0` → recompute from timestamps when possible; drop only if policy is set to `drop`.

---

## Field-Specific Rules (Step-1 EDA)

The Step-1 EDA pipeline applies outlier filtering to the following numeric columns
as configured in `config/eda.yaml`:

- `page_clicks`
- `base_fare_usd`
- `hotel_per_room_usd`
- `nights`
- `rooms`
- `seats`

Each column uses the configured method (`iqr` by default) and removes rows that fall
outside the computed bounds. Missing values are retained.

---

## Handling Strategy Summary

- **Drop rows** when values are extreme per the configured outlier method
- **Recompute** only when a deterministic alternative exists (currently only for invalid `nights`)
- **Never cap / winsorize** (to avoid artificial clustering density)

---

## Documentation Requirements

Every application of this policy must be reflected in:

- `docs/eda/dq-report.md`
- Inline comments in SQL / notebooks referencing this document

---

## Change Log

Initial version — TT-015
