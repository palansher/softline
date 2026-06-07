from objects import *


def login(admins_list: list) -> dict[str, int | str] | None:
    username = input("Введите логин: ")
    password = input("Введите пароль: ")

    for admin in admins_list:
        if admin['username'] == username and admin['password'] == password:
            print(f"Добро пожаловать, {username}!\n")
            return True

    print("Неверный логин или пароль.")
    return False


def get_product(product_id: int) -> dict | None:
    # Возвращаем первый совпавший объект или None
    for item in products:
        if item['id'] == product_id:
            return item
    return None

def get_max_id():
    return max([item['id'] for item in products])


def show_items():
    print("Товары в каталоге:\n")
    for item in products:
        print(f'Автомобиль {item["title"]} стоит {item["price"]} (ID = {item["id"]})')
    print("=" * 100)


def create_item():
    title = input('Введите название авто: ')
    price = int(input('Введите стоимость авто: '))
    id = get_max_id() + 1
    new_item = {
        'title': title,
        'price': price,
        'id': id
    }
    products.append(new_item)
    print("Товар { new_item.title } успешно добавлен в каталог!")


def delete_item():
    id_removed = int(input('Введите ID товара, который требуется удалить'))
    for item in products:
        if item['id'] == id_removed:
            products.remove(item)
            print('Товар успешно удален из каталога!')
            for cart_item in cart:
                if cart_item['id'] == id_removed:
                    cart.remove(cart_item)
                    print('Товар успешно удален из корзины!')
            break
    else:
        print('Товар не найден!')


def change_item():
    """Изменение стоимости товара"""
    id_edit = int(input('Введите ID товара, для которого меняем цену\n'))
    for item in products:
        if item['id'] == id_edit:
            item['price'] = int(input('Введите новую цену'))
            print('Стоимость товара обновлена!')
            break
        else:
            print("Вы ввели несуществующий ID")
            break


def add_cart():
    """ Добавление товара в корзину """

    product_found_in_catalog = False

    # просим повторять ввод, если ID нет в каталоге
    while not product_found_in_catalog:
        show_items
        answer = input("Введите ID товара, который желаете добавить в корзину или '<' для выхода в меню\n")
        if answer == '<' : return
        ID = int(answer)
        if not ID in [item['id'] for item in products]:  # проверяем, что товар есть в каталоге, т.е. ввели корректный IDs
            print(f"ID {ID} в каталоге не существует!")
            continue
        else: product_found_in_catalog = True

    # Товар точно есть в каталоге
    for cart_item in cart:  # пытаемся найти товар в корзине
        if cart_item['id'] == ID:  # если товар найден в корзине, то увеличиваем свойство количество на 1
            print(f"товар {get_product(ID)['title']} (ID={ID}) найден в корзине, увеличиваем количество на 1")
            cart_item['quantity'] += 1
            return

    # если товар в корзине не найден, т.е. добавляем впервые
    cart.append({
        'id': ID,
        'quantity': 1
    })
    print(f"товар {get_product(ID)['title']} (ID={ID}) не найден в корзине и добавлен")


def get_item_by_id(id):
    for item in products:
        if item['id'] == id:
            return item


def show_cart():
    """Вывод корзины покупок"""
    common_price = 0
    for item_cart in cart:
        # получили товар по ID из каталога, чтобы иметь возможность вывести название и цену
        item = get_item_by_id(item_cart['id'])
        if item:
            res = item['price'] * item_cart['quantity']
            common_price += res
            print(f"Товар {item['title']} по цене {item['price']} добавлен в корзину {item_cart['quantity']} раз"
                  f" на сумму {res}")
    print("Товары в корзине:")
    print("Итоговая стоимость покупки с учетом всех товаров:", common_price)
