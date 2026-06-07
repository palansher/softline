from builder import CarBuilder


"""
Директор (управляет процессом)

Директору нужен только интерфейс CarBuilder, чтобы знать, какие методы сборки можно вызывать. 
Ему не нужно знать о конкретной реализации.
Решает, какую именно машину собирать.

Хранит в себе алгоритмы сборки популярных конфигураций.
Директор гарантирует, что этапы сборки пройдут в правильной последовательности (например, двигатель только после кузова).

Без директора, ответственность за сборку ложится на клиента (то есть на main.py)

Директор полезен когда автомобили типовые.

Он не нужен, если мы хотим использовать Fluent Interface (цепочку вызовов), где клиент сам накидывает детали:
car = builder.add_engine(200).add_turbo().get_result()

"""

class Director:
    """Класс, знающий 'рецепты' сборки разных конфигураций."""

    def construct_sport_car(self, builder: CarBuilder) -> None:
        builder.install_body("Купе")
        builder.install_engine(450)
        builder.install_transmission(7, True)
        builder.install_turbo()

    def construct_suv(self, builder: CarBuilder) -> None:
        builder.install_body("Внедорожник")
        builder.install_engine(250)
        builder.install_transmission(6, True)
        builder.install_remote_start()
