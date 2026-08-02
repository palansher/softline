"""
Просто демонстрация того, как работает Faker для создания рандомных автомобилей.
"""

from car import Car
from car_brand import CarBrand
from faker import Faker
from faker_vehicle import VehicleProvider

# Инициализируем Faker и добавляем провайдер техники
fake = Faker()
fake.add_provider(VehicleProvider)


def generate_random_car() -> Car:
    # fake.vehicle_object() возвращает словарь вида:
    # {'Year': 2019, 'Make': 'Toyota', 'Model': 'Camry', 'Category': 'Sedan'}
    veh_data = fake.vehicle_object()

    brand = CarBrand(name=veh_data["Make"])  # С заглавной буквы 'M'
    return Car(
        brand=brand,
        model=veh_data["Model"],  # С заглавной 'M'
        year=int(veh_data["Year"]),  # С заглавной 'Y'
        category=fake.vehicle_category(),
        vin=fake.vin(),
        color=fake.color_name(),
    )


# Генерируем случайный автомобиль
car = generate_random_car()

print(car)

# print(f"Марка: {car.brand.name}")
# print(f"Модель: {car.model}")
# print(f"Год: {car.year}")
# print(f"VIN: {car.vin}")
# print(f"Цвет: {car.color}")
