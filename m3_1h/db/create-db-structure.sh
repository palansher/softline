#!/usr/bin/env bash

dbname="car_shop_3_1"

# работаем идемпотентно :)
docker exec -i postgres-learn-py psql -U postgres -lqt | cut -d \| -f 1 | grep -qw "${dbname}" || docker exec -i postgres-learn-py psql -U postgres -c "CREATE DATABASE ${dbname};"

docker exec -i postgres-learn-py psql -U postgres -d "${dbname}" < create-db-structure.sql
