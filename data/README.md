
# Data Engineering: Extraction & Processing Stages

This document describes how data is sourced, scoped (cohort), and processed through the **raw → cleaned → transformed → outputs** stages for the TravelTide customer segmentation project.

---

## Data availability & repository policy

### Raw data availability

The raw datasets are committed to this repository to keep analysis offline and reproducible.

### Expected local inputs (raw)

The full raw exports live in the repository `data/` directory:

```text
data/
├─ users_full.csv
├─ sessions_full.csv
├─ flights_full.csv
└─ hotels_full.csv
```

### What is versioned in Git

- This documentation (`data/README.md`)
- SQL extraction logic (queries in this document; optionally mirrored in `sql/`)
- Code used to build cleaned/transformed/outputs (EDA, feature engineering, segmentation)

### What is not versioned in Git

- Derived artifacts (cleaned/transformed/outputs), e.g. `*.parquet`, `*.csv` produced by the pipeline

---

## Cohort definition (analysis scope)

To ensure fair behavioral comparisons, the analysis is scoped to a defined cohort based on account creation date.

**Default cohort (recommended half-open interval):**

- `sign_up_date >= '2022-01-01'`
- `sign_up_date <  '2023-01-01'`

Half-open intervals are robust if `sign_up_date` is stored as a timestamp rather than a date.

---

## Data contract (minimal)

### Keys

- `users.user_id` (primary key)
- `sessions.session_id` (primary key)
- `flights.trip_id` (primary key for flight bookings)
- `hotels.trip_id` (primary key for hotel bookings)

### Join path

- `users.user_id` → `sessions.user_id`
- `sessions.trip_id` → `flights.trip_id` / `hotels.trip_id`

### Expected integrity checks (performed in cleaned tables)

- `users.user_id` is **unique** and **not null**
- `sessions.session_id` is **unique** and **not null**
- `sessions.user_id` exists in `users.user_id` for the cohort extract
- `trip_id` consistency is measured (not all sessions have a trip; that is acceptable)

---

## How to run (local workflow)

This repository is designed for a **local-first** workflow.

### 1) Provide raw inputs

Ensure the four `*_full.csv` files exist in:

- `data/users_full.csv`
- `data/sessions_full.csv`
- `data/flights_full.csv`
- `data/hotels_full.csv`

### 2) Build downstream layers

Run the EDA / feature engineering / segmentation entrypoints used by the project.

> Note: The exact commands depend on the project’s current implementation (scripts vs. notebooks vs. CLI).
> As a minimum, the pipeline should read from `data/` and write derived artifacts to `artifacts/eda/` and `artifacts/outputs/`.

Recommended outputs:

- `artifacts/eda/<timestamp>/data/cleaned/*.parquet` — cleaned, typed, validated tables
- `artifacts/eda/<timestamp>/data/transformed/*.parquet` — transformed tables with derived columns
- `artifacts/outputs/*.parquet` — user-level features and final segmentation outputs

---

## SQL extraction queries (Full → Cohort-scoped)

The following SQL queries describe how the cohort-scoped extracts are produced from the source database.
Even if the extraction was executed externally (SQL client / DB UI), these queries provide full transparency of scope and logic.

> Recommendation: Store these queries in versioned files under `sql/cohort_2022/` in addition to this README.

### 1) Users (cohort anchor)

```sql
SELECT *
FROM users
WHERE sign_up_date >= '2022-01-01'
  AND sign_up_date <  '2023-01-01';
```

### 2) Sessions (cohort-scoped)

```sql
SELECT
  ses.cancellation,
  ses.flight_booked,
  ses.flight_discount,
  ses.flight_discount_amount,
  ses.hotel_booked,
  ses.hotel_discount,
  ses.hotel_discount_amount,
  ses.page_clicks,
  ses.session_end,
  ses.session_id,
  ses.session_start,
  ses.trip_id,
  ses.user_id
FROM sessions AS ses
JOIN users AS use
  ON use.user_id = ses.user_id
WHERE use.sign_up_date >= '2022-01-01'
  AND use.sign_up_date <  '2023-01-01';
```

### 3) Flights (cohort-scoped via sessions → users)

```sql
SELECT
  fli.base_fare_usd,
  fli.checked_bags,
  fli.departure_time,
  fli.destination,
  fli.destination_airport,
  fli.destination_airport_lat,
  fli.destination_airport_lon,
  fli.origin_airport,
  fli.return_flight_booked,
  fli.return_time,
  fli.seats,
  fli.trip_airline,
  fli.trip_id
FROM flights AS fli
JOIN sessions AS ses
  ON ses.trip_id = fli.trip_id
JOIN users AS use
  ON use.user_id = ses.user_id
WHERE use.sign_up_date >= '2022-01-01'
  AND use.sign_up_date <  '2023-01-01';
```

### 4) Hotels (cohort-scoped via sessions → users)

```sql
SELECT
  hot.check_in_time,
  hot.check_out_time,
  hot.hotel_name,
  hot.hotel_per_room_usd,
  hot.nights,
  hot.rooms,
  hot.trip_id
FROM hotels AS hot
JOIN sessions AS ses
  ON ses.trip_id = hot.trip_id
JOIN users AS use
  ON use.user_id = ses.user_id
WHERE use.sign_up_date >= '2022-01-01'
  AND use.sign_up_date <  '2023-01-01';
```

---

## Processing stages (multi-hop)

This project applies a multi-hop pipeline to transform raw data into business-ready analytical outputs.

### Raw data: Ingestion

**Status:** Raw, immutable exports

- Source: SQL exports from the TravelTide database
- Format: CSV
- Files: `users_full.csv`, `sessions_full.csv`, `flights_full.csv`, `hotels_full.csv`
- Role: Landing zone for raw data. No transformations are applied here.

### Cleaned data: Cleansed & conformed

**Status:** Typed, validated, corrected where necessary

Typical steps:

- Type casting (timestamps, booleans, numeric fields)
- Schema enforcement and null handling
- Referential sanity checks (user_id/session_id uniqueness)
- Data quality corrections where required

#### Hotel nights correction (data quality)

A known anomaly can occur in the `hotels.nights` column (e.g., zero/negative or mismatched values).
In cleaned tables, a corrected value can be derived from timestamps:

- `nights_corrected = DATE(check_out_time) - DATE(check_in_time)`

Recommended practice:

- keep `nights_original`
- compute `nights_corrected`
- add `nights_was_corrected` (boolean flag)
- filter invalid records (`nights_corrected <= 0`) if they cannot be reconciled

#### Why Parquet in cleaned/transformed data?

Parquet is preferred over CSV for internal layers because it provides:

1. **Schema preservation** (types stored with the data)
2. **Columnar performance** for analytics workloads
3. **Compression & I/O efficiency** (smaller files, faster reads)

### Transformed & outputs: Business-level aggregates (model-ready)

**Status:** Enriched, aggregated, analytics-ready

Typical outputs:

- User-level feature table (one row per user)
- Segment assignments (cluster labels / personas)
- Perk recommendation per segment (business mapping)

Outputs are the final “source of truth” for:

- visualizations,
- segment interpretation,
- and executive summary / stakeholder communication.

---

## Notes on reproducibility (portfolio context)

This repository prioritizes:

- clear methodology,
- transparent cohort logic,
- and professional pipeline structuring.

Because raw data is distributed with the repository, external users can reproduce the results out-of-the-box. The extraction logic and processing steps are documented to demonstrate end-to-end capability and decision-making.
