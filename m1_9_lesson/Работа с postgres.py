import psycopg2
from psycopg2.extras import RealDictCursor

connect = psycopg2.connect(
    host="localhost",
    dbname="python8",
    user="postgres",
    password="postgres",
    port="5433"
)

def show_cars():
    sql_query = "select * from marks"
    cursor.execute(sql_query)
    records = cursor.fetchall()  # получаем все записи
    # print(records)
    for record in records:
        print(f'Автомобиль {record["title"]} стоит {record["price"]}')

def update_price():
    info = input('Введите название авто и новую стоимость авто через пробел').split()
    sql_query = f"update marks set price={info[1]} where title='{info[0]}'"
    cursor.execute(sql_query)
    print('Стоимость изменена')


with connect:
    cursor = connect.cursor(cursor_factory=RealDictCursor) #объект cursor позволяет запускать sql запросы к базе данных
    print("До обновления цены:")
    show_cars()
    print("После обновления цены")
    update_price()
    show_cars()
    connect.commit()