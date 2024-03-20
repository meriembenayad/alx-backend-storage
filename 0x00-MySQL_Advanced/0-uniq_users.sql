-- 0. We are all unique!: creates a table users

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) Not NULL UNIQUE,
    name VARCHAR(255)
);
