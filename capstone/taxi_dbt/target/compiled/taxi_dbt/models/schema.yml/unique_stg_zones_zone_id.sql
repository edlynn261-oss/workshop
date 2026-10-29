
    
    

select
    zone_id as unique_field,
    count(*) as n_records

from "taxi"."main"."stg_zones"
where zone_id is not null
group by zone_id
having count(*) > 1


