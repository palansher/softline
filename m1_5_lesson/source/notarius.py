clients = []

while 1:
    clients.append(input("Введите Ваше имя\n"))
    if len(clients) == 5:
        print(f"Может войти {clients.pop(0)}, готовится {clients[0]}")