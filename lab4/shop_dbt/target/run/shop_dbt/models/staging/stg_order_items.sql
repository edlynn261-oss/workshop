
  
  create view "shop"."main"."stg_order_items__dbt_tmp" as (
    -- One clean row per product in each order
with orders as (

    select distinct order_id, items
    from "shop"."raw"."orders"

),

items as (

    -- unnest = turn the list of items into one row per item
    select order_id, unnest(items) as item
    from orders

)

select
    order_id,
    item.sku                                   as sku,
    item.product_name                          as product_name,
    item.category                              as category,
    cast(item.quantity ->> '$' as integer)     as quantity,     -- "2" or 2 -> 2
    cast(item.unit_price as decimal(10, 2))    as unit_price
from items
  );
