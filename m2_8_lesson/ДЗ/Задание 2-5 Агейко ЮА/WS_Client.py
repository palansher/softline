"""Клиент WEB-Socket"""
from socket import *
import ast

class WS_client:
    "Класс свойств и методов работы клиента WEB-сокет"
    def __init__(self, adress, port):
        self.adress = adress
        self.port = port
        self.answer = None
        self.client = None
        self.message = None

    def run_client(self):
        """Создание соединения"""
        try:
            self.client = socket(AF_INET, SOCK_STREAM)
            # Подключаемся к серверу
            self.client.connect((self.adress, self.port))
            print(f'Подключаемся к серверу: {self.adress} {self.port}')
            return True
        except:
            print(f'Ошибка подключения к серверу: {self.adress} {self.port}')
            return False

    def send_get_answer(self):
        """Отправка запроса и обработка ответа от сервера"""
        if self.check_message():
            print(f'Отправка сообщения серверу для вычисления: "{self.message}"')
            self.client.send(self.message.encode('UTF-8'))
            self.answer = self.client.recv(1024)
            print('Сервер ответил:', self.answer.decode('UTF-8'))
        
    def check_message(self):
        """ Предвариельная проверка запроса на возможность выполнения"""
        try:
            ast.parse(self.message, mode='eval') 
            return True
        except SyntaxError:
            print("Некорректное выражение")
            return False

    def __del__(self):
        """Закрытие соединения"""
        self.client.close()
        print ('Соединение закрыто')

    
