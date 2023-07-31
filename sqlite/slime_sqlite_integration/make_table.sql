CREATE TABLE table3 (
    person_id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR(50)
);

INSERT INTO table3(name)
VALUES
    ('john'),
    ('bill'),
    ('joe')
;

SELECT * FROM table3;
