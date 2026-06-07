-- Создание таблицы
CREATE TABLE persons (
    person_id serial primary key,
    fio varchar(20) NOT NULL,
    salary numeric
)