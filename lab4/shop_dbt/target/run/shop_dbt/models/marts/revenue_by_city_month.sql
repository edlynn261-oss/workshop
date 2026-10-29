
  
    
    

    create  table
      "shop"."main"."revenue_by_city_month__dbt_tmp"
  
    as (
      -- The report the shop owner asked for
select
    c.city,
    f.order_month,
    count(distinct f.order_id)  as orders,
    sum(f.line_total)           as revenue
from "shop"."main"."fct_order_items" as f
join "shop"."main"."dim_customers"   as c on c.customer_id = f.customer_id
group by c.city, f.order_month
order by c.city, f.order_month
    );
  
  