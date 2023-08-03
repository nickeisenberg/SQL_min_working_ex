pragma table_info(item_purchased);

select * from item_purchased
limit 2
;

pragma table_info(personal_info);

with cte as (
select * from personal_info
where
    first_name = 'Roberto'
or
    first_name = 'Carlos'
)
SELECT cte.first_name, item_purchased.item
    FROM cte
    LEFT JOIN item_purchased
    ON cte.id = item_purchased.id;
;

