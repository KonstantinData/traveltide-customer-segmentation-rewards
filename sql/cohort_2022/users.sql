-- sql/cohort_2022/users.sql
SELECT *
FROM users
WHERE sign_up_date >= '2022-01-01'
  AND sign_up_date <  '2023-01-01';
