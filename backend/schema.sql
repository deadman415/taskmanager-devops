- Run this in MySQL Workbench first!

CREATE DATABASE IF NOT EXISTS taskmanager;
USE taskmanager;

CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status ENUM('pending', 'completed') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample data (optional)
INSERT INTO tasks (title, description, status) VALUES
('Set up Flask server', 'Install Flask and configure routes', 'completed'),
('Connect MySQL database', 'Use mysql-connector-python to link DB', 'pending'),
('Build React frontend', 'Create UI with fetch API calls', 'pending');
