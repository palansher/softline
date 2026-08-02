from abc import ABC, abstractmethod
from car import Car
from components import Engine, Body, Transmission, Turbo, RemoteStart

# --- Абстрактный и Конкретный Строители ---

class CarBuilder(ABC):
    """Интерфейс строителя, определяющий этапы сборки."""
    
    @abstractmethod
    def reset(self) -> None:
        """
        Сброс состояния строителя для создания нового объекта.
        Без reset() вторая машина, которую начнем собирать, унаследует детали от первой
                
        Паттерн «Строитель» подразумевает, что один и тот же экземпляр ConcreteCarBuilder может использоваться 
        многократно для производства целой серии машин.
        reset гарантирует, что в self._car всегда находится новый, «пустой» объект.
        
        - нужен чтобы каждый раз не создавать новый экземпляр строителя для каждой новой машины
        - избавляет от необходимости вручную «обнулять» строителя
        """
        pass

    @abstractmethod
    def install_engine(self, hp: int) -> None:
        """Этап установки двигателя."""
        pass

    @abstractmethod
    def install_body(self, body_type: str) -> None:
        """Этап установки кузова."""
        pass

    @abstractmethod
    def install_transmission(self, gears: int, auto: bool) -> None:
        """Этап установки трансмиссии."""
        pass

    @abstractmethod
    def install_turbo(self) -> None:
        """Опциональный этап: турбонаддув."""
        pass

    @abstractmethod
    def install_remote_start(self) -> None:
        """Опциональный этап: автозапуск."""
        pass

    @abstractmethod
    def get_result(self) -> Car:
        """Показ готового экземпляра автомобиля."""
        pass


class ConcreteCarBuilder(CarBuilder):
    """Реализация конкретного процесса сборки."""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._car = Car()

    def install_body(self, body_type: str) -> None:
        print(f"[Этап 1] Установка кузова: {body_type}")
        self._car.body = Body(body_type)

    def install_engine(self, hp: int) -> None:
        print(f"[Этап 2] Установка двигателя мощностью {hp} л.с.")
        self._car.engine = Engine(hp)

    def install_transmission(self, gears: int, auto: bool) -> None:
        t_type = "автоматической" if auto else "механической"
        print(f"[Этап 3] Монтаж {t_type} трансмиссии ({gears} ст.)")
        self._car.transmission = Transmission(gears, auto)

    def install_turbo(self) -> None:
        print("[Опция] Установка турбонаддува")
        self._car.turbo = Turbo()

    def install_remote_start(self) -> None:
        print("[Опция] Установка системы дистанционного запуска")
        self._car.remote_start = RemoteStart()

    def get_result(self) -> Car:
        product = self._car
        self.reset()
        return product

