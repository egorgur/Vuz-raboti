SELECT
    o.order_id,
    o.order_date,
    o.total_amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE c.email = 'ivan.ivanov@example.com'
ORDER BY o.order_date;