import json
import pprint

cars = """{
    "cars": [
        {
            "id":1,
            "title": "Audi",
            "price":1300
        },
        {
            "id":2,
            "title": "BMW",
            "price":1500
        },
        {
            "id":3,
            "title": "VW",
            "price":1000
        }
    ],
    "store_title":{
        "title_shop":"VipCar",
        "address":"Москва..."
    }
}"""

# Для преобразования строки json в словарь функцию loads
info = json.loads(cars)

#TODO
# pprint.pprint(info)

# Для конвертации словаря(или списка словарей) в строку

dict_to_json = json.dumps(info,ensure_ascii=False,indent=4)
print(dict_to_json)
