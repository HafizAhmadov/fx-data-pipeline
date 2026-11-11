WITH rates as (
    SELECT *
    FROM {{ref('stg_cbar_rates')}} 
),
start_end_dates as (
    SELECT min(rate_date) as start_date, max(rate_date) as end_date
    FROM rates
),
date_day_generator as (
    SELECT unnest(range(start_date, end_date + 1, interval 1 day))::date as date_day
    from start_end_dates
),
parse_date as (
    SELECT 
        date_day,
        year(date_day) as year,
        quarter(date_day) as quarter, 
        month(date_day) as month,
        monthname(date_day) as month_name,
        day(date_day) as day_of_month,
        isodow(date_day) as day_of_week,
        dayname(date_day) as day_name,
        weekofyear(date_day) as week_of_year,
        isodow(date_day) >= 6 as is_weekend
    FROM date_day_generator
),
publication_dates as (
    SELECT 
        DISTINCT rate_date
    FROM rates r 
) 
SELECT
    p.*, 
    pd.rate_date IS NOT NULL as is_publication_day
FROM parse_date p
LEFT JOIN publication_dates pd
ON p.date_day = pd.rate_date