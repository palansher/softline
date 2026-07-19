# Postgres database backup restore

- [Postgres database backup restore](#postgres-database-backup-restore)
  - [backup](#backup)
    - [просто бэкап](#просто-бэкап)
    - [вырезает строки с secure метками из файла](#вырезает-строки-с-secure-метками-из-файла)
    - [в zip архиве](#в-zip-архиве)
    - [аргументы](#аргументы)
      - [pg\_dump](#pg_dump)
      - [Docker](#docker)
    - [бэкап ТОЛЬКО структуры](#бэкап-только-структуры)
    - [бэкап ТОЛЬКО данных (без таблиц)](#бэкап-только-данных-без-таблиц)
  - [restore](#restore)

## backup

### просто бэкап

`docker exec postgres-learn-py pg_dump -U postgres -d shop_db_hw3_2 -F p --inserts > app-db-backup_$(date +%Y-%m-%d_%H-%M-%S).sql`

### вырезает строки с secure метками из файла

`docker exec postgres-learn-py pg_dump -U postgres -d shop_db_hw3_2 -F p --inserts | sed '/^\\restrict/d; /^\\unrestrict/d' > app-db-backup_$(date +%Y-%m-%d_%H-%M-%S).sql`

### в zip архиве

`docker exec postgres-learn-py pg_dump -U postgres -d shop_db_hw3_2 -F p --inserts | sed '/^\\restrict/d; /^\\unrestrict/d' | zip > app-db-backup_$(date +%Y-%m-%d_%H-%M-%S).zip`

### аргументы

#### pg_dump

-U postgres — имя пользователя

-d shop_db_hw3_2 — имя базы данных.

-F p — самый важный флаг (Format: Plain text). Он говорит утилите: «сделай бэкап в виде обычного понятного текста».

--inserts — заставляет записывать данные привычными командами INSERT INTO ... VALUES .... По умолчанию Postgres использует команду COPY, которая работает быстрее, но её сложнее читать глазами в текстовом файле. Флаг --inserts делает файл максимально переносимым.

-f backup.sql — имя файла, в который запишется результат

#### Docker

Разбор отличий для Docker:
docker exec -t имя_контейнера — даёт команду Docker запустить процесс внутри работающего контейнера.

> вместо -f — знак перенаправления потока >. Утилита pg_dump выводит весь текст в консоль контейнера, а этот знак перехватывает его и сохраняет в файл backup.sql уже на вашей реальной машине (в той папке, где сейчас открыт терминал).

### бэкап ТОЛЬКО структуры

без самих товаров и пользователей

Добавьте флаг -s (schema-only):

`pg_dump -U postgres -d shop_db_hw3_2 -F p -s -f structure.sql`

### бэкап ТОЛЬКО данных (без таблиц)

Добавьте флаг -a (data-only):

```Bash
pg_dump -U postgres -d shop_db_hw3_2 -F p -a --inserts -f data.sql
```

## restore

`docker exec -i postgres-learn-py psql -U postgres -d shop_db_hw3_2 < backup.sql`
