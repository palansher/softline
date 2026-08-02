# Пример №1

# def get_sum(a,b,*x):
#     # return a + b + sum(x)
#     s = a + b
#     for item in x:
#         s += item
#     return s
#
# print(get_sum(1,2,3,4,5))

# Пример №2
# def get_numbers():
#     return 1,2,3,(4,5,6,(7,"Тест",9))
#
# # print(get_numbers()[3][3][1])
# print(get_numbers())

# Пример №3

# calc = lambda a, b: a + b if a % 2 == 0 and b % 2 == 0 else a * b
#
# def calc_v2(a, b):
#     return a + b if a % 2 == 0 and b % 2 == 0 else a * b
#
# print(calc(2,8))

# add = lambda a, b: a + b
# dif = lambda a, b: a - b
# mult = lambda a, b: a * b
# div = lambda a, b: a / b if b != 0 else 0

# def calc(a,b,sign):
#     match sign:
#         case '+':
#             return add(a,b)
#         case '-':
#             return dif(a,b)
#         case '*':
#             return mult(a,b)
#         case '/':
#             return div(a,b)
#
# print(calc(1,2,'*'))

# Альтернативный вариант решения

# calc = lambda a, b, sign : (a + b) if sign == '+' else (a - b) if sign == '-' else (a * b) if sign == '*' else (a / b)\
#     if sign == '/' and b != 0 else 0
# print(calc(2, 0, '+'))

# print((lambda a, b, sign : (a + b) if sign == '+' else (a - b) if sign == '-' else (a * b) if sign == '*' else (a / b)\
#     if sign == '/' and b != 0 else 0)(2,10,'/'))

# Пример №4

# add = lambda a, b: a + b
#
# def calc(a,b,c):
#     return a(b,c)
#
# print(calc(add,2,3))

# Пример №5 (Вложенные функции)

# def pc(title,size_ram,size_hard,is_on=False):
#     """Описание структуры системного блока и запуск/выключение ПК"""
#     def ram():
#         info = "Модуль RAM запущен" if is_on else "Модуль RAM остановлен"
#         print(f"ПК {title} имеет размер RAM {size_ram}\n{info}")
#     def hard():
#         info = "Hard запущен" if is_on else "Hard остановлен"
#         print(f"ПК {title} имеет размер Hard {size_hard}\n{info}")
#     return ram,hard
#
# pc("Acer",8,1,True)[0]()
# pc("Acer",8,1,True)[1]()


# Пример №6(Замыкания)
# Цель замыкания - генерация новых функций

# def calc(a):
#     def get_sum(b):
#         return a + b
#     return get_sum

# print(type(calc(2)))

# sum_ten = calc(10)
# print(sum_ten(1))
# print(sum_ten(2))
# print(sum_ten(3))
#
# sum_one = calc(1)
# print(sum_one(1))
# print(sum_one(2))
# print(sum_one(3))

# Пример по замыканию №2

def domain(base_url):
    def subdomain(part_url):
        return f"{base_url}/{part_url}"
    return subdomain

site1 = domain("http://www.site.ru")
print(site1("about"))
print(site1("contacts"))
print(site1("catalog"))

site2 = domain("http://www.shop.ru")
print(site2("about"))
print(site2("contacts"))
print(site2("catalog"))