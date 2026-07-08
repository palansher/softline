import pandas as pd

animals = pd.read_csv('animals.csv')

# Получаем всех львов
# print(animals[animals['animal'] == 'lion'])

# Получаем количество львов
# print(len(animals[animals['animal'] == 'lion']))

# Получаем всех зебр, которые 200 литров воды
# print(animals[(animals['animal'] == 'zebra') & (animals['water_need'] <= 200)])

# Получаем уникальный список всех животных

# print((animals['animal'].unique())) #получаем уникальный список элементов

# Получить по каждому виду животных среднее значение
# avg_water1 = animals.groupby('animal')['water_need'].mean()
# avg_water2 = animals.groupby('animal')['water_need'].median()
# print(avg_water1)
# print(avg_water2)

# Чтение данных из CSV файла в котором нет заголовков
grid = pd.read_csv('pandas_tutorial_read.csv',delimiter=';',
                   names=['date_create','access','id_country','session_id','role','location'])

# print(grid[['location','access']]) #если берем более одного поля из DataFrame, то обязательны двойные скобки

# Получаем первые 5 записей, где страна Африка
print(grid[grid['location']=='Africa'].head(5))