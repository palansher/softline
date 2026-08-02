from typing import Dict, Optional
from models import CarNumber


class CarNumberSystem:
    """
    Управляет системой учета.
    Хранит связь между номерами машин и именами их владельцев.
    """

    def __init__(self):
        # Хранилище: {Номер: Имя}
        self.database: Dict[str, str] = {}

    @staticmethod
    def format_owner_name(raw_name: str) -> str:
        """
        Статический метод для форматирования ФИО.
        Делает первую букву каждого слова заглавной, остальные — строчными.

        :param raw_name: Ввод пользователя (например, 'иван иванович иванов')
        :return: Отформатированная строка (например, 'Иван Иванович Иванов')
        """
        return " ".join(word.capitalize() for word in raw_name.split())

    def is_number_exists(self, car_number_str: str) -> bool:
        """
        Проверка на существующий номер в базе.

        :param car_number_str: Строка номера (ключ)
        :return: True, если номер уже есть в базе
        """
        return car_number_str in self.database

    def register_new_entry(self, owner_name: str, region: str) -> str:
        """
        Регистрирует владельца и автоматически генерирует для него уникальный номер.

        :param owner_name: Сырое имя владельца из input.
        :param region: Регион для генерации.
        :return: Сгенерированный итоговый номер.
        """
        formatted_owner_name = self.format_owner_name(owner_name)

        while True:
            # Генерируем новый номер
            new_car_number = CarNumber.generate_random(region)
            num_str = new_car_number.full_number

            # Проверка на валидность номера
            if not CarNumber.is_valid(num_str):
                continue

            # Проверка на дубликат номера в базе
            # Если номер уже есть (даже если у этого же владельца), генерируем заново
            if self.is_number_exists(num_str):
                continue

            # Если мы здесь, значит номер уникален и валиден.
            # Записываем в базу. Если имя владельца уже сущестует — у него просто появится еще один авто с новым номером.
            self.database[num_str] = formatted_owner_name
            return num_str

    def find_owner(self, full_number: str) -> Optional[str]:
        """
        Поиск владельца по номеру.
        Метод устойчив к регистру ввода.

        :param full_number: Номер авто для поиска
        :return: Имя владельца или None, если номер не найден
        """
        return self.database.get(full_number.upper())

    def display_all(self) -> None:
        """
        Вывод реестра владельцев авто и их номеров.
        """
        print("\n" + "=" * 50)
        print(f"{'НОМЕР':<15} | {'ВЛАДЕЛЕЦ':<20}")
        print("-" * 50)
        for num, owner in self.database.items():
            print(f"{num:<15} | {owner:<20}")
        print("=" * 50)
