WITH currencies as (
    SELECT 
        currency_code,
        first_seen_date,  
        CASE 
            WHEN is_active then (SELECT max(date_day) FROM {{ref('dim_date')}})
            else last_seen_date end as fill_until
    FROM {{ref('dim_currency')}}
), spine as (
    SELECT 
        d.date_day,
        c.currency_code
    FROM {{ref('dim_date')}} d
    JOIN currencies c ON d.date_day between c.first_seen_date and c.fill_until
), 
joining as (
    SELECT 
        s.date_day,
        er.rate_date,
        s.currency_code,
        er.rate_per_unit
    FROM spine s
    LEFT JOIN {{ref('fact_exchange_rate')}} er
    ON s.date_day = er.rate_date
    AND s.currency_code = er.currency_code
),
final as (
    SELECT 
        date_day,
        currency_code,
        last_value(rate_date ignore nulls) over w as rate_source_date,
        last_value(rate_per_unit ignore nulls) over w as rate_per_unit,
        rate_date is null as is_carried_forward
    FROM joining
    WINDOW w AS (
        PARTITION BY currency_code 
        ORDER BY date_day
        rows between unbounded preceding and current row
    )
)
SELECT
    date_day,
    currency_code,
    rate_per_unit,
    rate_source_date,
    is_carried_forward
FROM final

