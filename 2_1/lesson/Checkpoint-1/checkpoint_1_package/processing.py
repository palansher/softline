"""Модуль инициализации и вычислений"""
import math,re
from math import degrees

# Коэффициенты
a = b = c = 0.0
# Флаг, является ли уравнение квадратным (false) или линейным (true)
equation_flag=False


def set_coefficient(coeff_name:str)->float:
    """
    Ввод, проверка и преобразование в тип float коэффициента квадратного уравнения
    :param coeff_name: имя коэффициента
    :return: коэффициент типа float
    """
    reg = r"^-?([0-9]+\.[0-9]+|[0-9]*\.[0-9]+|[0-9]+)$"
    while True:
        coeff_value=input(f"Введите коэффициент {coeff_name}: ")
        if re.match(reg, coeff_value):
            return float(coeff_value)
        else:
            print("Коэффициент может быть только целым или вещественным числом (включая ноль)")

def show_equation(a:float,b:float,c:float)->None:
    """
    Печать на экран квадратного уравнения
    :param a: коэффициент a
    :param b: коэффициент b
    :param c: коэффициент c
    :return: None
    """
    def string_builder(x)->str:
        return f"{x:.0f}" if x.is_integer() else f"{x}"
    show_separator()
    result=""
    # Обработка a
    if a !=0:
        result += f"{string_builder(a)}*x^2"
    # Обработка b
    if b > 0:
        result += f" +{string_builder(b)}*x" if a!=0 else f"{string_builder(b)}*x"
    elif b < 0:
        result += f" -{string_builder(-b)}*x"
    # Обработка c
    if c > 0:
        result += f" +{string_builder(c)}" if a!=0 or b!=0 else f"{string_builder(c)}"
    elif c < 0:
        result += f" -{string_builder(-c)}"
    print("Квадратное уравнение имеет следующий вид:" if a!=0 else "Линейное уравнение имеет следующий вид:")
    show_separator()
    print(f"{result} = 0")
    show_separator()

def show_separator(sep_char="-",sep_len=30)->None:
    """
    Вывод разделителя на экран
    :param sep_char: символ разделителя
    :param sep_len: длина разделителя
    :return: None
    """
    print(f"{sep_char}"*sep_len)

def init_equation()->None:
    """
    Инициализация(ввод) коэффициентов
    :return: None
    """
    global a, b, c, equation_flag
    show_separator()
    print("Введите коэффициенты квадратного уравнения (a*x^2 + b*x + c = 0)")
    a = set_coefficient("a")
    b = set_coefficient("b")
    c = set_coefficient("c")
    show_equation(a, b, c)
    if a == 0 and b == 0:
        print("Неверное значение коэффициентов а = 0 и b = 0. Попробуйте ввести другие значения")
        init_equation()
    elif a == 0:
        print("Это не квадратное уравнение!")
        equation_flag=True

def get_roots(precision:int)->None:
    """
    Вычисление квадратных корней
    :param precision: Точность (количество знаков после запятой)
    :return: None
    """
    if equation_flag:
        print("Решаем линейное уравнение")
        x = -c/b
        print(f"Корень линейного уравнения x= {x.__round__(precision)}")
        pass
    else:
        discr = (b * b - (4 * a * c)).__round__(precision)
        print(f"Дискриминант равен: {discr}")
        show_separator()
        if discr > 0:
            # Два корня
            x1 = (-b + math.sqrt(discr)) / (2 * a)
            x2 = (-b - math.sqrt(discr)) / (2 * a)
            print("Дискриминант больше 0, уравнение имеет 2 корня")
            print(f"x1 = {x1.__round__(precision)}\nx2 = {x2.__round__(precision)}")
        elif discr == 0:
            # Один корень
            x = -b / (2 * a)
            print("Дискриминант равен 0, уравнение имеет 1 корень")
            print(f"x = {x.__round__(precision)}")
        else:
            # Корней нет
            print("Корней в уравнении нет")

def processing(precision:int=5)->None:
    """
    Основная функция решения квадратного уравнения
    :param precision: точность (количество знаков после запятой)
    :return: None
    """
    init_equation()
    get_roots(precision)