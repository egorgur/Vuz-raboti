-- Самые популярные кники --
SELECT
    b.title AS "Название книги",
    COUNT(bl.id) AS "Количество выдач"
FROM
    library.books b
LEFT JOIN
    library.book_loans bl ON b.id = bl.book_id
GROUP BY
    b.title
ORDER BY
    COUNT(bl.id) DESC
LIMIT 10;


-- Читатели с просроченными книгами --
SELECT
    CONCAT(r.last_name, ' ', r.first_name) AS "Читатель",
    b.title AS "Книга",
    bl.picked_at + bl.pick_days * INTERVAL '1 day' AS "Срок возврата",
    CURRENT_DATE - (bl.picked_at + bl.pick_days * INTERVAL '1 day') AS "Дней просрочки"
FROM
    library.readers r
JOIN
    library.tickets t ON r.id = t.reader_id
JOIN
    library.book_loans bl ON t.id = bl.ticket_id
JOIN
    library.books b ON bl.book_id = b.id
WHERE
    bl.returned_at IS NULL
    AND bl.picked_at + bl.pick_days * INTERVAL '1 day' < CURRENT_TIMESTAMP
ORDER BY
    "Дней просрочки" DESC;

-- Количество книг по жанрам --
SELECT
    g.name AS "Жанр",
    COUNT(bg.book_id) AS "Количество книг"
FROM
    library.genres g
LEFT JOIN
    library.book_genres bg ON g.id = bg.genre_id
GROUP BY
    g.name
ORDER BY
    COUNT(bg.book_id) DESC;
