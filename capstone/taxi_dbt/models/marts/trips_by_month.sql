-- EXAMPLE report model - use it as a pattern for your own.
-- Answers question 1: trips and revenue per month.
select
    strftime(pickup_at, '%Y-%m')          as pickup_month,
    count(*)                              as trips,
    round(sum(total_amount), 2)           as revenue,
    round(avg(distance_miles), 2)         as avg_distance_miles
from {{ ref('stg_trips') }}
group by pickup_month
order by pickup_month
