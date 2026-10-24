-- WEEK 2 ASSESSMENT: TASK 1 - SQL ANALYSIS

-- SETUP 1: Create customers table
CREATE TABLE customers (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL
);

-- SETUP 2: Create orders table
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(id),
    amount NUMERIC(10,2) NOT NULL,
    ordered_at DATE NOT NULL
);

-- SETUP 3: Create products table
CREATE TABLE products (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    attrs JSONB
);

-- SETUP 4: Insert customers
INSERT INTO customers VALUES
(1, 'Arun', 'Chennai'),
(2, 'Priya', 'Mumbai'),
(3, 'Rahul', 'Chennai'),
(4, 'Divya', 'Bangalore'),
(5, 'Kumar', 'Coimbatore');

-- SETUP 5: Insert orders
INSERT INTO orders VALUES
(101, 1, 700, '2026-01-05'),
(102, 1, 600, '2026-02-10'),
(103, 2, 300, '2026-01-20'),
(104, 2, 800, '2026-02-15'),
(105, 3, 1200, '2026-03-01'),
(106, 3, 500, '2026-03-10'),
(107, 4, 900, '2026-03-15'),
(108, 4, 400, '2026-04-01'),
(109, 1, 200, '2026-04-05');

-- SETUP 6: Insert products
INSERT INTO products VALUES
(1, 'Laptop A', '{"brand":"Dell","ram":16}'),
(2, 'Laptop B', '{"brand":"HP","ram":8}');


-- QUERY 1: Total sales per customer above 1000
SELECT c.id, c.name, SUM(o.amount) AS total_sales
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name
HAVING SUM(o.amount) > 1000
ORDER BY total_sales DESC;


-- QUERY 2: Customers who have never ordered
SELECT c.id, c.name, c.city
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;


-- QUERY 3: Top customer per city using CTE
WITH customer_sales AS (
    SELECT c.id, c.name, c.city,
           SUM(o.amount) AS total_sales
    FROM customers c
    JOIN orders o ON c.id = o.customer_id
    GROUP BY c.id, c.name, c.city
),
ranked_customers AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY city
               ORDER BY total_sales DESC
           ) AS rn
    FROM customer_sales
)
SELECT id, name, city, total_sales
FROM ranked_customers
WHERE rn = 1
ORDER BY city;


-- QUERY 4: Rank orders and show previous order amount
SELECT customer_id,
       id AS order_id,
       amount,
       ROW_NUMBER() OVER (
           PARTITION BY customer_id
           ORDER BY amount DESC
       ) AS order_rank,
       LAG(amount) OVER (
           PARTITION BY customer_id
           ORDER BY ordered_at
       ) AS previous_order_amount
FROM orders
ORDER BY customer_id, ordered_at;


-- QUERY 5A: Find Dell products using JSONB
SELECT *
FROM products
WHERE attrs @> '{"brand": "Dell"}';


-- QUERY 5B: Extract RAM from JSONB
SELECT name, attrs ->> 'ram' AS ram
FROM products;