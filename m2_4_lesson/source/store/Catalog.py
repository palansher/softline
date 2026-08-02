from store.Cart import Cart


class Catalog:
    def __init__(self,items):
        self.items = items

    def show_catalog(self):
        print(f"{'ID товара':^12} {'Название товара':^20} {'Стоимость товара':^18} {'Категория товара':^15}")
        for item in self.items:
            print(f"{item.id:^12} {item.title:^20} {item.price:^18} {item.category.title_category:^15}")

    def get_item_by_id(self,id):
        for item in self.items:
            if item.id == id:
                return item
        print('Товар не найден!')

    def add_to_cart(self,cart:Cart):
        while 1:
            try:
                id = int(input('Введите ID товара, который добавим в корзину или -1 для выхода'))
                if id < 0:
                    break
                item = self.get_item_by_id(id) #Товар каталога
                if item: #если товар существут с таким ID
                    cart.save_item_in_cart(id)
            except ValueError:
                print('Ввели не число')
