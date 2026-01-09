/*
Description:
User-level extraction limited to the same cohort definition as sessions.sql.
This guarantees consistency between demographic/user attributes and the behavioral cohort.

# Notes:
# - Uses the same session-window cohort and eligibility rule (>7 sessions).
# - Does not filter by sign_up_date unless the project explicitly requires it.
*/

WITH cohort_sessions AS (
    SELECT
        ses.user_id
    FROM sessions AS ses
    WHERE ses.session_start >= '2023-01-04'
    -- # Note: cohort window aligned with sessions.sql.
),
eligible_users AS (
    SELECT
        user_id
    FROM cohort_sessions
    GROUP BY user_id
    HAVING COUNT(*) > 7
    -- # Note: minimum behavior threshold per user.
)
SELECT
    u.*
FROM users AS u
JOIN eligible_users AS eu
    ON eu.user_id = u.user_id;
