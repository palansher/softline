# Фишки

## Создание структуры из cli

```bash
#!/usr/bin/env bash

# create-db-structure.sh

dbname="shop_db_hw3_2" 

# работаем идемпотентно :)
docker exec -i postgres-learn-py psql -U postgres -lqt | cut -d \| -f 1 | grep -qw "${dbname}" || docker exec -i postgres-learn-py psql -U postgres -c "CREATE DATABASE ${dbname};"

или

docker exec -i postgres-learn-py psql -U postgres -d "${dbname}" < create-db-structure.sql
```
