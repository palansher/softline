import random

from car import Car


class Factory(object):
    def __init__(self, title_factory, models_factory):
        self.title_factory = title_factory
        self.models_factory = models_factory

    def create(self, title):
        """
        Создание авто
        :param title: Название модели
        :return:
        """
        if title in self.models_factory:
            print(f'Завод {self.title_factory} приступил к созданию авто: {title}')
            car = Car(title, random.randint(1000, 5000))
            print(f'Автомобиль {title} готов')
            return car
        print(f'Завод {self.title_factory} не производит {title}')
        return None