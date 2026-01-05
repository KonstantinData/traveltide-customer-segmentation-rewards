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

1. **Transparency over convenience**No silent row removal.
2. **Conservative filtering**Prefer robust statistics over distributional assumptions.
3. **Reproducibility**All rules must be deterministic and re-runnable from raw data.
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

### 2. Hard Validity Rules (Domain Constraints)

Applied where values are logically impossible.

Examples:

- `nights <= 0` → invalid
- `seats <= 0` → invalid
- `rooms <= 0` → invalid
- monetary values `< 0` → invalid

---

## Field-Specific Rules

### sessions

| Field       | Rule type | Handling |
| ----------- | --------- | -------- |
| page_clicks | IQR       | Drop row |

---

### flights

| Field         | Rule type | Handling         |
| ------------- | --------- | ---------------- |
| seats         | Hard rule | Drop row if ≤ 0 |
| checked_bags  | IQR       | Drop row         |
| base_fare_usd | IQR       | Drop row         |

---

### hotels

| Field              | Rule type | Handling                                         |
| ------------------ | --------- | ------------------------------------------------ |
| nights             | Hard rule | Recompute from timestamps if possible, else drop |
| rooms              | Hard rule | Drop row if ≤ 0                                 |
| hotel_per_room_usd | IQR       | Drop row                                         |

---

## Handling Strategy Summary

- **Drop rows** when values are invalid or extreme and cannot be reliably corrected
- **Recompute** only when a deterministic alternative exists
- **Never cap / winsorize** (to avoid artificial clustering density)

---

## Documentation Requirements

Every application of this policy must be reflected in:

- `docs/eda/dq-report.md`
- Inline comments in SQL / notebooks referencing this document

---

## Change Log

Initial version — TT-015
