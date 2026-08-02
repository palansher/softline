"""Сделать чат-бот между клиентом и сервером. 
Клиент может передавать запросы в виде любых математических действий, а сервер должен 
их принимать обрабатывать и возвращать клиенту верный ответ или сообщение об ошибке, если 
данные, полученные от клиента были некорректными.

Клиентский модуль.
Предварительно выполнить main_s.py
"""

from WS_Client import WS_client
import random

list_operator= ['+','-','/','*','=']                # список возможных операндов
list_operand = ['3','5','x','y','6','7','9']        # список возможных оператор

i = 0
while i < 10:
    work = WS_client('localhost', 8899)             # создаем соединение
    print(f'{"="*100}')

    # генерируем операции для отправки 
    # на сервер для вычисления
    if work.run_client():                           # проверяем установлено ли соединение
        operand_1 = random.choice(list_operand)
        operand_2 = random.choice(list_operand)
        operator = random.choice(list_operator)
        work.message = operand_1+operator+operand_2
        work.send_get_answer()                      # отправка и обработка ответа                 
    i += 1
