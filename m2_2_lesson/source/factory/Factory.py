import random

from factory.Car import Car

class Factory:
    def __init__(self,title_factory,models_factory):
        self.models_factory = models_factory
        self.title_factory = title_factory

    def create_car(self,title_car):
        """Выполняем создание автомобиля по заказу
        :param title_car: название автомобиля, который необходимо создать
        :return: готовый автомобиль, т.е. объект класса Car
        """
        print(f"Завод {self.title_factory} приступил к созданию автомобиля {title_car}")
        car = Car(title_car,random.randint(1000,5000))
        print(f"Автомобиль {title_car} готов!")
        return car