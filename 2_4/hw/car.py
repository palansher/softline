from typing import Optional
from components import Engine, Body, Transmission, Turbo, RemoteStart

# --- Основной класс Продукта ---

class Car:
    """Класс автомобиля, содержащий все возможные комплектующие."""

    def __init__(self) -> None:
        self.engine: Optional[Engine] = None
        self.body: Optional[Body] = None
        self.transmission: Optional[Transmission] = None
        self.turbo: Optional[Turbo] = None
        self.remote_start: Optional[RemoteStart] = None

    def show_car_info(self) -> None:
        """Выводит информацию о комплектации автомобиля."""
        print("\n" + "="*30)
        print("ХАРАКТЕРИСТИКИ АВТОМОБИЛЯ:")
        components = [
            self.body, self.engine, self.transmission, 
            self.turbo, self.remote_start
        ]
        for item in components:
            if item:
                print(f" - {item}")
        print("="*30 + "\n")
