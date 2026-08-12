import numpy as np

list1 = [1, 2, 3]
list2 = [4, 5, 6]

# Конкатенация обычных списков Python
print(list1 + list2)
# Вывод: [1, 2, 3, 4, 5, 6]

# Поэлементное суммирование через zip
# Но это ресурсозатратно, поэтому используем NumPy.
sum_list = [a + b for a, b in zip(list1, list2)]  # noqa: B905
print(sum_list)
# Вывод: [5, 7, 9]

# Пример №1: Поэлементное сложение массивов NumPy
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
sum_arr = arr1 + arr2
print(sum_arr)
# Вывод: [5 7 9]

# Пример №2: Векторные операции со скаляром
scalar_value = arr1 * 2 + 1
print(scalar_value)
# Вывод: [3 5 7]

# Практика: Двумерный массив и возведение элементов в квадрат
matrix_2n = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(matrix_2n.shape)
# Вывод: (3, 3)

s = matrix_2n**2
print(s)
# Вывод:
# [[ 1  4  9]
#  [16 25 36]
#  [49 64 81]]
