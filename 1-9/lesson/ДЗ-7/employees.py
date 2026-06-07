import json

employees = [
    {"first_name": "Алиса", "last_name": "Иванова", "position": "Специалист по рискам", "salary": 210_000},
    {"first_name": "Алексей", "last_name": "Алексеевич", "position": "Программист", "salary": 385_000},
    {"first_name": "Дарья", "last_name": "Тимофеева", "position": "Руководитель проектов", "salary": 200_000},
    {"first_name": "Александр", "last_name": "Медведев", "position": "Специалист", "salary": 100_000},
    {"first_name": "Михаил", "last_name": "Иванов", "position": "Руководитель отдела", "salary": 475_000},
]

with open("employees.json", "w", encoding="utf-8") as file:
    json.dump(employees, file, ensure_ascii=False, indent=4)

with open("employees.json", "r", encoding="utf-8") as file:
    employees = json.load(file)

total_salary = sum(employee["salary"] for employee in employees)

average_salary = total_salary / len(employees)

# def get_max(persons):
#     max_person = person[0]
#     for i in range(1,len(persons)):
#         if max_person['salary'] < persons[i]['salary']:
#             max_person = persons[i]
#     return max_person
        

max_employee = max(employees, key=lambda employee: employee["salary"])

max_employee["salary"] = average_salary

with open("employees.json", "w", encoding="utf-8") as file:
    json.dump(employees, file, ensure_ascii=False, indent=4)

print("Средняя зарплата:", average_salary)
print("Обновленный список сотрудников записан в файл employees.json")