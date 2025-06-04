SELECT
    oi.order_item_id,
    p.name AS product_name,
    oi.quantity,
    oi.price_per_item,
    (oi.quantity * oi.price_per_item) AS line_item_total
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
WHERE oi.order_id = 1;