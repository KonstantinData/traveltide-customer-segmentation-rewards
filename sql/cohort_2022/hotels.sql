/*
Description:
Hotel-level extraction restricted to the cohort definition required for segmentation.
The cohort is defined by a fixed observation window starting after the New Year holiday
(2023-01-04) and a minimum amount of observed behavior per user (> 7 sessions) within
that same window.

# Notes:
# - The cohort is session-window based (not hotel-booking based).
# - Users must have > 7 sessions in the observation window to ensure sufficient behavioral signal.
# - Hotels are linked via trip_id, but trip_id is only considered after cohort eligibility is enforced.
# - page_clicks >= 2 is included explicitly for auditability, even if the source dataset already
#   satisfies a minimum-click condition by design.
*/

WITH cohort_sessions AS (
    SELECT
        ses.user_id,
        ses.trip_id,
        ses.page_clicks,
        ses.session_start
    FROM sessions AS ses
    WHERE ses.session_start >= '2023-01-04'
    -- # Note: Defines the fixed observation window for cohorting.
),
eligible_users AS (
    SELECT
        cs.user_id
    FROM cohort_sessions AS cs
    WHERE cs.page_clicks >= 2
    -- # Note: Ensures sessions carry a minimum amount of behavioral signal.
    GROUP BY cs.user_id
    HAVING COUNT(*) > 7
    -- # Note: Elena's eligibility criterion: users must have more than 7 sessions in the same window.
),
cohort_trips AS (
    SELECT DISTINCT
        cs.trip_id
    FROM cohort_sessions AS cs
    JOIN eligible_users AS eu
        ON eu.user_id = cs.user_id
    WHERE cs.trip_id IS NOT NULL
    -- # Note: Restricts downstream booking tables to trips observed within the cohort.
)
SELECT
    h.trip_id,
    h.hotel_name,
    h.nights,
    h.rooms,
    h.check_in_time,
    h.check_out_time,
    h.hotel_per_room_usd
FROM hotels AS h
JOIN cohort_trips AS ct
    ON ct.trip_id = h.trip_id;
-- # Note: Only hotel bookings connected to cohort-qualified trips are included.
