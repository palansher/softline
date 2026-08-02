from store.Cart import Cart
from store.Catalog import Catalog
from store.Category import Category
from store.Item import Item

category1 = Category('Российские авто')
category2 = Category('Импортные авто')

item1 = Item('ВАЗ',1000,category1)
item2 = Item('УАЗ',1400,category1)
item3 = Item('ГАЗ',1300,category1)

item4 = Item('BMW',5000,category2)
item5 = Item('KIA',4000,category2)
item6 = Item('JAC',3000,category2)

cars = [item1,item2,item3,item4,item5,item6]

catalog = Catalog(cars)
catalog.show_catalog()

print('Добавление товара в корзину:')
cart = Cart()
catalog.add_to_cart(cart)

cart.show_cart(catalog)