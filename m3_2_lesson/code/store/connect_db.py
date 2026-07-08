import psycopg2
from psycopg2.extras import RealDictCursor

connection = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="postgres",
    database="flask_shop",
    port="5433" # 5432 - default port
     
)

with connection:
    cursor = connection.cursor(cursor_factory=RealDictCursor)
