SELECT 
    rate_date,
    currency_code,
    rate_per_unit
FROM {{ref('stg_cbar_rates')}}
WHERE rate_per_unit <= 0