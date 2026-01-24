## Feature Engineering Design

The goal of Step 2 is to transform raw session‑level data into a **customer‑level feature table** suitable for clustering and downstream analytics.  Feature design is guided by domain knowledge (what behaviours matter for rewards adoption) and by statistical patterns observed during EDA.  Each feature should have a clear business interpretation and be robust to missing or extreme values.

### Guiding principles

1. **Aggregation granularity** – All features are aggregated at the **customer** level.  Sessions are first cleaned and validated (Step 1) and then grouped by `user_id` for aggregation.  Booking‑level data (flights/hotels) are joined on the session identifiers to enrich behaviour signals.

2. **Interpretability** – Features are chosen to be easy to explain to business stakeholders.  Ratios and rates are preferred over raw counts when they better capture intensity or propensity (e.g., percentage of sessions with a discount).

3. **Robustness** – Outliers identified during EDA are either removed or Winsorised before aggregation.  Aggregations use medians instead of means where distributions are skewed.  Missing values are imputed with reasonable defaults (typically zero or the median) to avoid biasing cluster assignments.

4. **GDPR safety** – Demographic and personally identifiable information are not included.  All features are derived from behavioural logs and summarised at the user level.

### Core features and rationale

| Feature name               | Type     | Description and motivation                                                                                             |
|----------------------------|---------|-------------------------------------------------------------------------------------------------------------------------|
| `n_sessions`               | numeric | Total number of cleaned sessions per user.  Captures engagement frequency; high counts may indicate loyal users.        |
| `avg_page_clicks`          | numeric | Mean number of page clicks per session.  Measures browsing intensity; high values imply greater research behaviour.     |
| `avg_session_duration_sec` | numeric | Mean session duration in seconds.  Longer durations may correspond to complex trip planning or indecision.              |
| `research_intensity_ind`   | numeric | Ratio of sessions with more than a threshold of page clicks.  Identifies users who deeply research before booking.       |
| `discount_affinity_ind`    | numeric | Proportion of sessions where a flight or hotel discount was surfaced.  Indicates cost sensitivity.                       |
| `mean_spend_base_fare`     | numeric | Average base fare across booked flights.  Captures spending power; high spenders may be amenable to premium perks.      |
| `cancellations_pct`        | numeric | Percentage of sessions that resulted in a cancellation event.  High values signal risk of churn or dissatisfaction.      |
| `propensity_multi_city`    | numeric | Share of bookings that are multi‑city itineraries.  Multi‑city planners might value flexible or bundled rewards.         |
| `propensity_round_trip`    | numeric | Share of bookings that are simple round trips.  Complements `propensity_multi_city` to identify trip structure bias.     |
| `hotel_vs_flight_ratio`    | numeric | Ratio of hotel bookings to flight bookings.  Differentiates package travellers from flight‑only customers.              |
| `early_booking_ratio`      | numeric | Share of bookings made more than X days before departure.  Early planners may respond well to loyalty points or upgrades. |
| `late_booking_ratio`       | numeric | Share of bookings made within Y days of departure.  Late bookers might prioritise convenience and speed.               |

These features are specified in `config/features.yaml` under sections such as `numeric_means`, `bool_means`, and `first_non_null_cols`.  The configuration file also defines input paths and output locations.  The feature aggregation logic is implemented in `src/traveltide/features/pipeline.py`, which reads cleaned sessions, derives new columns, applies any necessary imputations, and writes a Parquet table.

### Implementation notes

* The aggregation functions rely on Pandas groupby operations and Pandera schema validation to ensure output consistency.
* Feature scaling/normalisation is applied later during segmentation (Step 3).  The feature table intentionally preserves raw units where meaningful.
* A small CSV preview of the feature table (first 5 rows) can be exported for documentation purposes, but the canonical dataset lives in the `artifacts/runs/<run_id>/step2_feature_engineering/data/` directory.
