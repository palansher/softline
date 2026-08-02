--- Выполнять ВНУТРИ новой базы


-- Настройка прав (теперь выполняется строго внутри нужной базы)
GRANT ALL ON SCHEMA public TO shop_admin;
ALTER SCHEMA public OWNER TO shop_admin;
