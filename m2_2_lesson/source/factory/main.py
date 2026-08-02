from factory.Diller import Diller
from factory.Factory import Factory
from factory.Order import Order


models_factory = ['Гранта','Нива','Веста','Ларгус']
factory = Factory("АвтоВаз",models_factory)
count = 30
title_models = ['Гранта','БМВ','Порше','Ларгус']
# Делаем объект со всей информацией о заказе
order = Order(title_models, count,factory)

diller = Diller("Элвис",20)
diller.create_order(order)

# 1) Если поступает некорректный заказ, необходимо сообщить, что нет технической возможности изготовить
# 2) Вывести информацию сколько было создано каждой модели. То есть, Гранта: 7ед, Веста: 10ед...


# ДЗ - учесть скидку 10% на стоимость каждой машины, если срок работы дилера более 10 лет