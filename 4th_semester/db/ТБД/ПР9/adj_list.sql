-- Создание базы данных ais (выполняется один раз администратором)
-- Предполагается, что база уже создана командой `createdb ais` пользователем postgres.
-- Если базы нет, нужно выполнить эту команду отдельно в shell:
-- createdb ais

-- Подключение к базе данных ais (не нужно в файле, так как задаётся в psql -d ais)

-- Таблица "Персонал" (Personnel)
DROP TABLE IF EXISTS Personnel CASCADE;

CREATE TABLE Personnel (
    emp_nbr INTEGER NOT NULL PRIMARY KEY,    -- Код сотрудника
    emp_name VARCHAR(20) NOT NULL,           -- Имя сотрудника
    emp_addr VARCHAR(50) NOT NULL,           -- Адрес сотрудника
    birth_date DATE NOT NULL                 -- Дата рождения
);

-- Заполнение таблицы Personnel
INSERT INTO Personnel VALUES
    (0, 'вакансия', '', '2014-05-19'),
    (1, 'Иван', 'ул. Любителей языка С', '1962-12-01'),
    (2, 'Петр', 'ул. UNIX гуру', '1965-10-21'),
    (3, 'Антон', 'ул. Ассемблерная', '1964-04-17'),
    (4, 'Захар', 'ул. им. СУБД PostgreSQL', '1963-09-27'),
    (5, 'Ирина', 'просп. Программистов', '1968-05-12'),
    (6, 'Анна', 'пер. Перловый', '1969-03-20'),
    (7, 'Андрей', 'пл. Баз данных', '1945-11-07'),
    (8, 'Николай', 'наб. ОС Linux', '1944-12-01');

-- Таблица "Организационная структура" (Org_chart)
DROP TABLE IF EXISTS Org_chart CASCADE;

CREATE TABLE Org_chart (
    job_title VARCHAR(30) NOT NULL PRIMARY KEY,  -- Наименование должности
    emp_nbr INTEGER DEFAULT 0 NOT NULL          -- Код сотрудника (0 = вакансия)
        REFERENCES Personnel(emp_nbr)
        ON DELETE SET DEFAULT
        ON UPDATE CASCADE
        DEFERRABLE,
    boss_emp_nbr INTEGER DEFAULT 0              -- Код начальника (NULL для главы)
        REFERENCES Personnel(emp_nbr)
        ON DELETE SET DEFAULT
        ON UPDATE CASCADE
        DEFERRABLE,
    salary DECIMAL(12,4) NOT NULL CHECK (salary >= 0.00), -- Зарплата
    CHECK ((boss_emp_nbr <> emp_nbr) OR (boss_emp_nbr = 0 AND emp_nbr = 0)),
    FOREIGN KEY (boss_emp_nbr) REFERENCES Org_chart(emp_nbr)
        ON DELETE SET DEFAULT
        ON UPDATE CASCADE
        DEFERRABLE,
    UNIQUE (emp_nbr)  -- Ограничение уникальности для emp_nbr
);

-- Заполнение таблицы Org_chart
INSERT INTO Org_chart VALUES
    ('Президент', 1, NULL, 1000.00),
    ('Вице-президент 1', 2, 1, 900.00),
    ('Вице-президент 2', 3, 1, 800.00),
    ('Архитектор', 4, 3, 700.00),
    ('Ведущий программист', 5, 3, 600.00),
    ('Программист C', 6, 3, 500.00),
    ('Программист Perl', 7, 5, 450.00),
    ('Оператор', 8, 5, 400.00);

-- Триггерная функция для проверки структуры Org_chart
CREATE OR REPLACE FUNCTION check_org_chart() RETURNS trigger AS $$
BEGIN
    IF (SELECT COUNT(*) FROM Org_chart) - 1 < (SELECT COUNT(boss_emp_nbr) FROM Org_chart) THEN
        RAISE EXCEPTION 'Bad orgchart structure';
    ELSE
        IF (TG_OP = 'DELETE') THEN
            RETURN OLD;
        ELSIF (TG_OP = 'UPDATE') THEN
            RETURN NEW;
        ELSIF (TG_OP = 'INSERT') THEN
            RETURN NEW;
        END IF;
        RETURN NULL;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Создание триггера
DROP TRIGGER IF EXISTS check_org_chart ON Org_chart;

CREATE TRIGGER check_org_chart
AFTER INSERT OR UPDATE OR DELETE ON Org_chart
FOR EACH ROW EXECUTE PROCEDURE check_org_chart();

