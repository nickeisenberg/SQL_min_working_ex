-- command line client requires this delimiter setting

DROP TABLE IF EXISTS table0;
create table table0 (
    id Int primary key auto_increment,
    item varchar(10),
    action float,
    col0 Float,
    col1 Float
);
DROP TABLE IF EXISTS table1;
create table table1 (
    item varchar(10) primary key,
    sum_col Float
);

delimiter |
create trigger
    update_table1
after insert on
    table0 
for each row
begin
    INSERT INTO
        table1
    values 
        (
            new.item,
            new.col0 + new.col1
        ) 
    ON DUPLICATE KEY UPDATE    
        col0 = new
        col1 = profit - (new.no_units * new.at_price * new.action),
        current_value = new.at_price * inv,
        gain = select f.total from (
            select 
                cte.item, 
                100 * (profit + current_value) / cte.total as total 
            from invetory
            left join (
                select item, sum(no_units * at_price) as total
                from trans
                where action = 1
                group by item
            ) as cte
            on invetory.item = cte.item) as f where f.item = new.item;
end;
|
delimiter ;

insert into trans (item, action, no_units, at_price)
values 
    ('car', 1, 2, 50),
    ('boat', 1, 2, 50),
    ('car', -1, 1, 100),
    ('boat', -1, 2, 25)
;




select * from invetory;

select cte.item, 100 * (profit + current_value) / cte.total as total from invetory
left join (
    select item, sum(no_units * at_price) as total
    from trans
    where action = 1
    group by item
) as cte
on invetory.item = cte.item
;
