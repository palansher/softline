"""
Создать JSON-документ с информацией о сотрудниках.
Обновить зарплату сотрудника, который имеет максимальный оклад на среднюю зарплату и записать изменения в файл.
"""


# будем хранить деньги в десятичной строке для точности с округлением
import json
from decimal import Decimal, ROUND_HALF_EVEN

json_file_name="data.json"

# Создаем список с Decimal
employees = [
    {"first_name": "Иван", "last_name": "Иванов", "salary": Decimal("50000.00")},
    {"first_name": "Анна", "last_name": "Каренина", "salary": Decimal("120000.00")},
    {"first_name": "Петр", "last_name": "Петров", "salary": Decimal("80000.00")}
]

# Функция для записи: превращаем Decimal в строку для сохранения в json (который не понимает decimal)
def decimal_to_str(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    return obj

### Сохраняем в JSON
# что делает default=
# json.dump не понимает тип decimal. И при default=decimal_to_str, когда встречается неизвестный тип данных, то делает что-то вроде:
# если встретишь штуковину, которую не умеешь записывать в JSON, то прогони её через функцию decimal_to_str, и записывай то, что она вернет.
with open(json_file_name, 'w', encoding='utf-8') as json_file:
    json.dump(employees, json_file, indent=4, ensure_ascii=False, default=decimal_to_str)

# Читаем JSON обратно для изменения
with open(json_file_name, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Преобразуем зарплаты обратно из строки в Decimal для расчетов
for employee in data:
    employee['salary'] = Decimal(employee['salary'])

# Считаем среднюю зарплату и округляем её (ибо получим float)
all_salaries = [employee['salary'] for employee in data]
# Оборачиваем все деление в Decimal и даже применяем банковское округление :) для прикола и точности
avg_salary = Decimal(sum(all_salaries) / len(all_salaries)).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)


# Находим сотрудника с макс. окладом
max_worker = max(data, key=lambda x: x['salary'])
max_worker['salary'] = avg_salary

# Снова сохраняем в JSON, превращая Decimal в строки
with open(json_file_name, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False, default=decimal_to_str)

print(f"Вау! В файле {json_file_name} зарплата для {max_worker['last_name']} теперь {avg_salary} денег")
