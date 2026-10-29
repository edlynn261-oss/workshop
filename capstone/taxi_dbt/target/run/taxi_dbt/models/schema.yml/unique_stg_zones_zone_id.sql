
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    zone_id as unique_field,
    count(*) as n_records

from "taxi"."main"."stg_zones"
where zone_id is not null
group by zone_id
having count(*) > 1



  
  
      
    ) dbt_internal_test