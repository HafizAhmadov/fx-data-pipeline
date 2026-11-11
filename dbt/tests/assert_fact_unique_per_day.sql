SELECT 
    rate_date, 
    currency_code, 
    count(*) as row_count
FROM {{ref('fact_exchange_rate')}}
GROUP BY rate_date, currency_code
HAVING count(*) > 1