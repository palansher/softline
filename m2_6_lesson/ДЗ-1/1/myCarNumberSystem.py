from re import match
from random import randint, choice
from myСarNumber import CarNumber


class CarNumberSystem:
    list_letters_series = ["А", "В", "Е", "К", "М", "Н", "О", "Р", "С", "Т", "У", "Х"]
    region = None
    collection_cars_numbers = []

    def __init__(self, count_cars_numbers):
        """Заполнить коллекцию автомбильными номерами"""
        self.count_cars_numbers = count_cars_numbers
        self.create_region()
        while count_cars_numbers > 0:
            number = self.great_random_number(3)
            series = self.create_series()
            if self.is_dublicate(number, series):
                continue
            car_number = CarNumber(
                series,
                number,
                CarNumberSystem.region,
                input("Введите имя владельца автомобиля:\n"),
            )
            CarNumberSystem.collection_cars_numbers.append(car_number)
            print("Создан номер", car_number)
            print()
            count_cars_numbers -= 1

    def create_region(self):
        """Создание региона для номера автомобиля в ручном режиме"""
        while True:
            input_region = input(f"Введите регион: ")
            if match("^[0-9]{3}$", input_region):
                CarNumberSystem.region = input_region
                print()
                break
            else:
                print(f"Введите корректный регион, в формате 000")

    @staticmethod
    def great_random_number(count_number):
        """Создание рандомной последовальности из нужного количества цифр"""
        random_number = ""
        for _ in range(count_number):
            random_number += str(randint(0, 9))
        return random_number

    def create_series(self):
        random_series = ""
        for _ in range(3):
            random_series += choice(CarNumberSystem.list_letters_series)
        return random_series

    def is_dublicate(self, number, series):
        for car_number in CarNumberSystem.collection_cars_numbers:
            if car_number.number == number and car_number.series == series:
                return True
        return False

    @classmethod
    def find_owner(cls, s_n):
        try:
            series = s_n[0] + s_n[4:6]
            number = s_n[1:4]
            region = s_n[6:]

            for car_number in CarNumberSystem.collection_cars_numbers:
                if (
                    car_number.series == series
                    and car_number.number == number
                    and car_number.region == region
                ):
                    return f"Владелец автомобиля: {car_number.owner_fio}"
            return "Указанный номер автомобиля в системе не найден"
        except IndexError:
            return f"Неверное значение номера автомобиля для поиска"
