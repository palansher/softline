import pandas as pd

animals = pd.read_csv("animals.csv")

### Получаем всех львов
# print(animals[animals["animal"] == "lion"])

### Получаем количество львов
# количество по каждому столбцу
# print(animals[animals["animal"] == "lion"].count())
# print('\n')
# общее количество одним значением
# print(len(animals[animals['animal'] == 'lion']))

### Получаем всех зебр, которые пьют меньше 200 литров воды
# два условия используем оператор and (&)
# print(animals[(animals['animal'] == 'zebra') & (animals['water_need'] <= 200)])

### Получаем уникальный список всех животных

# print(animals['animal'].unique()) #получаем уникальный список элементов

### Получить по каждому виду животных среднее значение потребления воды
# используем группировку
# avg_water1 = animals.groupby('animal')['water_need'].mean()
# avg_water2 = animals.groupby('animal')['water_need'].median()
# print(avg_water1)
# print(avg_water2)

### Чтение данных из CSV файла в котором нет заголовков
grid = pd.read_csv(
    "pandas_tutorial_read.csv",
    delimiter=";",
    # Задаем название столбцов, если в CSV нет заголовков, придумываем сами.
    names=["date_create", "access", "id_country", "session_id", "role", "location"],
)

# по умолчанию получаем первые пять и последние пять элементов в выводе в консоли
print(
    grid[["location", "access"]]
)  # если берем более одного поля из DataFrame, то обязательны двойные скобки

### Получаем первые 5 записей, где страна Африка
# Первый grid – это обращение к объекту датафрейм.
# Затем, чтобы взять элемент этого датафрейма, нужно опять обратиться к этому элементу через объект датафрейм, тот же grid.
# Внутри скобок мы указываем условие. А чтобы указать условия по элементу датафрейм, нужно опять обратиться к датафрейм.
print(grid[grid["location"] == "Africa"].head(5))