-- Функция проверки дерева на циклы
CREATE OR REPLACE FUNCTION tree_test() RETURNS CHAR(6) AS $$
BEGIN
    CREATE TEMP TABLE Tree ON COMMIT DROP AS
    SELECT emp_nbr, boss_emp_nbr FROM Org_chart;
    
    WHILE (SELECT COUNT(*) FROM Tree) - 1 = (SELECT COUNT(boss_emp_nbr) FROM Tree)
    LOOP
        DELETE FROM Tree
        WHERE Tree.emp_nbr NOT IN (SELECT T2.boss_emp_nbr FROM Tree AS T2 WHERE T2.boss_emp_nbr IS NOT NULL);
    END LOOP;
    
    IF NOT EXISTS (SELECT * FROM Tree) THEN
        RETURN ('Tree');
    ELSE
        RETURN ('Cycles');
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Функция обхода дерева снизу вверх (Вариант 1)
CREATE OR REPLACE FUNCTION up_tree_traversal(IN current_emp_nbr INTEGER)
RETURNS TABLE (emp_nbr INTEGER, boss_emp_nbr INTEGER) AS $$
BEGIN
    WHILE EXISTS (SELECT * FROM Org_chart AS O WHERE O.emp_nbr = current_emp_nbr)
    LOOP
        RETURN QUERY SELECT O.emp_nbr, O.boss_emp_nbr
        FROM Org_chart AS O
        WHERE O.emp_nbr = current_emp_nbr;
        
        current_emp_nbr = (SELECT O.boss_emp_nbr FROM Org_chart AS O WHERE O.emp_nbr = current_emp_nbr);
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Функция обхода дерева снизу вверх (Вариант 2)
CREATE OR REPLACE FUNCTION up_tree_traversal2(IN current_emp_nbr INTEGER)
RETURNS SETOF RECORD AS $$
DECLARE
    rec RECORD;
BEGIN
    WHILE EXISTS (SELECT * FROM Org_chart AS O WHERE O.emp_nbr = current_emp_nbr)
    LOOP
        SELECT O.emp_nbr, O.boss_emp_nbr INTO rec
        FROM Org_chart AS O
        WHERE O.emp_nbr = current_emp_nbr;
        
        RETURN NEXT rec;
        
        current_emp_nbr = (SELECT O.boss_emp_nbr FROM Org_chart AS O WHERE O.emp_nbr = current_emp_nbr);
    END LOOP;
    RETURN;
END;
$$ LANGUAGE plpgsql;

-- Функция удаления поддерева
CREATE OR REPLACE FUNCTION delete_subtree(IN dead_guy INTEGER) RETURNS VOID AS $$
BEGIN
    CREATE TEMP SEQUENCE New_emp_nbr START WITH 1;
    CREATE TEMP TABLE Working_table (emp_nbr INTEGER NOT NULL) ON COMMIT DROP;
    
    SET CONSTRAINTS org_chart_emp_nbr_fkey, org_chart_boss_emp_nbr_fkey, org_chart_boss_emp_nbr_fkey1 DEFERRED;
    
    UPDATE Org_chart
    SET emp_nbr = CASE WHEN emp_nbr = dead_guy THEN nextval('New_emp_nbr') * -1 ELSE emp_nbr END,
        boss_emp_nbr = CASE WHEN boss_emp_nbr = dead_guy THEN nextval('New_emp_nbr') * -1 ELSE boss_emp_nbr END
    WHERE dead_guy IN (emp_nbr, boss_emp_nbr);
    
    WHILE EXISTS (SELECT * FROM Org_chart WHERE boss_emp_nbr < 0 AND emp_nbr >= 0)
    LOOP
        DELETE FROM Working_table;
        INSERT INTO Working_table
        SELECT emp_nbr FROM Org_chart WHERE boss_emp_nbr < 0;
        
        UPDATE Org_chart
        SET emp_nbr = nextval('New_emp_nbr') * -1
        WHERE emp_nbr IN (SELECT emp_nbr FROM Working_table);
        
        UPDATE Org_chart
        SET boss_emp_nbr = nextval('New_emp_nbr') * -1
        WHERE boss_emp_nbr IN (SELECT emp_nbr FROM Working_table);
    END LOOP;
    
    DELETE FROM Org_chart WHERE emp_nbr < 0;
    
    SET CONSTRAINTS ALL IMMEDIATE;
    DROP SEQUENCE New_emp_nbr;
END;
$$ LANGUAGE plpgsql;

-- Представление для реконструирования организационной структуры
DROP VIEW IF EXISTS Personnel_org_chart CASCADE;

CREATE VIEW Personnel_org_chart (emp_nbr, emp, boss_emp_nbr, boss) AS
SELECT O1.emp_nbr, E1.emp_name, O1.boss_emp_nbr, B1.emp_name
FROM (Org_chart AS O1 LEFT OUTER JOIN Personnel AS B1 ON O1.boss_emp_nbr = B1.emp_nbr), Personnel AS E1
WHERE O1.emp_nbr = E1.emp_nbr;

-- Представление для построения путей сверху вниз (4 уровня)
DROP VIEW IF EXISTS Create_paths;

CREATE VIEW Create_paths (level1, level2, level3, level4) AS
SELECT O1.emp AS e1, O2.emp AS e2, O3.emp AS e3, O4.emp AS e4
FROM Personnel_org_chart AS O1
LEFT OUTER JOIN Personnel_org_chart AS O2 ON O1.emp = O2.boss
LEFT OUTER JOIN Personnel_org_chart AS O3 ON O2.emp = O3.boss
LEFT OUTER JOIN Personnel_org_chart AS O4 ON O3.emp = O4.boss
WHERE O1.emp = 'Иван';

-- Функция удаления элемента и продвижения подчинённых вверх
CREATE OR REPLACE FUNCTION delete_and_promote_subtree(IN dead_guy INTEGER) RETURNS VOID AS $$
BEGIN
    UPDATE Org_chart
    SET boss_emp_nbr = (SELECT boss_emp_nbr FROM Org_chart WHERE emp_nbr = dead_guy)
    WHERE boss_emp_nbr = dead_guy;
    
    DELETE FROM Org_chart WHERE emp_nbr = dead_guy;
END;
$$ LANGUAGE plpgsql;