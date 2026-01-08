-- sql/cohort_2022/flights.sql
SELECT
  fli.base_fare_usd,
  fli.checked_bags,
  fli.departure_time,
  fli.destination,
  fli.destination_airport,
  fli.destination_airport_lat,
  fli.destination_airport_lon,
  fli.origin_airport,
  fli.return_flight_booked,
  fli.return_time,
  fli.seats,
  fli.trip_airline,
  fli.trip_id
FROM flights AS fli
JOIN sessions AS ses
  ON ses.trip_id = fli.trip_id
JOIN users AS use
  ON use.user_id = ses.user_id
WHERE use.sign_up_date >= '2022-01-01'
  AND use.sign_up_date <  '2023-01-01';
