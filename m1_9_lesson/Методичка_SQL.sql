-- Создание таблицы
CREATE TABLE persons (
    person_id serial primary key,
    fio varchar(20) NOT NULL,
    salary numeric
)

-- Удаление таблицы
DROP TABLE persons

--Заполнение таблицы информацией
INSERT INTO persons(fio,salary) VALUES('Иванов',100000),('Петров',130000),('Сидоров',110000)

--Получение данных из таблицы
SELECT * FROM persons WHERE salary > 100000 ORDER BY salary DESC

-- Обновление данных (даем премию всем 10%)

UPDATE persons SET salary=salary * 1.1

-- Удаление по фильтру
DELETE FROM persons WHERE fio='Иванов'

TRUNCATE TABLE persons

Получение общих данных из двух таблиц
SELECT m1.title,m2.title FROM marks m1 JOIN models m2 ON m1.mark_id=m2.mark_id