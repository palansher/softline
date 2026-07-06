import psycopg2
from psycopg2.extras import RealDictCursor

connection = psycopg2.connect(
    host="vm-perepechenko01.brg.loc",
    user="postgres",
    password="admin",
    database="shop_db_hw3_1",
    port="5432",
)

with connection:
    cursor = connection.cursor(cursor_factory=RealDictCursor)
