import json
from pprint import pprint

store = {
    "cars":[
        {
            "title":"Ауди",
            "price":1000
        },
        {
            "title": "BMW",
            "price": 1200
        },
        {
            "title": "VW",
            "price": 900
        },
    ]
}

# pprint(store)

# Записываем данные нашего словаря в файл .json
# Функция dump конвертирует словарь в файл json
# with open("store.json","w",encoding="utf-8") as f:
#     json.dump(store,f,ensure_ascii=False,indent=4)

# Преобразование файла json в словарь осуществляется функцией dump
with open("store.json","r",encoding="utf-8") as f:
    my_dict = json.load(f)
    pprint(my_dict)