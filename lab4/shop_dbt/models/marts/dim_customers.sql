-- One row per customer
select distinct
    customer_id,
    customer_name,
    city
from {{ ref('stg_orders') }}
