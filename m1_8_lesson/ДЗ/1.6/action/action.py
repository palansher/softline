def authorize(admins):
    login = input('Введите логин: ').strip()
    password = input('Введите пароль: ').strip()

    for admin in admins:
        if admin['login'] == login and admin['password'] == password:
            print('Авторизация успешна. Вы вошли как администратор.')
            return True

    print('Нет доступа')
    return False


def get_max_id(items):
    return max([item['id'] for item in items])



def show_items(items):
    for item in items:
        print(f'Автомобиль {item["title"]} стоит {item["price"]} (ID = {item["id"]})')
    print("=" * 100)


def create_item(items):
    title = input('Введите название авто')
    price = int(input('Введите стоимость авто'))
    id = get_max_id(items) + 1
    new_item = {
        'title': title,
        'price': price,
        'id': id
    }
    items.append(new_item)
    print('Товар успешно добавлен в каталог!')

def delete_item(items, cart):
    id_removed = int(input('Введите ID товара, который требуется удалить'))
    for item in items:
        if item['id'] == id_removed:
            items.remove(item)
            print('Товар успешно удален из каталога!')
            for cart_item in cart:
                if cart_item['id'] == id_removed:
                    cart.remove(cart_item)
                    print('Товар успешно удален из корзины!')
            break
    else:
        print('Товар не найден!')


def change_item(items):
    """Изменение стоимости товара"""
    id_edit = int(input('Введите ID товара, для которого меняем цену\n'))
    for item in items:
        if item['id'] == id_edit:
            item['price'] = int(input('Введите новую цену'))
            print('Стоимость товара обновлена!')
            break
    else:
        print("Вы ввели несуществующий ID")


def add_cart(items, cart):
    ID = int(input('Введите ID товара, который желаете добавить в корзину\n'))
    for item in items:
        if item['id'] == ID: #проверяем, что товар есть в каталоге, т.е. ввели корректный ID
            for cart_item in cart: #пытаемся найти товар в корзине
                if cart_item['id'] == ID: #если товар найден в корзине, то увеличиваем свойство количество на 1
                    cart_item['quantity'] += 1
                    break
            else: #если товар в корзине не найден, т.е. добавляем впервые
                cart.append({
                    'id': ID,
                    'quantity': 1
                })
            print("Товар добавлен в корзину!")
            break
        else:
            print("Ввели несуществующий ID")


def get_item_by_id(id, items):
    for item in items:
        if item['id'] == id:
            return item



def show_cart(items, cart):
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
    print("Итоговая стоимость покупки с учетом всех товаров:",common_price)