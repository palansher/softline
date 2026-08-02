import random

from factory import Factory


class Order:
    INFO = {"MIN_AGE":10,"DISCAUNT":10,"IS_ACTIVE":False}
    def __init__(self,count_cars:int,models:list,factory:Factory):
        self.count_cars = count_cars
        self.models = models
        self.factory = factory
        self.common_price = 0 #Итоговая стоимость всех автомобилей в заказе
        self.cars = [] #фура, которую нужно заполнить заказанными автомобилями

    def start_order(self,age:int)->None:
        if age >= Order.INFO["MIN_AGE"]:
            Order.INFO["IS_ACTIVE"] = True
        for i in range(1,self.count_cars + 1):
            car = self.factory.create_car(random.choice(self.models))#завод авто создал
            if car:
                if Order.INFO["IS_ACTIVE"]:
                    car.price = car.price - round(car.price * Order.INFO["DISCAUNT"] / 100,2)
                self.cars.append(car) #помещаем авто в фуру для отправки дилеру
                self.common_price += car.price #учтем стоимость авто в заказе

    def show_result(self):
        if Order.INFO["IS_ACTIVE"]:
            print("Автосалону предоставлена скидка",Order.INFO["DISCAUNT"])
        for i,car in enumerate(self.cars,1):
            print(f"{i}) {car.title} стоит {car.price}")
        print("Общая стоимость заказа:",self.common_price)
        print("*" * 50)
        self.show_count_models()

    def show_count_models(self):
        access_models = set(self.factory.models_factory)
        models_orders = set(self.models)
        actual_models = access_models.intersection(models_orders)
        for model_order in actual_models:
            counter = 0
            for car in self.cars:
                if car.title == model_order:
                    counter += 1
            print(f"Автомобилей {model_order} было создано {counter} единиц")

