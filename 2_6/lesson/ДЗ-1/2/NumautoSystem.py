import random
import re
from Numauto import Numauto

class NumautoSystem:
    """Класс коллекции обьектов (номера транспортных средств) и функций класса"""
    region = None
    list_numbers = [] #список номеров
    def __init__(self,count_autonums):
        """Заполнить коллекцию номерами автомобилей"""
        self.create_region()
        while count_autonums > 0:
            number_autonum = NumautoSystem.create_random_number(3)
            print(number_autonum)
            if self.is_dublicate(number_autonum):
                continue
            # Создать обьект номер транспортного средства
            autonum = Numauto(self.create_series(),number_autonum,NumautoSystem.region,input('Введите имя владельца транспортного средства\n'))
            NumautoSystem.list_numbers.append(autonum)
            print("Зарегистрирован новый номер",autonum)
            count_autonums -= 1

    @classmethod
    def is_dublicate(self,number):
        """Проверка на дубликат цифровой части номера"""
        for autonum in NumautoSystem.list_numbers:
            if autonum.number == number and autonum.series == Numauto.series:
                return True
        return False

    @staticmethod
    def create_random_number(count_numbers):
        """Получаем строку с необходимым количеством цифр"""
        s = ""
        for _ in range(count_numbers):
            s += str(random.randint(0,9))
        return s

    @classmethod
    def create_series(self):
        """Генератор серии из трех букв английского алфавита"""
        simbol_in_series = list(c for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        return random.choices(simbol_in_series, k=3)

    @classmethod
    def create_region(cls):
        answer = input("Введите регион - ").strip()
        NumautoSystem.region = answer

    @classmethod
    def find_owner(cls,s_n):
        mas = s_n
        for autonum in NumautoSystem.list_numbers:
            if autonum.fullnumber == mas:
                return autonum.fio
        return "Номер в системе не найден!"
