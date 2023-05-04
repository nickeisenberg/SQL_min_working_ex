DROP TABLE IF EXISTS emergency_contact;
CREATE TABLE emergency_contact (
    person_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    number VARCHAR(20) NOT NULL,
    relation VARCHAR(100) DEFAULT NULL
);
LOAD DATA LOCAL
    INFILE '/Users/nickeisenberg/GitRepos/SQL_Notebook/DB_Table_CSV/em_cont.csv'
    INTO TABLE emergency_contact
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    LINES TERMINATED BY "\n"
    IGNORE 1 ROWS
    (name, number, relation);
