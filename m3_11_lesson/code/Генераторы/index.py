# def f(n):
#     i = 0
#     my_list = []
#     while i <= n:
#         my_list.append(i)
#         i += 1
#     return my_list
# print(f(10))

# Если n большое число и список требуется лишь для одноразового чтения данных, то вместо списков
# оптимальнее использовать генераторы. Генератор - это специальный обхект, который в один момент времени
# хранит лишь одно значение, которое можно считать через функцию next. После получения из генератора
# текущего значения, это значение удаляется, то есть повторно его получить не получится. Плюс генератора в том,
# что не нужно в памяти хранить огромные списки.

# def f(n):
#     i = 1
#     while i <= n:
#         yield i #оператор yield возвращает одно значение и приостанавливает функцию
#         i += 1
#
# my_generator = f(3)
# print(next(my_generator))
# print(next(my_generator))
# print(next(my_generator))
# print(next(my_generator))

# Пример №2 (читаем текстовый документ)

def read_file(filename):
    with open(filename,'r') as f:
        for line in f:
            yield line.strip()

gen = read_file('1.txt')
print(next(gen))
print(next(gen))
print(next(gen))