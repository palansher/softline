import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.interchange.dataframe_protocol import DataFrame

# Пример №1 (Создание простого объекта DataFrame)


# data = {
#     'apples':[2,3,1,5],
#     'oranges':[3,1,2,7]
# }

# df = pd.DataFrame(data)
# print(df)

# Пример №2 (Поменяем индексы на ключи)

# df = pd.DataFrame(data,index=['Иван','Анна','Олег','Игорь'])
# print(df)
# print(df.loc['Анна'])

# Пример №3 (фильтрация)
info = {
    "Имя":['Анна','Игорь','Алексей','Андрей'],
    "Город":['Москва','Саратов','Омск','Москва'],
    "Возраст":[25,30,29,50]
}

df = pd.DataFrame(info)

# Фильтрация по возрасту

# print(df[df['Возраст'] > 25])

# Найдем средни возраст по городам
# Группировка данных
# print(df.groupby('Город')['Возраст'].mean())

# Работа с внешними данными
animals = pd.read_csv('animals.csv')
# print(animals.info()) #мета информация о полученных данных

# Визуализация данных
# animals['water_need'].plot.box()
# plt.title('Тестовый график')
# plt.show()

# Базовые операции с DataFrame
# print(animals.count()) #получим количество элементов в каждом столбце
# print(animals.water_need.max()) #макс. значение в столбце water_need
# print(animals.water_need.mean())
# print(animals['water_need'].value_counts()) #количество повторений элементов

# print(animals.head(3)) #Берем первые 3 строки
print(animals.tail(3)) #Берем последние 3 строки