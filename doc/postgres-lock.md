# Postgres - борьба с нежданными блокировками

## Проверяем зависшие процессы и блокировки

Откройте в pgAdmin новое окно запросов (Query Tool) к этой же базе данных (если оно откроется) или подключитесь через терминал прямо внутри контейнера:

```Bash
docker exec -it postgres_learn psql -U postgres -d shop_db_hw3_1
```

Выполните запрос, чтобы увидеть, какие процессы сейчас выполняются и что они ждут:

```SQL
SELECT pid, age(clock_timestamp(), query_start), state, query, wait_event_type, wait_event
FROM pg_stat_activity
WHERE state != 'idle';
```

Если вы увидите там свой SELECT со статусом ожидания (wait_event_type = 'Lock'), значит, его точно что-то блокирует.

## Убиваем зависшие транзакции

Чтобы принудительно прервать все транзакции, которые держат блокировки (кроме вашей текущей сессии), выполните прямо в psql/pgAdmin:

```SQL
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE pid <> pg_backend_pid()
  AND (state = 'idle in transaction' OR age(clock_timestamp(), query_start) > interval '5 minutes');
```

## Самый быстрый "костыль"

Если не хочется разбираться в блокировках, просто перезапустите контейнер. Это гарантированно сбросит все активные сессии и снимет блокировки:

```Bash
docker restart postgres_learn
```

После этого зайдите в pgAdmin и попробуйте выполнить запрос снова — он должен отработать мгновенно.
