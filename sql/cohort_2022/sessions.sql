/*
Description:
Session-level extraction for segmentation prep. Defines a cohort based on a fixed analysis window
(starting after the New Year holiday) and a minimum amount of observed behavior per user.
No feature engineering is performed here—this is filtering and shaping the session-level dataset.

# Notes:
# - Cohort window: sessions with session_start >= '2023-01-04'
# - Engagement threshold: users must have > 7 sessions in that same window
# - Quality/activity threshold: keep only sessions with page_clicks >= 2
*/

WITH cohort_sessions AS (
    SELECT
        ses.*
    FROM sessions AS ses
    WHERE ses.session_start >= '2023-01-04'
    -- # Note: lower-bound defines the fixed observation window for cohorting.
),
eligible_users AS (
    SELECT
        user_id
    FROM cohort_sessions
    GROUP BY user_id
    HAVING COUNT(*) > 7
    -- # Note: ensures each user has enough sessions to represent behavior reliably.
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
    ON eu.user_id = cs.user_id
WHERE cs.page_clicks >= 2;
-- # Note: removes near-empty browsing sessions that carry little behavioral signal.
