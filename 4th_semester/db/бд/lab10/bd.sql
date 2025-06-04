CREATE SCHEMA library;

CREATE TABLE library.readers (
    id SERIAL PRIMARY KEY,
    last_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    CONSTRAINT check_last_name CHECK (TRIM(last_name) <> ''),
    CONSTRAINT check_first_name CHECK (TRIM(first_name) <> ''),
    CONSTRAINT check_middle_name CHECK (middle_name IS NULL OR TRIM(middle_name) <> '')
);
COMMENT ON TABLE library.readers IS 'Таблица читателей библиотечной системы';
COMMENT ON COLUMN library.readers.last_name IS 'Фамилия читателя';
COMMENT ON COLUMN library.readers.first_name IS 'Имя читателя';
COMMENT ON COLUMN library.readers.middle_name IS 'Отчество читателя (опционально)';

CREATE TABLE library.tickets (
    id SERIAL PRIMARY KEY,
    reader_id INTEGER NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMPTZ NOT NULL,
    FOREIGN KEY (reader_id) REFERENCES library.readers(id) ON DELETE CASCADE,
    CONSTRAINT check_created_at CHECK (created_at <= expires_at)
);
COMMENT ON TABLE library.tickets IS 'Таблица читательских билетов';
COMMENT ON COLUMN library.tickets.reader_id IS 'Идентификатор читателя';
COMMENT ON COLUMN library.tickets.created_at IS 'Дата создания билета';
COMMENT ON COLUMN library.tickets.expires_at IS 'Дата истечения срока действия билета';

CREATE TABLE library.books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL UNIQUE,
    CONSTRAINT check_title CHECK (TRIM(title) <> '')
);
COMMENT ON TABLE library.books IS 'Таблица книг с их заголовками';
COMMENT ON COLUMN library.books.title IS 'Название книги';

CREATE TABLE library.genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL UNIQUE,
    description TEXT,
    CONSTRAINT check_name CHECK (TRIM(name) <> ''),
    CONSTRAINT check_description CHECK (description IS NULL OR TRIM(description) <> '')
);
COMMENT ON TABLE library.genres IS 'Таблица книжных жанров';
COMMENT ON COLUMN library.genres.name IS 'Название жанра';
COMMENT ON COLUMN library.genres.description IS 'Описание жанра (опционально)';

CREATE TABLE library.book_genres (
    book_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    PRIMARY KEY (book_id, genre_id),
    FOREIGN KEY (book_id) REFERENCES library.books(id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES library.genres(id) ON DELETE CASCADE
);
COMMENT ON TABLE library.book_genres IS 'Таблица связей между книгами и жанрами';

CREATE TABLE library.authors (
    id SERIAL PRIMARY KEY,
    last_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    born_at DATE,
    CONSTRAINT check_last_name CHECK (TRIM(last_name) <> ''),
    CONSTRAINT check_first_name CHECK (TRIM(first_name) <> ''),
    CONSTRAINT check_middle_name CHECK (middle_name IS NULL OR TRIM(middle_name) <> ''),
    CONSTRAINT check_born_at CHECK (born_at IS NULL OR born_at <= CURRENT_DATE)
);
COMMENT ON TABLE library.authors IS 'Таблица авторов книг';
COMMENT ON COLUMN library.authors.last_name IS 'Фамилия автора';
COMMENT ON COLUMN library.authors.first_name IS 'Имя автора';
COMMENT ON COLUMN library.authors.middle_name IS 'Отчество автора (опционально)';
COMMENT ON COLUMN library.authors.born_at IS 'Дата рождения автора (опционально)';

CREATE TABLE library.book_authors (
    book_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES library.books(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES library.authors(id) ON DELETE CASCADE
);
COMMENT ON TABLE library.book_authors IS 'Таблица связей между книгами и авторами';

CREATE TABLE library.book_loans (
    id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL,
    ticket_id INTEGER NOT NULL,
    picked_at TIMESTAMPTZ NOT NULL,
    pick_days INT NOT NULL,
    returned_at TIMESTAMPTZ,
    UNIQUE (book_id, ticket_id, picked_at),
    FOREIGN KEY (book_id) REFERENCES library.books(id) ON DELETE CASCADE,
    FOREIGN KEY (ticket_id) REFERENCES library.tickets(id) ON DELETE CASCADE,
    CONSTRAINT check_picked_at CHECK (picked_at <= CURRENT_TIMESTAMP),
    CONSTRAINT check_pick_days CHECK (pick_days > 0),
    CONSTRAINT check_returned_at CHECK (returned_at IS NULL OR returned_at >= picked_at)
);
COMMENT ON TABLE library.book_loans IS 'Таблица выдачи книг по читательским билетам';
COMMENT ON COLUMN library.book_loans.book_id IS 'Идентификатор книги';
COMMENT ON COLUMN library.book_loans.ticket_id IS 'Идентификатор билета';
COMMENT ON COLUMN library.book_loans.picked_at IS 'Дата выдачи книги';
COMMENT ON COLUMN library.book_loans.pick_days IS 'Срок выдачи (в днях)';
COMMENT ON COLUMN library.book_loans.returned_at IS 'Дата возврата книги (опционально)';

-- Индексы для оптимизации
CREATE INDEX idx_tickets_reader_id ON library.tickets(reader_id);
CREATE INDEX idx_book_genres_book_id ON library.book_genres(book_id);
CREATE INDEX idx_book_authors_book_id ON library.book_authors(book_id);
CREATE INDEX idx_book_loans_ticket_id ON library.book_loans(ticket_id);
CREATE INDEX idx_book_loans_book_id ON library.book_loans(book_id);

-- Триггер для проверки выдачи книги на срок, превышающий срок действия читательского билета
CREATE FUNCTION check_loan_expiry() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.picked_at + NEW.pick_days * INTERVAL '1 day' > (
        SELECT expires_at FROM library.tickets WHERE id = NEW.ticket_id
    ) THEN
        RAISE EXCEPTION 'Период выдачи книги превышает срок действия читательского билета';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_check_loan_expiry
BEFORE INSERT OR UPDATE ON library.book_loans
FOR EACH ROW EXECUTE FUNCTION check_loan_expiry();
