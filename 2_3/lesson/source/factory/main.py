from factory.Diler import Diler
from factory.Factory import Factory
from factory.Order import Order

factory = Factory("АвтоВаз",['Гранта','Веста','Нива'])
diler = Diler("VipCar",15)

count_cars = 30 #заказываем 30 авто
title_models = ['Гранта','Веста','Audi',"BMW X5"]
order = Order(count_cars,title_models,factory)

diler.create_order(order)

# 1) При заказе некорректной модели выводить сообщение, что нет
# технической возможности изготовить данное авто