SELECT 
    rate_date,
    currency_code,
    count(*) as curr_cnt_per_day
FROM {{ref('stg_cbar_rates')}}
GROUP BY rate_date, currency_code
HAVING count(*) > 1