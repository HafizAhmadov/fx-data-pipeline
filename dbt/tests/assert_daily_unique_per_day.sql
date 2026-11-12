SELECT 
    date_day,
    currency_code,
    count(*) as row_count
FROM {{ref('fact_exchange_rate_daily')}}
GROUP BY date_day, currency_code
HAVING count(*) > 1