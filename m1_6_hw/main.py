from actions import *

from objects import admins, products

"""
Доработать консольный интернет-магазин:

1) Сделать функцию login, в которой вводите логин и пароль и сравниваете введенные значения с элементами
admins.
Если пользователь админ, то он может запускать методы по управлению товарами
(add, delete, change), а если он не админ, то выводим сообщение -нет доступа.

2) После первой проверки авторизации в дальнейшем спрашивать логин и пароль уже не нужно.

3) Все функции вынести в отдельный модуль (модули).
"""

is_admin_authorized = False  # Статус: залогинен админ или нет

print(f"Выберите действие\n")

while True:
    answer = int(input(MENU))

    match answer:
        case 1:
            show_items()

        case 2 | 3 | 4:  # Группируем админские действия
            if not is_admin_authorized:
                is_admin_authorized = login(admins)  # Пытаемся войти

            if is_admin_authorized:
                if answer == 2:
                    create_item()
                elif answer == 3:
                    delete_item()
                elif answer == 4:
                    change_item()
            else:
                print("Ошибка: Доступ запрещен (нужны права админа)")

        case 5:
            add_cart()
        case 6:
            show_cart()
        case 7:
            print("До свидания.")
            break
        case _:
            print('Вы ввели некорректный пункт меню')
