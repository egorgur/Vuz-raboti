SELECT DISTINCT
    c.name,
    c.email
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date > '2023-10-26 11:00:00'
ORDER BY c.name;