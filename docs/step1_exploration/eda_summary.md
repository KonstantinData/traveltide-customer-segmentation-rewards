## Exploratory Data Analysis Summary

The first step in the TravelTide pipeline is a **comprehensive exploratory data analysis (EDA)**.  The goals are to
understand the structure and quality of the raw event data, define the analysis cohort, and explore behavioural
patterns that might later inform feature design and segmentation.  This summary documents the high‑level
approach and highlights the most important observations from the sample dataset shipped with this repository.

### Data scope and cohort definition

The EDA operates on two primary tables derived from the raw TravelTide logs:

| Table                   | Description                                                                                                     | Record granularity |
|-------------------------|-----------------------------------------------------------------------------------------------------------------|--------------------|
| `sessions_clean.parquet`| Cleaned browsing sessions, one row per user session with derived columns for duration, page clicks and discounts | Session‑level      |
| `users_agg.parquet`     | Aggregated user statistics summarising sessions and bookings at the customer level                               | Customer‑level     |

The cohort definition, including date ranges and filters (e.g., minimum number of sessions), is controlled via
`config/eda.yaml`.  The sample configuration targets a small safe subset of data for demonstration purposes.

### Methodology

1. **Schema validation:** raw CSV/Parquet files are validated using Pandera schemas to ensure expected columns and
   types.  Records with missing mandatory identifiers are dropped.
2. **Cleaning and derivation:** session durations (in seconds) and page click counts are computed; negative or
   zero durations are removed.  Discount‑related flags are normalised to booleans.
3. **Missingness and outliers:** the pipeline produces a missingness overview chart and applies an IQR‑based
   outlier filter to numeric fields.  The outlier policy is described in `docs/eda/outlier-policy.md`.
4. **Descriptive statistics:** distributions of key variables (session duration, page clicks, base fare) are
   visualised and summarised with median/quantile statistics.  Relationships between variables are explored via
   scatter and correlation plots.

### Key observations

* **Session duration distribution:** most user sessions are short, with a right‑skewed distribution.  A small
  fraction of sessions exceed the IQR threshold and are treated as outliers.
* **Page clicks:** the number of page interactions per session varies widely.  Heavy clickers tend to exhibit
  longer session durations and higher engagement with discount offers.
* **Discount behaviour:** sessions where a flight discount was surfaced exhibit marginally higher base fares on
  average.  This may suggest that discount visibility is correlated with high‑value itineraries.
* **Missing data:** demographic fields (e.g., age, country) are sometimes missing at the raw level.  These fields
  are excluded from downstream feature engineering to maintain GDPR safety.

Full details, including per‑column statistics and interactive charts, can be found in the generated EDA report
(`artifacts/runs/<run_id>/step1_eda/<timestamp>/reports/eda_report.html`).  The plots catalogue in
`docs/step1_exploration/plots_catalog.md` lists all figures produced by the EDA pipeline.
