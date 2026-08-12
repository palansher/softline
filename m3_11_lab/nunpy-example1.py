# Демонстрация извлечения подмассива из массива
from pprint import pprint

# x = [1,2,3,8,5]
# print(x[2:4])
import numpy as np

my_array = np.arange(10)
print(my_array) #[0 1 2 3 4 5 6 7 8 9]
print(my_array[:5]) #получаем элемент до индекса 5

print(my_array[::-1]) #получим элементы в обратном порядке


# Срезы в двумерном массиве
print('Срезы в двумерном массиве')
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

print(matrix[1,1]) #5

print(matrix[1,:]) #берем строку с индексом 1 все столбцы

pprint(matrix[0:2,0:2])
