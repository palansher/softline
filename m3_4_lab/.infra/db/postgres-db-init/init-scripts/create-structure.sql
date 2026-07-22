
DROP TABLE person;

CREATE TABLE person (
    id_person SERIAL PRIMARY KEY,
    fio VARCHAR(100) NOT NULL,
    salary DECIMAL(10, 2) NOT NULL,
    department VARCHAR(50),
    hire_date DATE DEFAULT CURRENT_DATE
);

-- TRUNCATE TABLE person;

-- Наполнение таблицы тестовыми данными
INSERT INTO person (fio, salary, department, hire_date) VALUES
('Иванов И.И.', 50000.00, 'IT', '2020-01-15'),
('Петров П.П.', 45000.00, 'Бухгалтерия', '2019-03-20'),
('Сидоров С.С.', 55000.00, 'IT', '2021-06-10'),
('Кузнецова Е.В.', 48000.00, 'HR', '2018-11-05'),
('Смирнов А.А.', 52000.00, 'Маркетинг', '2022-02-28'),
('Васильева О.К.', 47000.00, 'Бухгалтерия', '2020-09-12'),
('Николаев Д.С.', 51000.00, 'IT', '2019-07-22'),
('Орлова М.И.', 49000.00, 'HR', '2021-04-18'),
('Федоров В.П.', 53000.00, 'Маркетинг', '2018-12-03'),
('Жукова Л.Н.', 46000.00, 'Бухгалтерия', '2022-01-08') RETURNING *;

-- Проверка данных
-- SELECT * FROM person ORDER BY id_person;
