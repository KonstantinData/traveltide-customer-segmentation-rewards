# ADR-0002: Customer cohort definition

**Status:** Accepted
**Date:** 2026-01-02

## Context

Customer behavior accumulates over time.
Including users with very different platform tenures would bias segmentation
results and invalidate behavioral comparisons.

## Decision

The analysis cohort includes users who:

- signed up between **2022-01-01 and 2022-12-31**
- have at least one recorded session
- are not test or incomplete users (implicit via dataset constraints)

### Canonical implementation (SQL)

To avoid boundary ambiguity (date vs timestamp), the cohort window is implemented with an exclusive upper bound:

`sign_up_date >= '2022-01-01' AND sign_up_date < '2023-01-01'`

## Rationale

- Aligns customers to a comparable lifecycle stage
- Reduces bias caused by tenure-driven behavior differences
- Matches the strategic timeframe of the rewards program rollout

This definition is based on guidance from the Head of Marketing (business context)
and validated through exploratory data analysis.

## Implementation notes / Overrides

- The cohort filter MUST be applied at the user anchor level and propagated via joins (users → sessions → flights/hotels).
- Exploratory overrides are allowed, but must be parameterized (single source of truth) and documented in the respective analysis artifact (notebook/report).

## Consequences

- Results are not directly generalizable to very new or very old users
- Future iterations may compare multiple cohorts via additional ADRs
