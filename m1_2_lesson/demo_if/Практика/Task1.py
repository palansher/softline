"""Вывод информации о статусе пользователя на основе его возраста"""
from random import randint

age = randint(5,30)
print("Возраст:",age)
if age < 7:
    print("Ребенок")
elif age <= 17:
    print("Ученик")
else:
    answer = input('Введите Y если Вы учитесь после школы дальше').upper()
    if answer == 'Y':
        print("Желаем успешного обучения!")
    else:
        answer =  input('Введите Y если Вы работаете').upper()
        if answer == 'Y':
            print("Желаем успешной работы!")
        else:
            print("Приятного отдыха")


# Абстрактный пример

# Любое значение, которое отличается от 0, "",'',None это True, а перечисленные значения это всегда по умолчанию
# False

# a = 3
# if a:
#     if a < 5:
#         a += 5
#         if "test":
#             a = 0
#     else:
#         if 10:
#             a = 1
#     a += 1
#
# print(a)

