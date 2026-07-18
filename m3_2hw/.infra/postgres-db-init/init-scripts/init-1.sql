--- подключившись к дефолтной базе postgres (или любой другой существующей)
--- Выполнять под пользователем postgres

-- 1. создаем пользователя
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'shop_admin') THEN
        CREATE USER shop_admin WITH PASSWORD 'admin';
    ELSE
        -- Если пользователь есть, просто обновляем ему пароль на случай изменений
        ALTER USER shop_admin WITH PASSWORD 'admin';
    END IF;
END
$$;

-- 2. Создаем базу данных
-- В IDE блок DO с dblink может не сработать без расширения, поэтому пишем чистый SQL.
-- Если база уже есть, IDE покажет ошибку/варнинг, но это нормально — переходите к Шагу 2.
CREATE DATABASE shop_db_hw3_2;

-- 3. Даем права на базу
GRANT ALL PRIVILEGES ON DATABASE shop_db_hw3_2 TO shop_admin;
