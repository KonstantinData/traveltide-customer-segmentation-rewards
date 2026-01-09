# TravelTide — Step 1 EDA Data Dictionary (TT-012)

## Purpose

This document defines the **data contract** for the TT-012 Step 1 EDA artifacts.
It describes the columns emitted by the EDA generator so that Step 2 (Feature Engineering) and later
steps can rely on stable names, meanings, and grain.

---

## Artifact 1: `sessions_clean.parquet`

**Location:** `artifacts/eda/<timestamp>/data/sessions_clean.parquet`
**Grain:** **1 row per `session_id`**
**Source tables:** `sessions` (fact) joined with `users` (dimension) and `flights`/`hotels` (trip enrichment)

### Identifiers

- `session_id`: Unique session identifier
- `user_id`: Unique user identifier
- `trip_id`: Trip identifier (nullable when no trip context exists)

### Session fields (from `sessions`)

- `session_start`: Session start timestamp (UTC)
- `session_end`: Session end timestamp (UTC)
- `page_clicks`: Number of page interactions during the session
- `flight_discount`: Whether a flight discount was shown/applied (flag)
- `hotel_discount`: Whether a hotel discount was shown/applied (flag)
- `flight_discount_amount`: Discount amount for flight (nullable)
- `hotel_discount_amount`: Discount amount for hotel (nullable)
- `flight_booked`: Whether a flight booking occurred in this session (flag)
- `hotel_booked`: Whether a hotel booking occurred in this session (flag)
- `cancellation`: Whether the session is marked as cancellation-related (flag)

### User attributes (from `users`)

- `birthdate`: User birthdate (nullable)
- `gender`: Reported gender (nullable)
- `married`: Marital status flag (nullable)
- `has_children`: Whether user has children (nullable)
- `home_country`: Home country (nullable)
- `home_city`: Home city (nullable)
- `home_airport`: Home airport code (nullable)
- `sign_up_date`: Signup date used for cohort filtering

### Flight enrichment (from `flights`, left join)

- `origin_airport`: Origin airport code (nullable)
- `destination`: Destination city/location (nullable)
- `destination_airport`: Destination airport code (nullable)
- `seats`: Number of seats booked (nullable)
- `return_flight_booked`: Whether a return flight exists (nullable flag)
- `departure_time`: Flight departure timestamp (nullable)
- `return_time`: Return flight timestamp (nullable)
- `checked_bags`: Number of checked bags (nullable)
- `trip_airline`: Airline name/code (nullable)
- `base_fare_usd`: Base fare in USD (nullable)

### Hotel enrichment (from `hotels`, left join)

- `hotel_name`: Hotel name (nullable)
- `nights`: Number of nights (nullable; cleaned via TT-012 policy)
- `rooms`: Number of rooms booked (nullable)
- `check_in_time`: Check-in timestamp (nullable)
- `check_out_time`: Check-out timestamp (nullable)
- `hotel_per_room_usd`: Hotel price per room in USD (nullable)

### Derived columns (TT-012 preprocessing)

- `session_duration_sec`: `(session_end - session_start)` in seconds (nullable if timestamps missing)
- `age_years`: Approximate age in years (derived from `birthdate`, descriptive-only)
- `customer_tenure_days`: Days between `sign_up_date` and `session_start` (descriptive-only)

### Cleaning / outliers notes (TT-012)

- Invalid `nights` values (<= 0) are handled according to `config/eda.yaml`:
  - `recompute`: recompute from `(check_out_time - check_in_time)` and ceil to whole days, clamped to `>= 1`
  - `drop`: drop affected rows
- Outlier filtering is applied to configured numeric columns using the configured method (`iqr` or `zscore`).
- Removed row counts per column are recorded in `metadata.yaml` / `metadata.json`.

---

## Artifact 2: `users_agg.parquet`

**Location:** `artifacts/eda/<timestamp>/data/users_agg.parquet`
**Grain:** **1 row per `user_id`**
**Source:** Aggregation of `sessions_clean.parquet`

### Aggregated behavioral metrics

- `n_sessions`: Number of distinct sessions for the user
- `avg_page_clicks`: Mean `page_clicks` per session
- `p_flight_booked`: Mean of `flight_booked` (booking rate across sessions)
- `p_hotel_booked`: Mean of `hotel_booked` (booking rate across sessions)
- `p_cancellation_session`: Mean of `cancellation` (rate across sessions)
- `avg_base_fare_usd`: Mean `base_fare_usd` across sessions (nullable if no flight context)
- `avg_hotel_per_room_usd`: Mean `hotel_per_room_usd` across sessions (nullable if no hotel context)
- `avg_nights`: Mean `nights` across sessions
- `avg_rooms`: Mean `rooms` across sessions
- `avg_seats`: Mean `seats` across sessions

### Carried-forward user attributes

These fields are attached using a **first non-null** rule within each `user_id`:

- `gender`, `married`, `has_children`
- `home_country`, `home_city`, `home_airport`
- `sign_up_date`, `birthdate`

---

---

## Cleaned datasets

These datasets are **cleaned, typed, and validity-checked**. They are the cleaned outputs
used as the baseline for downstream transformations and modeling outputs.

**Location:** `artifacts/eda/<timestamp>/data/cleaned/`

### `sessions_cleaned.parquet`

- **Grain:** 1 row per `session_id`
- **Description:** Cleaned sessions data with standardized types and core session fields.

### `users_cleaned.parquet`

- **Grain:** 1 row per `user_id`
- **Description:** Cleaned user dimension data with standardized demographic attributes.

### `flights_cleaned.parquet`

- **Grain:** 1 row per `trip_id` (nullable for non-flight sessions)
- **Description:** Cleaned flight dimension data with standardized fares, airports, and timestamps.

### `hotels_cleaned.parquet`

- **Grain:** 1 row per `trip_id` (nullable for non-hotel sessions)
- **Description:** Cleaned hotel dimension data with standardized pricing and stay details.

---

## Transformed datasets

These datasets are **transformed** for consumption-ready analytics, aligned with cleaned grain
and nomenclature but enriched for downstream modeling and reporting.

**Location:** `artifacts/eda/<timestamp>/data/transformed/`

### `sessions_transformed.parquet`

- **Grain:** 1 row per `session_id`
- **Description:** Transformed sessions dataset derived from cleaned sessions.

### `users_transformed.parquet`

- **Grain:** 1 row per `user_id`
- **Description:** Transformed users dataset derived from cleaned users.

### `flights_transformed.parquet`

- **Grain:** 1 row per `trip_id` (nullable for non-flight sessions)
- **Description:** Transformed flights dataset derived from cleaned flights.

### `hotels_transformed.parquet`

- **Grain:** 1 row per `trip_id` (nullable for non-hotel sessions)
- **Description:** Transformed hotels dataset derived from cleaned hotels.

---

## Associated run files (context)

- `eda_report.html`: Human-readable EDA report (shapes, missingness, charts, previews)
- `metadata.yaml` / `metadata.json`: Audit trail (config, DB table row counts, row counts per stage, outlier removals)

---

## Stability guarantees (for Step 2+)

- Artifact grain and core column names are intended to remain stable.
- Any breaking change to column names, grain, or cleaning/outlier policy should be treated as a versioned change
  and reflected in both `config/eda.yaml` and this data dictionary.
