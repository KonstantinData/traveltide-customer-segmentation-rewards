-- sql/cohort_2022/hotels.sql
SELECT
  hot.check_in_time,
  hot.check_out_time,
  hot.hotel_name,
  hot.hotel_per_room_usd,
  hot.nights,
  hot.rooms,
  hot.trip_id
FROM hotels AS hot
JOIN sessions AS ses
  ON ses.trip_id = hot.trip_id
JOIN users AS use
  ON use.user_id = ses.user_id
WHERE use.sign_up_date >= '2022-01-01'
  AND use.sign_up_date <  '2023-01-01';
