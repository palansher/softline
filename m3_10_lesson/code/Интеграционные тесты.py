import unittest
import time


import docker
import psycopg2

class MyTestIntegrationForCrudTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Данный метод будет запущен первым"""
        #Создаем клиент Docker и используем переменные среды
        cls.client = docker.from_env()
        cls.container = cls.client.containers.run(
            "postgres:17",
            environment={
                'POSTGRES_USER':'postgres',
                'POSTGRES_PASSWORD':'postgres',
                'POSTGRES_DB':'my_db',
            },
            ports={"5432/tcp":None},
            detach=True #Запуск в фоновом режими
        )
        # Ожидание инициализации Postgres
        time.sleep(10)

        # Получение динамического порта контейнера
        cls.container.reload() #обновляем данные контейнера
        # cls.container.attrs - словарь с метаданными контейнера
        port = cls.container.attrs['NetworkSettings']['Ports']['5432/tcp'][0]['HostPort']

        # Конфигурация подключения к БД
        cls.db_config = {
            'dbname': 'my_db',
            'user': 'postgres',
            'password': 'postgres',
            'host': 'localhost',
            'port': port
        }

        #Создаем тестовую таблицу
        conn = psycopg2.connect(**cls.db_config)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE students(
               id SERIAL PRIMARY KEY,
               name VARCHAR(30),
               phone VARCHAR(15)
            )
        """)
        conn.commit()
        cur.close()
        conn.close()

    @classmethod
    def tearDownClass(cls):
        """Остановка и удаление контейнера"""
        cls.container.stop()
        cls.container.remove()
        cls.client.close() #Закрытие Докер-

    def setUp(self):
        """Метод запускается перед каждым тестом"""
        self.conn = psycopg2.connect(**self.db_config)
        self.cur = self.conn.cursor()

    def tearDown(self):
        """Метод запускается после каждого теста. В нем будем удалять данные"""
        self.cur.execute('TRUNCATE TABLE students RESTART IDENTITY CASCADE')
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def test_create_table(self):
        """Тестируем создание таблицы"""
        self.cur.execute("CREATE TABLE demo(id serial primary key,name varchar(20))")
        self.conn.commit()

        # Проверка на существование таблицы
        self.cur.execute("""
            SELECT table_name FROM information_schema.tables WHERE table_name = 'demo'
        """)
        result = self.cur.fetchone()
        self.assertEqual(result[0], "demo")

        # Удаление таблицы
        self.cur.execute("DROP TABLE demo")
        self.conn.commit()

    def test_insert_table(self):
        self.cur.execute("INSERT INTO students(name,phone) VALUES(%s,%s)",('Иван','+79234234234'))
        self.conn.commit()
        # Проверка количества добавленных записей
        self.cur.execute("SELECT COUNT(*) FROM students where name='Иван'")
        count_records = self.cur.fetchone()[0]
        self.assertEqual(count_records,1)

    def test_select_table(self):
        self.cur.execute("INSERT INTO students(name,phone) VALUES(%s,%s)", ('Алексей', '+79234234231'))
        self.conn.commit()

        # Проверка количества добавленных записей
        self.cur.execute("SELECT name,phone FROM students where name='Алексей'")
        data = self.cur.fetchone()
        self.assertEqual(data, ('Алексей','+79234234231'))

    def test_update_table(self):
        self.cur.execute("INSERT INTO students(name,phone) VALUES(%s,%s)", ('Игорь', '+79334234231'))
        self.conn.commit()
        # Обновление данных
        self.cur.execute("UPDATE students SET phone='+7935346546' WHERE name='Игорь'")
        self.conn.commit()

        # Проверка количества измененных записей
        self.cur.execute("SELECT phone FROM students where name='Игорь'")
        phone = self.cur.fetchone()[0]
        self.assertEqual(phone, '+7935346546')

    def test_delete_table(self):
        self.cur.execute("INSERT INTO students(name,phone) VALUES(%s,%s)", ('Мария', '+79934234231'))
        self.conn.commit()

        self.cur.execute("DELETE FROM students WHERE name='Мария'")
        self.conn.commit()

        # Проверка удаления
        self.cur.execute("SELECT COUNT(*) FROM students where name='Мария'")
        count_records = self.cur.fetchone()[0]
        self.assertEqual(count_records, 0)





if __name__ == '__main__':
    unittest.main()