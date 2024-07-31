db = grocery_store;
table = inventory 

CREATE TABLE inventory (
    product_id VARCHAR(10),
    product_name VARCHAR(255),
    category VARCHAR(50),
    brand VARCHAR(50),
    price VARCHAR(10),
    stock_quantity INT,
    supplier VARCHAR(255),
    expiry_date DATE,
    discount VARCHAR(10),
    location VARCHAR(50),
    image_path VARCHAR(2083),
    ratings INT
);


INSERT INTO inventory (product_id, product_name, category, brand, price, stock_quantity, supplier, expiry_date, discount, location, image_path, ratings)
VALUES
('101', 'Banana', 'Fruits', 'Chiquita', '$0.79', 98, 'Local Farms', '2023-01-10', '5%', 'Aisle 1', 'https://m.media-amazon.com/images/I/51Y0PF2A1bL._SX300_SY300_QL70_ML2_.jpg', 3),
('102', 'Apples', 'Fruits', 'Real', '$0.67', 21, 'Local Farms', '2024-07-29', '3.75%', 'Ohio', 'https://m.media-amazon.com/images/I/51FLUURf1kL._SL1024_.jpg', 5),
('103', 'Oranges', 'Fruits', 'Real', '$0.77', 83, 'Local Farms', '2024-07-31', '8%', 'NYC', 'https://m.media-amazon.com/images/I/71S39VbEUJL._SL1500_.jpg', 2),
('104', 'Butter', 'Dairy', 'Amul', '$0.96', 22, 'Land O\' Lakes', '2024-12-23', '2%', 'NYC', 'https://m.media-amazon.com/images/I/51KrxEKN58L.jpg', 4),
('105', 'Milk', 'Dairy', 'Amul', '$0.70', 50, 'Horizon', '2024-09-13', '1.7%', 'Kolkata', 'https://m.media-amazon.com/images/I/41qYzVy0UwL.jpg', 1),
('106', 'Yogurt', 'Dairy', 'Amul', '$2', 35, 'Yoplait Light \'n Fit Nonfat Vanilla', '2024-09-12', '2%', 'Haldia', 'https://m.media-amazon.com/images/I/61d25yNKxML._SL1500_.jpg', 5);
