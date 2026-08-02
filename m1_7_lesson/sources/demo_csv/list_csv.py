import csv

persons = [
    ["Иван",80_000],
    ["Алексей",280_000],
    ["Анна",180_000],
]

# Запись в CSV документ

# with open('persons.csv', 'w',encoding='utf-8',newline='') as file:
#     obj = csv.writer(file) #подготовили объект писателя, который умеет записывать список в файл csv
#     obj.writerows(persons)

# Добавление нового сотрудника документ

# with open('persons.csv', 'a',encoding='utf-8',newline='') as file:
#     obj = csv.writer(file) #подготовили объект писателя, который умеет записывать список в файл csv
#     obj.writerow(['Андрей',145000])

# Получение данных из CSV
with open('persons.csv', 'r',encoding='utf-8',newline='') as file:
    obj = csv.reader(file,delimiter=";") #подготовили объект писателя, который умеет записывать список в файл csv
    for row in obj:
        print(f'{row[0]} зарабатывает {row[1]}')