-- 1. Создаем/обновляем пользователя
CREATE USER shop_admin WITH PASSWORD 'admin';
ALTER USER shop_admin WITH PASSWORD 'admin';

-- 2. Создаем базу (без блока DO)
-- Если она уже есть при случайном ручном запуске, Postgres просто выдаст варнинг/ошибку в лог, но пойдет дальше
CREATE DATABASE shop_db_hw3_1;

-- 3. Навешиваем права на саму базу
GRANT ALL PRIVILEGES ON DATABASE shop_db_hw3_1 TO shop_admin;

-- 4. Переключаемся на созданную базу и даем права на работу со схемами
\c shop_db_hw3_1
GRANT ALL ON SCHEMA public TO shop_admin;
