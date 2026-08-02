# map(function,iterable) - данная функция применяет функцию из первого параметра
# к каждому элементу второго параметра и возвращает новый итерируемый объект

# Пример №1

# numbers = [5,8,2,4]

# Создать новый список в котором каждый элемент является квадратом исходного списка

# Способ №1
# new_list = []
# for number in numbers:
#     new_list.append(number ** 2)

# Способ №2
# print(list(map(lambda num: num ** 2, numbers)))

# Пример №2

# langs = ['Java','JS','Python']
#
# size_langs = list(map(len,langs))
# print(size_langs)

# Пример №3
items = [["Ауди",1000],["БМВ",1200],["Лексуc",2000]]
# Преобразовать исходный список в новый списк таким образом, чтобы в новом списке было
# 3 строки: Автомобиль Ауди стоит 1000 у.е.,...

# info_items = list(map(lambda item : f'Автомобиль {item[0]} стоит {item[1]}', items))
# print(info_items)

# print("\n".join(list(map(lambda item : f'Автомобиль {item[0]} стоит {item[1]}', items))))


# Пример на повторение

my_list = [1,2,3,["test",["demodlfgjldgjld"]]]

# Получить подстроку demo из списка
print(my_list[3][1][0][:4])