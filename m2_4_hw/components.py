# --- Классы компонентов автомобиля ---

class Engine:
    def __init__(self, horsepower: int):
        self.horsepower = horsepower

    def __str__(self) -> str:
        return f"Двигатель ({self.horsepower} л.с.)"


class Body:
    def __init__(self, body_type: str):
        self.body_type = body_type

    def __str__(self) -> str:
        return f"Кузов ({self.body_type})"


class Transmission:
    def __init__(self, gears: int, is_automatic: bool):
        self.type = "АКПП" if is_automatic else "МКПП"
        self.gears = gears

    def __str__(self) -> str:
        return f"Трансмиссия ({self.type}, {self.gears} ст.)"


class Turbo:
    def __str__(self) -> str:
        return "Турбонаддув установлен"


class RemoteStart:
    def __str__(self) -> str:
        return "Система автозапуска установлена"
