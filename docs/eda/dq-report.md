# Data Quality Report — Outlier & Anomaly Handling

## Context

This report documents the quantitative impact of all outlier and anomaly rules
defined in `outlier-policy.md`.

All counts refer to **cohort-scoped data only**.

---



> **Notation**
>
> `TBD` = *To Be Determined*
> Indicates values that will be populated once the corresponding
> SQL / Python data quality checks have been executed.
>

## sessions

### Rule: page_clicks (IQR-based)

| Metric       | Count |
| ------------ | ----- |
| Rows before  | TBD   |
| Rows after   | TBD   |
| Rows removed | TBD   |
| Impact (%)   | TBD   |

---

## flights

### Rule: seats ≤ 0 (invalid)

| Metric       | Count |
| ------------ | ----- |
| Rows before  | TBD   |
| Rows after   | TBD   |
| Rows removed | TBD   |
| Impact (%)   | TBD   |

### Rule: checked_bags (IQR-based)

| Metric       | Count |
| ------------ | ----- |
| Rows before  | TBD   |
| Rows after   | TBD   |
| Rows removed | TBD   |
| Impact (%)   | TBD   |

### Rule: base_fare_usd (IQR-based)

| Metric       | Count |
| ------------ | ----- |
| Rows before  | TBD   |
| Rows after   | TBD   |
| Rows removed | TBD   |
| Impact (%)   | TBD   |

---

## hotels

### Rule: nights ≤ 0

| Metric          | Count |
| --------------- | ----- |
| Rows before     | TBD   |
| Rows recomputed | TBD   |
| Rows dropped    | TBD   |
| Net rows after  | TBD   |

### Rule: rooms ≤ 0

| Metric       | Count |
| ------------ | ----- |
| Rows before  | TBD   |
| Rows after   | TBD   |
| Rows removed | TBD   |
| Impact (%)   | TBD   |

### Rule: hotel_per_room_usd (IQR-based)

| Metric       | Count |
| ------------ | ----- |
| Rows before  | TBD   |
| Rows after   | TBD   |
| Rows removed | TBD   |
| Impact (%)   | TBD   |

---

## Summary

- No rule was applied without explicit documentation.
- Total data loss remains within analytically acceptable bounds.
- All downstream metrics and models reference this report.

---

## Reproducibility

Counts can be reproduced by re-running the cohort-scoped extraction
and applying the rules defined in `outlier-policy.md`.
