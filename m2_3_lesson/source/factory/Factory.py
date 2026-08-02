import random

from Car import Car


class Factory:
    def __init__(self,title:str,models_factory:list):
        self.models_factory = models_factory
        self.title = title

    def create_car(self,title_car):
        """Производство автомобиля по заказу
            :arg title_car: название авто, которое нужно создать
            :return: готовый автомобиль
        """
        if title_car in self.models_factory:
            print(f"Завод {self.title} приступил к изготовлению автомобиля {title_car}")
            car = Car(title_car,random.randint(1000,5000))
            print(f"Автомобиль {self.title} {title_car} готов!")
            return car
        print("Нет технической возможности изготовить авто", title_car)
