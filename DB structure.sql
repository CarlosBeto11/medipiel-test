CREATE DATABASE medipiel;

CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) not null,
    last_name VARCHAR(50) not null
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) not null,
    price DOUBLE PRECISION not null default 0,
    stock INT not null default 0
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers ON DELETE CASCADE ON UPDATE CASCADE,
    status VARCHAR(50) not NULL
);

CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders ON DELETE CASCADE ON UPDATE CASCADE,
    product_id INT REFERENCES products ON DELETE CASCADE ON UPDATE CASCADE,
    quantity INT not NULL default 0
);

CREATE TABLE IF NOT EXISTS inventory_movements (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products ON DELETE CASCADE ON UPDATE CASCADE,
    movement_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    movement_type VARCHAR(50) not null,
    quantity INT not NULL default 0
);


INSERT INTO customers (name, last_name) VALUES ('Carlos Alberto', 'Alvarez Orta');
INSERT INTO customers (name, last_name) VALUES ('Karen Areli', 'Rodriguez Luna');
INSERT INTO customers (name, last_name) VALUES ('Emiliano', 'Alvarez Rodriguez');
INSERT INTO customers (name, last_name) VALUES ('Renata', 'Alvarez Rodriguez');


INSERT INTO products (id, name, price, stock) VALUES (1, 'Macbook Pro 2016', 34943.23, 100);
INSERT INTO products (id, name, price, stock) VALUES (2, 'Laptop DELL inspiron', 19283.53, 100);
INSERT INTO products (id, name, price, stock) VALUES (3, 'Monitor Samsung 24 Pulgadas', 2354.56, 100);
INSERT INTO products (id, name, price, stock) VALUES (4, 'Mouse Perfect Choice', 235.54, 100);
INSERT INTO products (id, name, price, stock) VALUES (5, 'Escritorio esquinero', 4325.43, 100);



INSERT INTO inventory_movements (product_id, movement_type, quantity) VALUES (1, 'receipt', 100);
INSERT INTO inventory_movements (product_id, movement_type, quantity) VALUES (2, 'receipt', 100);
INSERT INTO inventory_movements (product_id, movement_type, quantity) VALUES (3, 'receipt', 100);
INSERT INTO inventory_movements (product_id, movement_type, quantity) VALUES (4, 'receipt', 100);
INSERT INTO inventory_movements (product_id, movement_type, quantity) VALUES (5, 'receipt', 100);








