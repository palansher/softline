from builder import ConcreteCarBuilder
from director import Director

"""
Я немного отошел от примера из урока.
Не стал делать Fluent Interface (цепочку вызовов) типа:
house = House().build_base('Ленточный').build_box('Кирпич').build_roof('Металллочерепица')

но сделал Директора. Для сборки типовых конфигураций авто.
"""

if __name__ == "__main__":
    # Создаем инструменты
    builder = ConcreteCarBuilder()
    director = Director()

    print("--- Сборка Спортивного Автомобиля ---")
    director.construct_sport_car(builder)
    sport_car = builder.get_result()
    sport_car.show_car_info()

    print("--- Сборка Внедорожника ---")
    director.construct_suv(builder)
    suv = builder.get_result()
    suv.show_car_info()
