
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select pickup_month
from "taxi"."main"."trips_by_month"
where pickup_month is null



  
  
      
    ) dbt_internal_test