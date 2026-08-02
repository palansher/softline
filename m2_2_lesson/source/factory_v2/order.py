from factory import Factory
import random

class Order:
    def __init__(self, title_models: list, count_cars: int, factory: Factory):
        self.factory = factory
        self.count_cars = count_cars
        self.title_models = title_models

        self.cars = []
        self.common_price = 0

    def start(self):
        for i in range(1, self.count_cars + 1):
            car = self.factory.create(random.choice(self.title_models))
            if car:
                self.cars.append(car)
                self.common_price += car.price

    def full_info_model(self):
        all_info = {}

        for car in self.cars:
            if car.title in all_info:
                all_info[car.title] += 1
            else:
                all_info[car.title] = 1

        for car_title, count in all_info.items():
            print(f'Автомобилей: {car_title} произведено: {count}')


    def show_result(self):
        for i, car in enumerate(self.cars, 1):
            print(f'{i}) Автомобиль {car.title} стоит: {car.price}')
        print(f'Общая стоимость: {self.common_price}')
        self.full_info_model()
