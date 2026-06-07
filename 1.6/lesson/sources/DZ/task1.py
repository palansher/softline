"""
Напишите функцию get_middle(start,end), которая находит среднее арифметическое значение в отрезке от start до end
"""


def get_middle(start:int, end:int):
    # Проверяем, что оба аргумента — целые числа (int)
    if type(start) is int and type(end) is int:
        return (start + end) / 2
    return "Ошибка: значения должны быть целыми числами"


print(get_middle(5,10))


