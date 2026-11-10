
with source as (
    select * from {{source("raw", "cbar_rates")}}
),
cleaned as (
    select 
        strptime(rate_date, '%d.%m.%Y')::DATE as rate_date, 
        case currency_type 
            when 'Bank metalları' then 'metal'
            when 'Xarici valyutalar' then 'currency' 
        end as currency_type, 
        currency_code,
        currency_name,
        TRY_CAST(regexp_replace(nominal, '[^0-9]', '', 'g') AS INT) as nominal,
        rate as rate_per_nominal,
        loaded_at
    from source
),
final as (
    select 
        rate_date, 
        currency_type, 
        currency_code,
        currency_name,
        nominal,
        rate_per_nominal,
        rate_per_nominal / nominal as rate_per_unit,
        loaded_at
    from cleaned
)
select * from final