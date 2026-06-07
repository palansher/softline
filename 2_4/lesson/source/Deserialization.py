class Car:
    def __init__(self,title,age):
        self.title = title
        self.age = age

    def __str__(self):
        return f'{self.title} имеет возраст {self.age}'

def from_dict(cls,data):
    """
    :param cls:ссылка на класс для которого делаем объект
    :param data:словарь с данными
    :return:объект класса cls
    """
    # Создаем новый объект из словаря
    obj = cls.__new__(cls) #создали пустой объект
    for key,value in data.items():
        setattr(obj,key,value)#наполняем объект свойствами на основе словаря из параметра
    return obj
#
# test_dict = {'title':'Audi','age':2}
# car = from_dict(Car,test_dict)
# print(car)

json_str = """[
        {
            "title": "Audi",
            "age":10
        },
         {
            "title": "BMW",
            "age":1
        },
         {
            "title": "VW",
            "age":3
        }
]"""

# Задание - преобразовать строку json в список объектов

import json
data = json.loads(json_str) #получили список словарей
# print(data)

# Получаем список объектов
cars = [from_dict(Car,car) for car in data]

for car in cars:
    print(car)

