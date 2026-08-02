# def f(*x): # параметры в кортеже
# def f(**x): # параметры в словаре, удобно для именованых параметров
#     print(x)
#
# f(a=1,b=2,c=3)
import math


def log(func):
    def add_log_to_func(self,*args):
        print('Будет запущена функция',func.__name__,'с параметрами',args)
        result = func(self,*args)
        print('Функция', func.__name__, 'была успешно выполнена, получен результат:', result)
    return add_log_to_func


class Calculator:
    @log
    def show_sum(self,a,b):
        print(f"{a} + {b} = {a+b}")
        return a+b
    @log
    def show_mult(self,a,b):
        print(f"{a} * {b} = {a*b}")
        return a*b

obj = Calculator()
obj.show_sum(1,2)
print("*" * 50)
obj.show_mult(2,3)

math.pi



