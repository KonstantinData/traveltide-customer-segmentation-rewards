/*
Description:
Flight bookings restricted to the segmentation cohort definition:
users signed up in 2022, sessions observed from 2023-01-04 onward with page_clicks >= 2,
and users having more than 7 qualifying sessions in that window. Flights are included only
for trip_id values observed in cohort-qualified sessions.

# Notes:
# - Flight rows are filtered via trip_id derived from cohort sessions (prevents leakage).
# - Eligibility is computed from sessions, not from flights.
*/

WITH cohort_users AS (
    SELECT
        u.user_id
    FROM users AS u
    WHERE u.sign_up_date >= DATE '2022-01-01'
      AND u.sign_up_date <  DATE '2023-01-01'
),
cohort_sessions AS (
    SELECT
        s.user_id,
        s.trip_id,
        s.page_clicks,
        s.session_start
    FROM sessions AS s
    JOIN cohort_users AS cu
        ON cu.user_id = s.user_id
    WHERE s.session_start >= TIMESTAMP '2023-01-04'
      AND s.page_clicks >= 2
),
eligible_users AS (
    SELECT
        cs.user_id
    FROM cohort_sessions AS cs
    GROUP BY cs.user_id
    HAVING COUNT(*) > 7
),
cohort_trips AS (
    SELECT DISTINCT
        cs.trip_id
    FROM cohort_sessions AS cs
    JOIN eligible_users AS eu
        ON eu.user_id = cs.user_id
    WHERE cs.trip_id IS NOT NULL
    -- # Note: Only trips observed for eligible users in the observation window are kept.
)
SELECT
    f.*
FROM flights AS f
JOIN cohort_trips AS ct
    ON ct.trip_id = f.trip_id;
