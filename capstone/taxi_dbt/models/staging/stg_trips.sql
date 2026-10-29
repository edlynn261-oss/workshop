-- One clean row per taxi trip.
-- Every filter below removes rows that can't be real trips: write down
-- how many rows each rule removes for your data-quality slide!
with source as (

    select * from {{ source('raw', 'trips') }}

),

renamed as (

    select
        tpep_pickup_datetime                       as pickup_at,
        tpep_dropoff_datetime                      as dropoff_at,
        PULocationID                               as pickup_zone_id,
        DOLocationID                               as dropoff_zone_id,
        passenger_count,
        trip_distance                              as distance_miles,
        payment_type                               as payment_type_id,
        fare_amount,
        tip_amount,
        total_amount,
        date_diff('second', tpep_pickup_datetime, tpep_dropoff_datetime) / 60.0
                                                   as duration_minutes
    from source

)

select *
from renamed
where pickup_at >= timestamp '2024-01-01'          -- inside the months we downloaded
  and pickup_at <  timestamp '2024-04-01'          -- (change this if you add months)
  and distance_miles > 0 and distance_miles < 100   -- no zero or impossible distances
  and fare_amount > 0 and total_amount > 0          -- no refunds / negative amounts
  and duration_minutes between 1 and 180            -- 1 minute to 3 hours
