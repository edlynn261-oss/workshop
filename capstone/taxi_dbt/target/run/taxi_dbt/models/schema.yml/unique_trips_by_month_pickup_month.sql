
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    pickup_month as unique_field,
    count(*) as n_records

from "taxi"."main"."trips_by_month"
where pickup_month is not null
group by pickup_month
having count(*) > 1



  
  
      
    ) dbt_internal_test