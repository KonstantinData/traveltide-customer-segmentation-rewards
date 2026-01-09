# TravelTide — Step 2 Feature Data Dictionary (TT-019)

## Purpose

This document defines the **feature data contract** for the Step 2 customer-level dataset used
for segmentation. It specifies the expected output columns, how they are calculated, and the
source fields that populate them.

---

## Artifact: `customer_features.parquet`

**Location:** `artifacts/outputs/customer_features.parquet`
**Grain:** **1 row per `user_id`**
**Primary source:** `artifacts/eda/<timestamp>/data/sessions_clean.parquet`

> Note: `sessions_clean.parquet` is the cleaned, cohort-scoped session table produced in Step 1 EDA
> (see `docs/eda/data-dictionary.md` for the cleaned dataset contract).

---

## Feature dictionary

All features below are calculated over **all sessions for a user** unless otherwise noted.
Boolean flags are encoded as `0/1` for aggregation.

| Feature | Type | Definition | Calculation | Source columns |
| --- | --- | --- | --- | --- |
| `user_id` | string | Unique customer identifier. | Direct carry-forward. | `user_id` |
| `n_sessions` | integer | Total sessions observed for the user. | Count of distinct `session_id`. | `session_id` |
| `avg_session_duration_sec` | float | Average time spent per session. | Mean of `session_duration_sec`. | `session_duration_sec` |
| `avg_page_clicks` | float | Average interaction volume per session. | Mean of `page_clicks`. | `page_clicks` |
| `p_flight_booked` | float | Share of sessions with a flight booking. | Mean of `flight_booked`. | `flight_booked` |
| `p_hotel_booked` | float | Share of sessions with a hotel booking. | Mean of `hotel_booked`. | `hotel_booked` |
| `p_cancellation_session` | float | Share of sessions marked as cancellation-related. | Mean of `cancellation`. | `cancellation` |
| `p_flight_discount_shown` | float | Share of sessions where a flight discount was shown. | Mean of `flight_discount`. | `flight_discount` |
| `p_hotel_discount_shown` | float | Share of sessions where a hotel discount was shown. | Mean of `hotel_discount`. | `hotel_discount` |
| `avg_flight_discount_amount` | float | Typical flight discount level. | Mean of `flight_discount_amount` (null-safe). | `flight_discount_amount` |
| `avg_hotel_discount_amount` | float | Typical hotel discount level. | Mean of `hotel_discount_amount` (null-safe). | `hotel_discount_amount` |
| `avg_base_fare_usd` | float | Average base fare of booked flights. | Mean of `base_fare_usd` (null-safe). | `base_fare_usd` |
| `avg_hotel_per_room_usd` | float | Average nightly room rate. | Mean of `hotel_per_room_usd` (null-safe). | `hotel_per_room_usd` |
| `avg_nights` | float | Typical length of stay. | Mean of `nights`. | `nights` |
| `avg_rooms` | float | Typical number of rooms per hotel booking. | Mean of `rooms`. | `rooms` |
| `avg_seats` | float | Typical number of seats booked. | Mean of `seats`. | `seats` |
| `avg_checked_bags` | float | Typical number of checked bags. | Mean of `checked_bags` (null-safe). | `checked_bags` |
| `p_return_flight_booked` | float | Share of sessions with a return flight. | Mean of `return_flight_booked` (null-safe). | `return_flight_booked` |
| `customer_tenure_days` | float | Tenure between signup and most recent session. | `max(session_start) - sign_up_date` in days. | `session_start`, `sign_up_date` |
| `age_years` | float | Approximate customer age for profiling only. | Derived from `birthdate` at most recent session. | `birthdate`, `session_start` |
| `home_country` | string | Home country for geographic profiling. | First non-null value per user. | `home_country` |
| `home_city` | string | Home city for geographic profiling. | First non-null value per user. | `home_city` |
| `home_airport` | string | Home airport for travel profile. | First non-null value per user. | `home_airport` |
| `gender` | string | Reported gender for descriptive profiling. | First non-null value per user. | `gender` |
| `married` | boolean | Marital status flag for descriptive profiling. | First non-null value per user. | `married` |
| `has_children` | boolean | Flag indicating children for descriptive profiling. | First non-null value per user. | `has_children` |

---

## Feature engineering notes

- Features are computed from the **cohort-scoped** cleaned table (`sessions_clean.parquet`).
- Any additional transformations (e.g., scaling, log transforms) should be applied **after** this
  feature table is produced and should be documented in the segmentation workflow.
- Null-safe means are computed using available values only; if no values exist for a user, the
  feature remains null.

---

## Stability guarantees

- The grain (`user_id`) and column names above are intended to remain stable across Step 2 runs.
- Any breaking change to feature definitions or naming must update this document and the
  feature generation pipeline.
