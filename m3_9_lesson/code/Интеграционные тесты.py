import time
import unittest

import docker
import psycopg2

class MyTestIntegrationForCrudTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Данный метод запускается до всех тестов, т.е. первым"""
        cls.client = docker.from_env()
        cls.container = cls.client.containers.run(
            "postgres:17",
            environment={
                "POSTGRES_USER": "postgres",
                "POSTGRES_PASSWORD": "postgres",
                "POSTGRES_DB": "my_db",
            },
            ports={"5432/tcp": None},
            detach=True, #запуск в фоновом режиме
        )
        time.sleep(10)

        # Получение динамического порта контейнера
        cls.container.reload()
        port = cls.container.attrs['NetworkSettings']['Ports']["5432/tcp"][0]["HostPort"]

        # Конфигурация подключения к базе данных
        cls.db_config = {
            'dbname': 'my_db',
            'user': 'postgres',
            'password': 'postgres',
            'host': 'localhost',
            'port': port
        }

        # Создаем тестовую таблицу
        conn = psycopg2.connect(**cls.db_config)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE students (
                id SERIAL PRIMARY KEY,
                name varchar(30) NOT NULL,
                phone varchar(15) NOT NULL)""")
        conn.commit()
        cur.close()
        conn.close()


    @classmethod
    def tearDownClass(cls):
        """Остановка и удаление контейнера"""
        cls.container.stop()
        cls.container.remove()
        cls.client.close() #закрытие ДОКЕР

    def setUp(self):
        """Метод запускается перед каждым тестом"""
        self.conn = psycopg2.connect(**self.db_config)
        self.cur = self.conn.cursor()

    def tearDown(self):
        self.cur.execute("TRUNCATE TABLE students RESTART IDENTITY CASCADE")
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def test_create_table(self):
        """Тестируем создание таблицы"""
        self.cur.execute("""CREATE TABLE demo (id serial PRIMARY KEY, name varchar(30))""")
        self.conn.commit()

        # Проверка на существование таблицы:
        self.cur.execute("SELECT table_name FROM information_schema.tables WHERE table_name = 'demo'")
        result = self.cur.fetchone()
        self.assertEqual(result[0], 'demo')

        # Удаление таблицы
        self.cur.execute("DROP TABLE demo")
        self.conn.commit()

if __name__ == '__main__':
    unittest.main()