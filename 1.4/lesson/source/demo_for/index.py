# Общая конструкция цикла for имеет вид:
# for item in множество_элементов:
#     тело цикла
import random

# cities = ['Москва','Омск','Томск']
#
# for city in cities:
#     print(city)


# Пример - вывести 5 элементов в консоль через цикл for

# for i in [1,2,3,4,5]:
#     print(f"Элемент №{i}")

# Оптимизируем пример выше, используя range, который генерирует набор чисел

# range(n) - генерация чисел от 0 до n
# range(a,b) - генерация чисел от a до b
# range(a,b,step) - генерация чисел от a до b с шагом step

# print(list(range(10)))
# print(list(range(1,10,3)))

# Пример №1
# for i in range(10):
#     if i <= 8:
#         continue
#     print(i)

# Пример №2 (проверить ученика на знание таблицы умножения на основе 5 вопросов)
# MAX_QUESTIONS = 5
# count_errors = 0
#
# for _ in range(MAX_QUESTIONS):
#     a = random.randint(1, 10)
#     b = random.randint(1, 10)
#     if int(input(f'{a} * {b} = ')) != a * b:
#         count_errors += 1
#         if count_errors > 2:
#             print("Незачет!")
#             break
# else:
#     print("Зачет!!!")

# Пример №3 (Обход строки)

str = "hello world!"
find = input("Введите символ\n")
for item in str:
    if item == find:
        print("Символ найден!")
        break
else:
    print("Элемент не найден")