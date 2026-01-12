/*
Description:
Session extraction for behavioral analysis and downstream feature engineering.
Returns only sessions that (1) belong to the 2022 sign-up cohort, (2) fall within the
observation window starting 2023-01-04, (3) have page_clicks >= 2, and (4) belong to users
with more than 7 such sessions in the same window.

# Notes:
# - Cohort is user-based (sign_up_date in 2022).
# - Observation window is session-based (session_start >= 2023-01-04).
# - Eligibility is user-based, computed from qualifying sessions in the window.
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
        s.*
    FROM sessions AS s
    JOIN cohort_users AS cu
        ON cu.user_id = s.user_id
    WHERE s.session_start >= TIMESTAMP '2023-01-04'
      AND s.page_clicks >= 2
    -- # Note: Observation window + minimum activity applied at session level.
),
eligible_users AS (
    SELECT
        cs.user_id
    FROM cohort_sessions AS cs
    GROUP BY cs.user_id
    HAVING COUNT(*) > 7
    -- # Note: Keep only users with sufficient behavioral history in the window.
)
SELECT
    cs.cancellation,
    cs.flight_booked,
    cs.flight_discount,
    cs.flight_discount_amount,
    cs.hotel_booked,
    cs.hotel_discount,
    cs.hotel_discount_amount,
    cs.page_clicks,
    cs.session_end,
    cs.session_id,
    cs.session_start,
    cs.trip_id,
    cs.user_id
FROM cohort_sessions AS cs
JOIN eligible_users AS eu
    ON eu.user_id = cs.user_id;
