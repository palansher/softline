# Функция filter - фильтрует элементы и возвращает новый итерируемый объект
from random import randint

numbers = [randint(1,9) for i in range(10)]
print(numbers)

even_numbers = filter(lambda item: item % 2 == 0, numbers)
print(list(even_numbers))

# Создать список городов (5 городов). Построить на базе исходного списка горов новый список
# в котором содержатся только города с количеством символов более 5Ос

cities = ["Москва","Ашхабад","Омск","Владивосток","Орел"]
print(cities)

big_cities = filter(lambda item: len(item) > 5, cities)
print(list(big_cities))