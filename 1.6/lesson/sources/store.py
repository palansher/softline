"""Консольный интернет-магазин"""

admins = [
    {
        'login':'admin',
        'password':'123',
    },
    {
        'login':'root',
        'password':'321'
    }
]

# 1)
# Сделать функцию, в которой вводите логин и пароль и сравниваете введенные значения с элементами admins. Если
# пользователь админ, то он может запускать методы по управлению товарами(add,delete,change), а если он не админ,
# то выводим сообщение - нет доступа.

# 2) После первой проверки авторизации в дальнейшем спрашивать логин и пароль уже не нужно

# 3) Все функции вынести в отдельный модуль. Кроме функций в модуле не должно быть ничего

items = [
    {
        'id':1,
        'title':'Audi',
        'price':1000
    },
    {
        'id':2,
        'title':'BMW',
        'price':1500
    },
    {
        'id':3,
        'title':'VW',
        'price':900
    }
]

cart = []

MENU = f"""{'*'*100}
1) Показать товары каталога\n2) Добавить товар в каталог\n3) Удалить товар из каталога
4) Изменить стоимость товара\n5) Добавить товар в корзину покупок\n6) Вывести корзину\n7) Выход\n{'*'*100}\n"""


def get_max_id():
    return max([item['id'] for item in items])



def show_items():
    for item in items:
        print(f'Автомобиль {item["title"]} стоит {item["price"]} (ID = {item["id"]})')
    print("=" * 100)


def create_item():
    title = input('Введите название авто')
    price = int(input('Введите стоимость авто'))
    id = get_max_id() + 1
    new_item = {
        'title': title,
        'price': price,
        'id': id
    }
    items.append(new_item)
    print('Товар успешно добавлен в каталог!')

def delete_item():
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


def change_item():
    """Изменение стоимости товара"""
    id_edit = int(input('Введите ID товара, для которого меняем цену\n'))
    for item in items:
        if item['id'] == id_edit:
            item['price'] = int(input('Введите новую цену'))
            print('Стоимость товара обновлена!')
            break
    else:
        print("Вы ввели несуществующий ID")


def add_cart():
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


def get_item_by_id(id):
    for item in items:
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
    print("Итоговая стоимость покупки с учетом всех товаров:",common_price)


while True:
    answer = int(input(MENU))
    match answer:
        case 1:
            show_items()
        case 2:
            create_item()
        case 3:
            delete_item()
        case 4:
            change_item()
        case 5:
            add_cart()
        case 6:
            show_cart()
        case 7:
            break
        case _:
            print('Вы ввели некорректный пункт меню')