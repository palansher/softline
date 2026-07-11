import psycopg2
# from psycopg2.extras import RealDictCursor

connection = psycopg2.connect(
    host="vm-perepechenko01.brg.loc",
    user="postgres",
    password="admin",
    database="shop_db_hw3_2",
    port="5432",
)

# Включаем автоматическое закрытие одиночных запросов - защищает от зависших локов
connection.autocommit = True

# with connection: # конфликтует с connection.autocommit
# cursor = connection.cursor(cursor_factory=RealDictCursor)
