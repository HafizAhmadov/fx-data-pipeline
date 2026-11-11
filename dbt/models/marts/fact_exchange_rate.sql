WITH rates as (
    SELECT *
    FROM {{ref('stg_cbar_rates')}}
),
per_currency as (
    SELECT 
        rate_date, 
        currency_code,
        nominal, 
        rate_per_nominal,
        rate_per_unit,
        lag(rate_per_unit) 
        over (partition by currency_code order by rate_date) as prev_rate_per_unit,
        loaded_at
    FROM rates 
)
SELECT
    rate_date,
    currency_code,
    nominal,
    rate_per_nominal,
    rate_per_unit,
    prev_rate_per_unit,
    round((rate_per_unit - prev_rate_per_unit) / prev_rate_per_unit * 100, 4) as change_pct,
    loaded_at
FROM per_currency
