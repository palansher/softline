
import math


def solve_quadratic():
    print("Программа для решения квадратного уравнения: ax^2 + bx + c = 0")

    try:
        # Запрашиваем ввод и преобразуем в float
        # Замена запятой на точку позволяет вводить числа в обоих форматах
        a = float(input("Введите a: ").replace(',', '.'))
        # Проверка на квадратное уравнение
        if a == 0:
            print("Это не квадратное уравнение.")
            return

        b = float(input("Введите b: ").replace(',', '.'))
        c = float(input("Введите c: ").replace(',', '.'))
    except ValueError:
        print("Ошибка: введите корректные числа, а не текст.")
        return

    # Вычисление дискриминанта
    d = b ** 2 - 4 * a * c

    if d > 0:
        x1 = (-b + math.sqrt(d)) / (2 * a)
        x2 = (-b - math.sqrt(d)) / (2 * a)
        print(f"Уравнение имеет два корня: {x1:.5f} и {x2:.5f}")
    elif d == 0:
        x = -b / (2 * a)
        print(f"Уравнение имеет один корень: {x:.5f}")
    else:
        print("Уравнение не имеет корней")


# if __name__ == "__main__":
solve_quadratic()
