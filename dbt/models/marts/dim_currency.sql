WITH rates as (
    SELECT *
    FROM {{ref('stg_cbar_rates')}}
),
latest as (
    SELECT max(rate_date) as max_date
    FROM rates
),
per_currency as (
    SELECT 
        currency_code,
        arg_max(currency_name, rate_date) as currency_name,
        arg_max(currency_type, rate_date) as currency_type,
        min(rate_date) as first_seen_date,
        max(rate_date) as last_seen_date
    FROM rates
    GROUP BY currency_code
)
SELECT 
    p.currency_code,
    p.currency_name,
    p.currency_type,
    p.first_seen_date,
    p.last_seen_date,
    p.last_seen_date = l.max_date as is_active
FROM per_currency p
CROSS JOIN latest l