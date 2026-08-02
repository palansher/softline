--- для cli утилиты.

/* cd /home/vp/code/learn-python/m3_2hw/.infra/postgres-db-init/init-scripts
docker exec -i postgres-learn-py psql -U postgres -d postgres < init-cli.sql
*/

-- ============================================================================
-- Работаем в системной базе (создаем пользователя и саму БД)
-- ============================================================================

-- Безопасно создаем пользователя, если его еще нет
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

-- Безопасно создаем базу данных, если её еще нет
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'shop_db_hw3_2') THEN
        PERFORM dblink_exec('dbname=' || current_database(), 'CREATE DATABASE shop_db_hw3_2');
    END IF;
EXCEPTION 
    -- Если dblink не настроен, используем стандартный фолбек. 
    -- Из DO-блока нельзя напрямую вызвать CREATE DATABASE, поэтому если база есть,
    -- обычный вызов ниже просто выдаст варнинг, но не остановит скрипт.
    WHEN OTHERS THEN NULL;
END
$$;

-- На случай если блок выше пропущен, вызываем обычный скрипт (ошибка тут не прервет psql)
-- Если запускаете в pgAdmin/DBeaver, это самый чистый путь
CREATE DATABASE shop_db_hw3_2;

-- Выдаем права на саму базу данных (эту команду можно выполнять повторенно)
GRANT ALL PRIVILEGES ON DATABASE shop_db_hw3_2 TO shop_admin;


-- ============================================================================
-- Переключаемся в созданную базу (Раскомментируйте для утилиты psql)
-- ============================================================================
\c shop_db_hw3_2


-- ============================================================================
-- Настройка прав ВНУТРИ новой базы shop_db_hw3_2
-- ============================================================================

-- Даем права на схему public именно в этой базе (безопасно для повторов)
GRANT ALL ON SCHEMA public TO shop_admin;

-- Передаем владение схемой public админу
ALTER SCHEMA public OWNER TO shop_admin;
