"""Cоздать JSON-документ с информацией о сотрудниках.
Обновить зарплату сотрудника, который имеет максимальный оклад на среднюю зарплату и
записать изменения в файл"""
import json
from pprint import pprint
salaries = {
    "staff":[
        {
            "person":"Ivanovchenko",
            "salary":500
        },
        {
            "person":"Petrovchenko",
            "salary":900
        },
        {
            "person":"Sidorovchenko",
            "salary":1000
        },
        {
            "person": "Semenovchenko",
            "salary": 100
        },
        {
            "person": "Viktorovchenko",
            "salary": 2000
        },
    ]
}
pprint(salaries)

staff = salaries["staff"]
# 1. Находим среднюю зарплату
avg_salary = sum(emp["salary"] for emp in staff) / len(staff)
print(f"Средняя зарплата работников равна", avg_salary)

# 2. Находим максимальную зарплату
max_salary = max(emp["salary"] for emp in staff)
print(f"Максимальная зарплата работников равна", max_salary)

# 3. Заменяем максимальную на среднюю
for emp in staff:
    if emp["salary"] == max_salary:
        emp["salary"] = avg_salary

# 4. Сохраняем в файл
with open("salaries.json", "w", encoding="utf-8") as f:
    json.dump(salaries, f, ensure_ascii=False, indent=4)
print(salaries)