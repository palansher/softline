from factory import Factory


from dealer import Dealer


from order import Order



models_factory = ['Гранта', 'Нива', 'Ларгус', 'Веста']


factory = Factory(title_factory='АвтоВаз', models_factory=models_factory)


count = 30


title_models = ['Гранта', 'Веста', 'Нива', 'Ларгус', 'Ауди']


order = Order(title_models=title_models, count_cars=count, factory=factory)


dealer = Dealer('Элвис', 20)

dealer.create_order(order)

