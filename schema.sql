CREATE TABLE users(id int auto_increment PRIMARY KEY,
username VARCHAR(100),password VARCHAR(100));

CREATE TABLE tasks(
id INT auto_increment PRIMARY KEY,
title VARCHAR(30),
description TEXT,
priority VARCHAR(80),
status VARCHAR(50),
created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);