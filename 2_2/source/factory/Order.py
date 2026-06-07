import random

from factory import Factory
from factory.Car import Car


class Order:
    def __init__(self,title_models:list,count_cars:int,factory:Factory):
        self.factory = factory
        self.count_cars = count_cars
        self.title_models = title_models
        # Создаем фуру, которая должна быть загружена готовыми автомобилями
        self.cars = []
        self.common_price = 0 #общая стоимость заказа

    def start(self):
        for i in range(1,self.count_cars+1):
            car = self.factory.create_car(random.choice(self.title_models))
            self.cars.append(car)
            self.common_price += car.price

    def show_result(self):
        for i,car in enumerate(self.cars,1):
            print(f'{i}) Автомобиль {car.title} стоит {car.price}')
        print("Общая стоимость заказа:",self.common_price)
        print("*" * 100)
        self.show_count_models()

    def show_count_models(self):
        for model in self.title_models:
            if model in self.factory.models_factory:
                count = 0
                for car in self.cars:
                    if car.model == model:
                        count += 1
                print(f'{model} была изготовлена {count} раз')