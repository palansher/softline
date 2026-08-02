# Существуют разные виды ошибок - синтаксические ошибки, логические ошибки и ошибки, возникающие
# в момент запуска Вашей программы. Для обработки ошибок в рантайме используются операторы
# try и except. Если инструкция может приводить к ошибке при запуске, такую инструкцию рекомендуется
# разместить в блоке try. Если ошибка возникает, то остальные инструкции в блоке try не выполняеются.
# Управление передается в блоке except, который ожидает ошибки данного типа

# Пример №1
from random import randint

# a = 10
# b = randint(0,1)
# try:
#     print(f"{a} / {b} = {a/b}")
#     print("111")
# except ZeroDivisionError as e:
#     # print("Возникла ошибка:",str(e))
#     print("На 0 делить нельзя!")
#
# print("Вы видите эту строку всегда!")

# Пример №2

# while 1:
#     a = input('Введите 1 число')
#     if a == "q":
#         break
#     b = input('Введите 2 число')
#     if b == "q":
#         break
#     try:
#         res = int(a) / int(b)
#
#     except ZeroDivisionError:
#         print("На 0 делить нельзя!")
#     except ValueError:
#         print("Ввели некорректное значение!")
#     except:
#         print("Возникла непредвиденная ошибка!")
#     else:
#         print(f"{a} / {b} = {res}")

# Пример №3
# my_file = 'test.txt'
# try:
#     with open(my_file, 'r') as f:
#         print(f.read())
# except FileNotFoundError:
#     print("Файл не существует")

# Оператор finally содержит блок с инструкциями, которые обязательно должны выполниться даже
# в случае наличия ошибки

# Пример №4
# my_file = 'test.txt'
# file = None
# try:
#     file = open(my_file, 'w')
#     print(1 / randint(0,1))
#
# except FileNotFoundError:
#     print("Файл не существует")
# except ZeroDivisionError as e:
#     print(e)
# finally:
#     if file:
#         file.close()
#         print('Файл был корректно закрыт')

# Пример №5 (оператор raise)

# Если мы хотим завершить работу программы ошибкой, то используйте оператор raise

# number = int(input("Введите число от 20 до 25"))
# if 20 <= number <= 25:
#     print("OK")
# else:
#     raise RuntimeError("Вы ввели неверное значение!")

# Оператор assert

# Конструкция:
# assert условие, сообщение об ошибке
# Если условие True, то выполняются действия ниже, а если False, то выводится сообщение об ошибке

a = 10
b = 0
assert b != 0, "На 0 делить нельзя"
print(a / b)