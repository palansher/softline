from random import randint

def show_salaries(salaries:list)->None:
    for i,salary in enumerate(salaries,1):
        print(f"{i}. {salary}")
    print("*"*50)
    print("Максимальный оклад:", max(salaries))
    print("Минимальный оклад:", min(salaries))
    print("Общая сумма для оплаты з/п", sum(salaries))
    print("Средняя з/п", sum(salaries) / len(salaries))

def get_salaries(address:str, count:int)->list:
    print(f"В офисе по адресу {address} работают {count} сотрудников>")
    return [randint(50_000,300_000) for _ in range(count)]
