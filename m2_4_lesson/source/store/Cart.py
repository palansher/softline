from typing import List

from store.Item import Item
from store.ItemCart import ItemCart


class Cart:
    def __init__(self):
        self.items_cart:List[ItemCart] = []

    def show_cart(self,catalog):
        if self.items_cart:
            print('Корзина покупок:')
            print(f"{'ID товара':^12} {'Название товара':^20} {'Стоимость товара':^18}"
                  f" {'Количество товаров':^15} {'Общая цена товара':^15}")
        s = 0
        for item in self.items_cart:
            item_full_info = catalog.get_item_by_id(item.id) #получаем товар каталога
            if item_full_info:
                print(f"{item.id:^12} {item_full_info.title:^20} {item_full_info.price:^18}"
                      f" {item.quantity:^15} {item.quantity * item_full_info.price:^15}")
                s += item.quantity * item_full_info.price
        print('Общая сумма всех добавленных в корзину товаров:',s)
    def save_item_in_cart(self,item_id):
        for item in self.items_cart:
            if item.id == item_id: #если нашли в корзине товар с ID, который хотим купить, т.е. он уже был в корзине
                item.quantity += 1 #у существующего товар увеличиваем количество на 1
                break
        else:
            self.items_cart.append(ItemCart(item_id,1))
        print('Товар добавлен в корзину')