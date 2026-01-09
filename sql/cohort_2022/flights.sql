/*
Description:
Trip-level extraction restricted to cohort-eligible users to keep feature engineering downstream valid.

# Notes:
# - Always derive eligible_users from sessions within the cohort window.
# - Join to trips/flights/hotels only after cohort restriction.
*/

WITH cohort_sessions AS (
    SELECT
        ses.user_id,
        ses.trip_id
    FROM sessions AS ses
    WHERE ses.session_start >= '2023-01-04'
),
eligible_users AS (
    SELECT
        user_id
    FROM cohort_sessions
    GROUP BY user_id
    HAVING COUNT(*) > 7
),
cohort_trips AS (
    SELECT DISTINCT
        cs.trip_id,
        cs.user_id
    FROM cohort_sessions AS cs
    JOIN eligible_users AS eu
        ON eu.user_id = cs.user_id
    WHERE cs.trip_id IS NOT NULL
)
-- Then join cohort_trips to flights/hotels on trip_id
SELECT
    f.*
FROM flights AS f
JOIN cohort_trips AS ct
    ON ct.trip_id = f.trip_id;
