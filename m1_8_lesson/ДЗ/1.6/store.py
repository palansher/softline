"""Консольный интернет-магазин"""


# 1)
# Сделать функцию, в которой вводите логин и пароль и сравниваете введенные значения с элементами admins. Если
# пользователь админ, то он может запускать методы по управлению товарами(add,delete,change), а если он не админ,
# то выводим сообщение - нет доступа.

# 2) После первой проверки авторизации в дальнейшем спрашивать логин и пароль уже не нужно

# 3) Все функции вынести в отдельный модуль. Кроме функций в модуле не должно быть ничего

from data.store_data import admins, items
from action.action import *


cart = []

MENU = f"""{'*'*100}
1) Показать товары каталога\n2) Добавить товар в каталог\n3) Удалить товар из каталога
4) Изменить стоимость товара\n5) Добавить товар в корзину покупок\n6) Вывести корзину\n7) Выход\n{'*'*100}\n"""

is_admin = False

while True:
    answer = int(input(MENU))
    match answer:
        case 1:
            show_items(items)
        case 2:
            if not is_admin:
                is_admin = authorize(admins)
            if is_admin:
                create_item(items)
        case 3:
            if not is_admin:
                is_admin = authorize(admins)
            if is_admin:
                delete_item(items, cart)
        case 4:
            if not is_admin:
                is_admin = authorize(admins)
            if is_admin:
                change_item(items)
        case 5:
            add_cart(items, cart)
        case 6:
            show_cart(items, cart)
        case 7:
            break
        case _:
            print('Вы ввели некорректный пункт меню')