from abc import ABC, abstractmethod

class Window(ABC):

    @abstractmethod
    def build(self):
       pass

class PlasticWindow(Window):
    def build(self):
        print('Установили пластиковое окно')

class WoodWindow(Window):
    def build(self):
        print('Установили деревянное окно')

class House:
    def __init__(self, window:Window):
        self.window = window

    def build(self):
        print('Построили дом')
        self.window.build()




house = House(WoodWindow())
house.build()


# Внедрение зависимостей может быть реализовано через:
# 1) Конструктор класса
# 2) Через сеттеры
# 3) Через внешние системы