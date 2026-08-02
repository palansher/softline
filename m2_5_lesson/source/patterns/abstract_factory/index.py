from abc import ABC, abstractmethod


class Food:
    def __init__(self,title):
        self.title = title

    def __str__(self):
        return self.title

class Drink:
    def __init__(self,title):
        self.title = title

    def __str__(self):
        return self.title

class AbstractMenu(ABC):
    @abstractmethod
    def add_food(self) -> Food:
        pass

    @abstractmethod
    def add_drink(self) -> Drink:
        pass

class MenuFirst(AbstractMenu):
    def add_food(self) -> Food:
        return Food('Пицца')

    def add_drink(self) -> Drink:
        return Drink('Чай')

class MenuSecond(AbstractMenu):
    def add_food(self) -> Food:
        return Food('Первое блюдо')

    def add_drink(self) -> Drink:
        return Drink('Компот')

class FactoryMethod:
    @staticmethod
    def get_menu(menu_number):
        if menu_number == 1:
            return MenuFirst()
        elif menu_number == 2:
            return MenuSecond()

menu = FactoryMethod.get_menu(1)
print(menu.add_food(),":",menu.add_drink())