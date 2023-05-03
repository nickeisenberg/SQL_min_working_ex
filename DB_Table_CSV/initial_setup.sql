-- Active: 1681858888208@@test-server-azure.mysql.database.azure.com@3306
DROP DATABASE IF EXISTS person_info;
CREATE DATABASE person_info;
DROP TABLE IF EXISTS person_info.contact;
CREATE Table person_info.contact (
    person_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    address VARCHAR(255) DEFAULT NULL
);
INSERT INTO person_info.contact (name, phone_number, address)
VALUES
    ('jon', '702-555-5555', NULL),
    ('tim', '702-555-1212', '2212 Park Ave');

DROP TABLE IF EXISTS person_info.job;
CREATE Table person_info.job (
    person_id INT AUTO_INCREMENT PRIMARY KEY,
    job_title VARCHAR(255) NOT NULL
);
INSERT INTO person_info.job (job_title)
VALUES
    ('Doctor'),
    ('Chef');
