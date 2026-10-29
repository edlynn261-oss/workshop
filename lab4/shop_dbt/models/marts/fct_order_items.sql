-- One row per product sold in a non-cancelled order
select
    i.order_id,
    i.sku,
    o.customer_id,
    cast(o.ordered_at as date)          as order_date,
    strftime(o.ordered_at, '%Y-%m')     as order_month,
    i.product_name,
    i.category,
    i.quantity,
    i.unit_price,
    i.quantity * i.unit_price           as line_total
from {{ ref('stg_order_items') }} as i
join {{ ref('stg_orders') }}      as o on o.order_id = i.order_id
where o.status <> 'cancelled'
