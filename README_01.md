CREATE DATABASE budget_tracker_1;
USE budget_tracker_1;

CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    amount FLOAT,
    category VARCHAR(100),
    type VARCHAR(20),
    month VARCHAR(10)
);
