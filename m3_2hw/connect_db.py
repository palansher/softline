# import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from flask import g
# from psycopg2.extras import RealDictCursor

_pool = None

def init_pool() : 
    global _pool
    if _pool is None:
        _pool = ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            host="vm-perepechenko01.brg.loc",
            user="postgres",
            password="admin",
            database="shop_db_hw3_2",
            port="5432",
        )

def get_connection():
    if _pool is None:
        init_pool()
    return _pool.getconn() # pyright: ignore[reportOptionalMemberAccess]

def release_connection(conn):
    if _pool is not None:
        _pool.putconn(conn)



def get_db():
    if 'db' not in g:
        g.db = get_connection()
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        release_connection(db)

# connection = psycopg2.connect(
#     host="vm-perepechenko01.brg.loc",
#     user="postgres",
#     password="admin",
#     database="shop_db_hw3_2",
#     port="5432",
# )

# Включаем автоматическое закрытие одиночных запросов - защищает от зависших локов
# connection.autocommit = True

# with connection: # конфликтует с connection.autocommit
# cursor = connection.cursor(cursor_factory=RealDictCursor)
