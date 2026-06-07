class TS:
    def __init__(self,title):
        self.title = title

    def go(self):
        print(self.title,'перемещается')

class Car(TS):
    """Легковой автомобиль"""
    def go(self):
        print(self.title,'может двигаться по дорогам общего пользования')

class Tractor(TS):
    def go(self):
        print(self.title,'может двигаться медленно по общим дорогам')
    def work(self):
        print(self.title,'используется в сельскохозяйственных работах')

class Truck(Car,Tractor):
    def show_info(self):
        self.go()
        self.work()

car = Truck('Камаз')
car.show_info()


# 1) Создать класс Сотрудник. У сотрудника есть имя и оклад и метод - получение общей информации
# 2) Создать потомка - Менеджер, он имеет еще одно свойство - роль (директор). Реализовать
# полиморфизм.