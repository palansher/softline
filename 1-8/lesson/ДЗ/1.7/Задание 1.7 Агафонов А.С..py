""" Задание 1.7
Cоздать JSON-документ с информацией о сотрудниках.

Обновить зарплату сотрудника, который имеет максимальный оклад на среднюю зарплату и
записать изменения в файл.
"""
import json

# Информация о сотрудниках
employees = [
    {
        "name": "Лермонтов М.Ю.",
        "salary": 85_000
    },
    {
        "name": "Толстой Л.Н",
        "salary": 115_000
    },
    {
        "name": "Гоголь Н.В.",
        "salary": 65_000
    },
    {
        "name": "Пушкин А.С.",
        "salary": 115_000
    },
]

# Функция выводит информацию о сотрудниках
def print_employees():
    for employee in employees:
        print(f"У сотрудника {employee['name']} должностной оклад {employee['salary']}.")

# Функция возвращает среднее значение 'salary'
def get_middle_salary():
    _sum = 0
    for employee in employees:
        _sum += employee["salary"]
    return int(_sum / employees.__len__())

# Функция возвращает максимальное значение 'salary'
def get_max_salary():
    return max(employees, key=lambda employee: int(employee["salary"]))["salary"]

# Функция заменяет максимальный оклад на средний
def replace_employee_salary (_max_salary: int, _middle_salary: int):
    for employee in employees:
        if employee['salary'] == _max_salary:
            employee['salary'] = _middle_salary

def save_employees():
    with open('employees.json', 'w', encoding='utf-8') as f:
        json.dump(employees, f, indent=4, ensure_ascii=False)

print_employees()
print(f"Средний оклад по сотрудникам {get_middle_salary()}, максимальный оклад по сотрудникам {get_max_salary()}.")
# Устанавливаем работнику с максимальным окладом средний оклад
print("Меняем оклад сотруднику с максимальным окладом на средний оклад.")
replace_employee_salary(get_max_salary(), get_middle_salary())
print_employees()
save_employees()