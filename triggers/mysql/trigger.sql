-- command line client requires this delimiter setting

DROP TABLE IF EXISTS trans;
create table trans (
    id Int primary key auto_increment,
    item varchar(20),
    trans_type Float,  -- 1 for buy and -1 for short
    action Float,  -- 1 for buy and -1 for sell
    no_units Float,
    at_price Float
);
DROP TABLE IF EXISTS inventory;
create table inventory (
    item varchar(20) primary key,
    inv Int,
    cost_basis Float,
    current_value Float,
    breakeven Float,
    realized_profit Float,
    gain Float
);

delimiter |
create trigger
    update_inv
after insert on
    trans
for each row
begin
if new.trans_type > 0 then
    if new.action > 0 then
        INSERT INTO
            inventory
        values 
            (
                new.item, -- item 
                new.no_units * new.action,  -- inv
                new.at_price * (new.no_units * new.action),  -- cost_basis
                new.at_price * (new.no_units * new.action),  -- current_value
                0,  -- breakeven 
                0,  -- realized_profit
                0  -- gain
            ) 
        ON DUPLICATE KEY UPDATE
            inv = inv + (new.no_units * new.action),
            cost_basis = cost_basis + (new.at_price * new.no_units * new.action),
            current_value = inv * new.at_price,
            breakeven = 0,
            realized_profit = realized_profit,
            gain = 100.0 * (current_value + realized_profit - cost_basis) / cost_basis;
    elseif new.action < 0 then
        UPDATE inventory SET
            inv = inv + (new.no_units * new.action),
            cost_basis = cost_basis,
            current_value = inv * new.at_price,
            breakeven = 0,
            realized_profit = realized_profit + (
                new.no_units * -1.0 * new.action * new.at_price
            ),
            gain = 100.0 * (current_value + realized_profit - cost_basis) / cost_basis;
    end if;
elseif new.trans_type < 0 then
    if new.action < 0 then
        INSERT INTO
            inventory
        values 
            (
                new.item, -- item 
                new.no_units * new.action,  -- inv
                new.at_price * (new.no_units * new.action),  -- cost_basis
                new.at_price * (new.no_units * new.action),  -- current_value
                new.at_price,  -- breakeven
                new.at_price * (new.no_units),  -- realized_profit 
                0  -- gain
            ) 
        ON DUPLICATE KEY UPDATE
            inv = inv + (new.no_units * new.action),
            cost_basis = cost_basis + (new.at_price * new.no_units * new.action),
            current_value = inv * new.at_price,
            breakeven = 0,
            realized_profit = realized_profit + (new.at_price * new.no_units),
            gain = 0;
    elseif new.action > 0 then
        UPDATE inventory SET
            inv = inv + (new.no_units * new.action),
            cost_basis = cost_basis + (new.no_units * new.action * new.at_price),
            current_value = inv * new.at_price,
            breakeven = 0,
            realized_profit = realized_profit 
                - (new.no_units * new.at_price),
            gain = 0;
    end if;
end if;
end;
|
delimiter ;

insert into trans (item, trans_type, action, no_units, at_price)
values 
    ('car', -1, -1, 10, 10),
    ('car', -1, -1, 5, 15)
;

select * from inventory;

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
