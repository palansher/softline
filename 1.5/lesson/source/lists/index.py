# Пример №1
# my_list = [1,2,3,4,5]
# my_list_v2 = my_list * 3
# print(my_list_v2)
import random

# Пример №2
# test = [1,2,3,[4,5,[6,7]]]
# print(test[-1][-1][-1])

# Пример №3 (добавление элементов через append)

# my_list = []
# for _ in range(10):
#     my_list.append(random.randint(1, 100))
# print(my_list)

# Альтернативное решение по заполнению списка через генератор

my_list = [random.randint(1, 100) for _ in range(10)]
# print(my_list)
# my_list_even = [item for item in my_list if item % 2 == 0]
# print(my_list_even)

# Пример №4(Сортировка списка)
# 1) Используем универсальную функцию sorted
# sorted_list = sorted(my_list,reverse=True)
# print(sorted_list)

# 2) Метод sort
# my_list.sort()
# print(my_list)

# Пример №5 (Обход списка)
# langs = "PHP,JS,C++,C#"
# langs_list = langs.split(",")
# for i,lang in enumerate(langs_list,1):
#     print(f"{i}. {lang}")

# Пример №6 (добавление элемента в произвольное место)
# my_list.insert(0,777)
# print(my_list)

# Пример №7

# Удаление элемента из списка осуществляется либо через pop, либо
# через remove.

# 1) pop() - удаление последнего элемента в списке
# 2) pop(index) - удаление элемента по индексу

test = [1,2,3,2,5,1,7,1]
# removed_item = test.pop()
# print(removed_item)
# print(test)

# 3) remove - это удаление элемента по значению В отличие от pop
# метод remove не возвращает удаленный элемент

# test.remove(2) #[1, 3, 4, 5]

# Метод remove нельзя применять для несуществующих значений списка.
# rem_item = 2
# if rem_item in test:
#     test.remove(rem_item)
#     print(test)
# else:
#     print("Нельзя удалить несуществующий элемент")

# Удаляем со всеми дубликатами
# while rem_item in test:
#     test.remove(rem_item)
# print(test)

# Пример №8

# Метод count - возвращает количество найденных элементов

# print(test.count(1))

# Пример №9
a = [1,2,3]
b = [5,3,1]
# Расшим список a значениями из списка b
# a.extend(b)
# print(a) #[1, 2, 3, 5, 3, 1]

# Создание нового списка на базе сущесвующих
c = a + b
print(c)