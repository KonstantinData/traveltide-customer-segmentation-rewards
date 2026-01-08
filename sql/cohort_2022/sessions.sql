-- sql/cohort_2022/sessions.sql
SELECT
  ses.cancellation,
  ses.flight_booked,
  ses.flight_discount,
  ses.flight_discount_amount,
  ses.hotel_booked,
  ses.hotel_discount,
  ses.hotel_discount_amount,
  ses.page_clicks,
  ses.session_end,
  ses.session_id,
  ses.session_start,
  ses.trip_id,
  ses.user_id
FROM sessions AS ses
JOIN users AS use
  ON use.user_id = ses.user_id
WHERE use.sign_up_date >= '2022-01-01'
  AND use.sign_up_date <  '2023-01-01';
