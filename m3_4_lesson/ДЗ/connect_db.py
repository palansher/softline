import psycopg2
from psycopg2.extras import RealDictCursor

connection = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="postgres",
    database="flask_shop",
    port="5433"
)

with connection:
    cursor = connection.cursor(cursor_factory=RealDictCursor)