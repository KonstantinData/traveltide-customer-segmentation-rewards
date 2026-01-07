# TT-017 — Build user-level feature table (one row per user)

## Objective

Produce a Gold-layer, user-level feature table (one row per user) that is ready for downstream
segmentation. The table is derived from the cleaned session-level data (Silver) and includes
behavioral rates, spend aggregates, discount affinity, and activity recency/tenure signals.

## Inputs

- `data/sessions_clean.parquet` (Silver session-level table, produced by TT-012)

## Output

- `data/features/user_features.parquet`

## How to run

```bash
python -m traveltide features \
  --input data/sessions_clean.parquet \
  --output data/features/user_features.parquet
```

## Feature list

### Behavioral volume & activity

- `n_sessions`: number of sessions per user
- `n_trips`: number of unique trips per user
- `first_session_ts`: first session timestamp
- `last_session_ts`: most recent session timestamp
- `session_span_days`: days between first and last session
- `sessions_per_active_day`: sessions per active day (span + 1)

### Booking, cancellation & discount propensity

- `p_flight_booked`: share of sessions with a flight booking
- `p_hotel_booked`: share of sessions with a hotel booking
- `p_cancellation_session`: share of sessions with a cancellation
- `p_return_flight_booked`: share of sessions with a return flight booked
- `p_flight_discount`: share of sessions with a positive flight discount
- `p_hotel_discount`: share of sessions with a positive hotel discount

### Spend & trip characteristics (averages)

- `avg_page_clicks`
- `avg_session_duration_sec`
- `avg_base_fare_usd`
- `avg_hotel_per_room_usd`
- `avg_nights`
- `avg_rooms`
- `avg_seats`
- `avg_checked_bags`
- `avg_flight_discount`
- `avg_hotel_discount`
- `avg_flight_discount_amount`
- `avg_hotel_discount_amount`
- `avg_customer_tenure_days`
- `avg_age_years`

### Dimensional attributes (first non-null per user)

- `gender`, `married`, `has_children`
- `home_country`, `home_city`, `home_airport`
- `sign_up_date`, `birthdate`

## Notes

- All numeric features are mean-aggregated by user, excluding nulls.
- Discount propensity is measured by the share of sessions with a positive discount.
- Dimensional attributes are propagated via “first non-null” to avoid mixed values across sessions.
