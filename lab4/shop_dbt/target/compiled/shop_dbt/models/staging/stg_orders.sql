-- One clean row per order
with source as (

    select * from "shop"."raw"."orders"

),

deduplicated as (

    -- the shop sometimes sends the same order twice: keep one copy
    select *
    from source
    qualify row_number() over (partition by order_id order by order_id) = 1

)

select
    order_id,
    timezone('Asia/Kuala_Lumpur', order_date)  as ordered_at,   -- Malaysia local time
    lower(trim(status))                        as status,       -- ' Paid ' -> 'paid'
    payment_method,
    customer.customer_id                       as customer_id,
    customer.name                              as customer_name,
    coalesce(customer.city, 'Unknown')         as city
from deduplicated