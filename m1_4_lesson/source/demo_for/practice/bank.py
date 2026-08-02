import random

clients = ['Василий','Игорь','Роман','Алексей','Анна']

# Функция enumerate извлекает из каждого элемента списка индекс элемента и значение элемента
# for i,name in enumerate(clients,1):
#     print(f"Клиента c номером {i} зовут {name}")


# Найдем прибыль каждого клиент от вклада

for i,name in enumerate(clients,1):
    money = random.randint(100_000,1000_000) #сумма клиента
    rate = 17 if money > 500_000 else 15 #процентная ставка
    years = random.randint(1,5) #срок вклада от 1 до 6
    print(f"Клиент №{i}: {name}, сумма вклада: {money},срок вклада: {years}, ставка: {rate}")
    print("-"*40) #сделаем отступ в 40 дефисов
    # Делаем цикл по годам
    for year in range(1,years + 1):
        profit = money * rate / 100
        money += profit
        print(f"Клиент {name} за {year} год заработал {round(profit,2)}, сумма стала: {round(money,2)}")
    print("*" * 40)