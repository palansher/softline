"""Сервер WEB-Socket"""

import time
from socket import *

class WS_Server:
    "Класс свойств и методов работы с сервером WEB-сокет"
    def __init__(self, adress, port):
        self.adress = adress
        self.port = port
        self.answer = None
        self.server = None
        self.message = None

    def create_socket(self):
        """Создание сокета"""
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((self.adress, self.port))
        self.server.listen(5) #допускаем до 5 запросов одновременно

    def get_question_answer(self):
        """Прием запроса и формирование ответа клиенту. Цикл из 10 запросов"""
        i = 0
        while i < 10:
            sock, data_from_client = self.server.accept()
            print(f'Получен запрос от клиента с данными {data_from_client}')
            data = sock.recv(1024)
            message = data.decode('UTF-8')
            print(f'Принято сообщение: {message}')
            # Готовим ответ клиенту
            answer = f'Привет, Вы подключились к серверу {self.adress} по порту {self.port} \n{time.ctime()}. \nРезультат вычислений '
            try:
                result = eval(message)
                answer += f'{message} = {result}'
            except:
                answer += f'{message} - некорректен'
            finally:
                # Шифруем строку для отправки клиенту
                sock.send(answer.encode('UTF-8'))
                sock.close()
            i += 1
            print (f'Запрос {i} обработан')