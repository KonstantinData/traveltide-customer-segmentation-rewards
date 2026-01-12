/*
Description:
User cohort definition for segmentation. Includes only users who signed up in 2022 and
meet the minimum behavioral eligibility threshold derived from sessions (observation window
from 2023-01-04 onward, page_clicks >= 2, and more than 7 sessions).

# Notes:
# - Cohort is defined by users.sign_up_date within 2022.
# - Eligibility is derived from sessions in the observation window.
# - The final user set is the intersection of cohort_users and eligible_users.
*/

WITH cohort_users AS (
    SELECT
        u.user_id
    FROM users AS u
    WHERE u.sign_up_date >= DATE '2022-01-01'
      AND u.sign_up_date <  DATE '2023-01-01'
    -- # Note: 2022 sign-up cohort (inclusive of 2022-12-31 via half-open interval).
),
observation_sessions AS (
    SELECT
        s.user_id,
        s.page_clicks
    FROM sessions AS s
    WHERE s.session_start >= TIMESTAMP '2023-01-04'
      AND s.page_clicks >= 2
    -- # Note: Observation window begins 2023-01-04; minimum activity enforced via page_clicks.
),
eligible_users AS (
    SELECT
        os.user_id
    FROM observation_sessions AS os
    GROUP BY os.user_id
    HAVING COUNT(*) > 7
    -- # Note: Eligibility threshold: more than 7 sessions in the observation window.
)
SELECT
    u.*
FROM users AS u
JOIN cohort_users AS cu
    ON cu.user_id = u.user_id
JOIN eligible_users AS eu
    ON eu.user_id = u.user_id;
