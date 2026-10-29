
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select zone_id
from "taxi"."main"."stg_zones"
where zone_id is null



  
  
      
    ) dbt_internal_test