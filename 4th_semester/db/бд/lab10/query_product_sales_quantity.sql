SELECT
    p.name AS product_name,
    SUM(oi.quantity) AS total_sold_quantity
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.name
ORDER BY total_sold_quantity DESC;