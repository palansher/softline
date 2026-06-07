# Компактная форма if/else называется тернарным оператором

from random import randint

number_day = randint(1, 7)
print(number_day)
print("Будний день" if 1 <= number_day <= 5 else "Выходной день")

# a = 10
# b = 20 if not a else 30
# print(b)


