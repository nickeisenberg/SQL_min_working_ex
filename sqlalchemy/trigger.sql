delimiter |
create trigger
    update_inv
after insert on
    trans
for each row
begin
    INSERT INTO
        inv
    values 
        (new.item, new.no_units * new.action)
    ON DUPLICATE KEY UPDATE    
        inv = inv + new.no_units * new.action;
end;
|

delimiter ;

select * from trans;
select * from inv;

insert into trans (item, action, no_units)
values 
    ('car', 1, 5),
    ('boat', 1, 2),
    ('car', -1, 1),
    ('boat', 1, 2),
    ('car', -1, 1),
    ('bike', 1, 2)
;

select * from trans;

select * from inv;
