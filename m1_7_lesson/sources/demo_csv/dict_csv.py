import csv

cars = [
    {"title":"Audi","price":1000,"color":"Белый"},
    {"title":"BMW","price":1200,"color":"Черный"},
    {"title":"VW","price":900,"color":"Синий"},
]

# with open('cars.csv', 'w',encoding='utf-8',newline='') as file:
#     obj = csv.DictWriter(file,fieldnames=cars[0].keys())
#     obj.writeheader()
#     obj.writerows(cars)

with open('cars.csv', 'r',encoding='utf-8',newline='') as file:
    reader = csv.DictReader(file)
    for row in reader: #каждая строка теперь словарь
        print(f"{row["title"]} стоит {row["price"]}")