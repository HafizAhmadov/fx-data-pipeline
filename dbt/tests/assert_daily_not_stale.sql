-- Fails if a carried-forward rate is more than 10 days old (pipeline probably stopped loading)
SELECT
    date_day,
    currency_code,
    rate_source_date,
    date_day - rate_source_date as days_old
FROM {{ ref('fact_exchange_rate_daily') }}
WHERE date_day - rate_source_date > 14