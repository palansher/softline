from psycopg2 import pool

# Создаём пул при старте приложения
db_pool = psycopg2.pool.SimpleConnectionPool(
    1, 20,  # минимум 1, максимум 20 соединений
    host='localhost',
    port='5433',
    dbname='store',
    user='postgres',
    password='postgres'
)

def get_db_connection():
    """Берёт соединение из пула"""
    return db_pool.getconn()

def return_db_connection(conn):
    """Возвращает соединение в пул"""
    db_pool.putconn(conn)