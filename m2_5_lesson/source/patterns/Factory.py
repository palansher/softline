from abc import ABC, abstractmethod


class Coffee(ABC):
    def __init__(self, name):
        self.name = name
        self.grind_coffee()
        self.make_coffee()
        self.pass_coffee()

    def grind_coffee(self):
        """Перемалывание зерен"""
        print("Идет процесс перемалывания зерен")

    @abstractmethod
    def make_coffee(self):
        pass

    def pass_coffee(self):
        print("Ваш кофе", self.name,'готов!' )

class Cappuchino(Coffee):
    def make_coffee(self):
        super().make_coffee()
        print("Добавляем молоко")

class Latte(Coffee):
    def make_coffee(self):
        super().make_coffee()
        print("Добавляем много молока")

class Americano(Coffee):
    def make_coffee(self):
        super().make_coffee()

class Factory:
    @staticmethod
    def factory_method(title_coffee):
        match title_coffee.upper():
            case "КАПУЧИНО":
                return Cappuchino(title_coffee)
            case "LATTE":
                return Latte(title_coffee)
            case "AMERICANO":
                return Americano(title_coffee)
            case _:
                print('Ошибка выбора напитка!')


Factory.factory_method(input("Введите название кофе:\n"))