# Рекурсия - это конструкция, которая позволяет повтоярть действия, поэтому это альтернатива циклам

# Пример №1

# Вывести числа от n до 0

# def show_numbers(n):
#     if n == 0:
#         return
#     print(n)
#     show_numbers(n - 1)
#
# show_numbers(10)
#
# Рекурсию стоит использовать именно при обходе древовидной структуры

# Пример №2 (Факториал числа)

# 5! = 1 * 2 * 3 * 4 * 5
# 5! = 5 * 4!
# n! = n * (n - 1)!

# def get_fact(n):
#     if n < 0:
#         print("Факториал для отрицательных значений не существует!")
#         return -1
#     if n == 0 or n == 1:
#         return 1
#     return n * get_fact(n-1)
#
# print(get_fact(3))



# get_fact(3) = 3 * get_fact(2) = 3 * 2 * 1 = 6

# Пример №3(рекурсия для нахождения положительной степени числа)
def get_power(a,n):
    if n < 0:
        print("Недопустимый случай в нашем примере")
        return 0
    if n == 0:
        return 1
    if n == 1:
        return a
    return a * get_power(a,n-1)

print(get_power(2,3))