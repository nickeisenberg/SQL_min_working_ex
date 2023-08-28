-- command line client requires this delimiter setting

DROP TABLE IF EXISTS trans;
create table trans (
    id Int primary key auto_increment,
    item varchar(20),
    action Float,
    no_units Float,
    at_price Float
);
DROP TABLE IF EXISTS invetory;
create table invetory (
    item varchar(20) primary key,
    inv Int,
    cost_basis Float,
    current_value Float,
    realized_profit Float,
);

delimiter |
create trigger
    update_inv
after insert on
    trans
for each row
begin
    INSERT INTO
        invetory
    values 
        (
            new.item, 
            new.no_units * new.action, 
            new.at_price * inv,
            -1 * new.at_price * new.no_units * new.action,
            0
        ) 
    ON DUPLICATE KEY UPDATE    
        inv = inv + new.no_units * new.action,
        profit = profit - (new.no_units * new.at_price * new.action),
        current_value = new.at_price * inv,
        gain = 0;
end;
|
delimiter ;

insert into trans (item, action, no_units, at_price)
values 
    ('car', 1, 2, 50),
    ('car', -1, 1, 100),
    ('boat', 1, 2, 50),
    ('boat', -1, 2, 25)
;

select * from invetory;

select * from trans;


select cte.item, 100 * (profit + current_value) / cte.total as total from invetory
left join (
    select item, sum(no_units * at_price) as total
    from trans
    where action = 1
    group by item
) as cte
on invetory.item = cte.item
;
