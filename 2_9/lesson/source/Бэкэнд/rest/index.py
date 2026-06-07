# REST API - это механизм взаимодействия клиента и сервера на основе протокола HTTP,
# который основан на методах:
#
# 1) GET - используется для получения данных
# 2) POST - используется для создания новой сущности (обязательно тело запроса)
# 3) PUT - используется для полного обновления объекта на сервере
# 4) PATCH - используется для частичного обновления объекта на сервере
# 5) DELETE - используется для удаления записи (тело допускается, но на пракике используется крайне редко)
#
# Метод называется идемпотентным если при нескольких запросах с одинаковым телом запроса Вы получаете
# одинаковый результат
import json

import requests

# Простой GET запрос

# response = requests.get('https://jsonplaceholder.typicode.com/posts')
# print(response.status_code)
# print(response.json())

# Пример №2 (получение курса доллара)

# response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
# valutes = json.loads(response.text)
# v = valutes['Valute']['USD']
# print(f"{v['Name']} стоит {v['Value']}")

# Пример №3 (Прогноз погоды)
# response = requests.get('http://wttr.in')
# print(response.text)

# Пример №4 (Работа с POST)

# body = {
#     'title':'Новая заметка',
#     'body':'Содержимое заметки'
# }
# response = requests.post('https://jsonplaceholder.typicode.com/posts',json=body)
# print(response.status_code)
# print(response.json())

# Пример №5 (PUT запрос)
# body = {
#     'title':'Новая заметка 2',
#     'body':'Содержимое заметки 2'
# }
# response = requests.put('https://jsonplaceholder.typicode.com/posts/1',json=body)
# print(response.status_code)
# print(response.json())

# Пример №6 (DELETE запрос)

response = requests.delete('https://jsonplaceholder.typicode.com/posts/1')
print(response.status_code)
print(response.json())
