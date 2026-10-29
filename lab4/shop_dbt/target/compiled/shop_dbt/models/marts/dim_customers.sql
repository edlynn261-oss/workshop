-- One row per customer
select distinct
    customer_id,
    customer_name,
    city
from "shop"."main"."stg_orders"