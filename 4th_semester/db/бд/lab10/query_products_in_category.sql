SELECT
    p.name,
    p.price,
    p.stock
FROM products p
JOIN categories cat ON p.category_id = cat.category_id
WHERE cat.name = 'Электроника'
ORDER BY p.price ASC;