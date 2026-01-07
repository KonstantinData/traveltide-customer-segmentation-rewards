# Data Quality Report — Outlier & Anomaly Handling

## Context

This report documents the quantitative impact of all validity and outlier rules
defined in `outlier-policy.md`. It is generated from the `metadata.yaml` emitted
by the Step-1 EDA pipeline.

All counts refer to **cohort-scoped session-level data** extracted by the EDA run.

---

## Structure

`reports/dq_report.md` contains:

1. **Overview** — raw vs. post-validity vs. post-outlier row counts (with data-loss %).
2. **Validity rules** — one row per rule (e.g., `invalid_hotel_nights`).
3. **Outlier rules** — one row per configured outlier column.
4. **Hotel nights detail** — recomputation vs. drops for `nights <= 0`.

---

## Reproducibility

1. Run the EDA pipeline:

   ```bash
   python -m traveltide eda --config config/eda.yaml --outdir artifacts/eda
   ```

2. Generate the DQ report from the latest artifact:

   ```bash
   python -m traveltide dq-report --artifacts-base artifacts/eda --out reports/dq_report.md
   ```
