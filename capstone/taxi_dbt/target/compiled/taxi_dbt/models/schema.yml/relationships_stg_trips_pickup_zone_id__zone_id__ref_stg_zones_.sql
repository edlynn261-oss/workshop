
    
    

with child as (
    select pickup_zone_id as from_field
    from "taxi"."main"."stg_trips"
    where pickup_zone_id is not null
),

parent as (
    select zone_id as to_field
    from "taxi"."main"."stg_zones"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


