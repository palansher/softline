def to_dict(obj):
    """Конвертация объекта в словарь"""
    return {key:value for key,value in obj.__dict__.items()}

class Car:
    def __init__(self,title,price):
        self.title = title
        self.price = price

car1 = Car("Audi",1000)
car2 = Car("BMW",1200)

cars = [car1,car2]

cars_dict = [to_dict(car) for car in cars]
import json
str_json = json.dumps(cars_dict,indent=4)
print(str_json)

