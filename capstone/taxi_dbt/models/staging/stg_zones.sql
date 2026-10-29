-- One row per taxi zone
select
    LocationID    as zone_id,
    Borough       as borough,
    Zone          as zone_name,
    service_zone
from {{ source('raw', 'zones') }}
