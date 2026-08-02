"""Создать с помощью паттерна Строитель автомобиль.
У Автомобиля могут быть свойства: двигатель, кузов, трансмиссия, турбина, автозапуск и др. свойства.
Построить кастомный автомобиль"""

from CreateAuto import CreateAuto
# создаем обьект автомобиль с вызовом методом по созданию каждого элемента
auto = CreateAuto('VW')

# обязательные опции
auto.create_kuzov('Универсал').create_shassi('Монокок').create_transmission('Автоматическая')
auto.create_glass('Триплекс с тонировкой').create_engine('Бензиновый')

# дополнительные опции
auto.mount_condition('Gree')
auto.mount_kovriki('Eva')
auto.mount_signal('Pantera')

# вывод информации об автомобиле
auto.show_info_Auto()
