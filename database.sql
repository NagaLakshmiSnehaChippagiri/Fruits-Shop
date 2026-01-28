CREATE DATABASE fruit_shop;
USE fruit_shop;

CREATE TABLE fruits (
    fruit_id INT AUTO_INCREMENT PRIMARY KEY,
    fruit_name VARCHAR(50) NOT NULL,
    price_per_kg DECIMAL(10,2) NOT NULL,
    stock_kg DECIMAL(10,2) NOT NULL
);

CREATE TABLE bills (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    bill_date DATE NOT NULL,
    total_amount DECIMAL(10,2)
);

CREATE TABLE bill_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    bill_id INT,
    fruit_id INT,
    weight_kg DECIMAL(10,2),
    price_per_kg DECIMAL(10,2),
    item_total DECIMAL(10,2),
    FOREIGN KEY (bill_id) REFERENCES bills(bill_id),
    FOREIGN KEY (fruit_id) REFERENCES fruits(fruit_id)
);

INSERT INTO fruits (fruit_name, price_per_kg, stock_kg) VALUES
('Apple', 120, 10),
('Banana', 40, 15),
('Orange', 60, 12),
('Mango', 150, 8),
('Grapes', 90, 5);

SELECT * FROM fruits;
SELECT * FROM bills;
SELECT * FROM bill_items;
