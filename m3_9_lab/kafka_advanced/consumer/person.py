"""Модель данных Person."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class Person:
    """Сущность человека, получаемая из Kafka."""

    id: int
    firstname: str
    lastname: str
    salary: int

    def to_dict(self) -> dict[str, Any]:
        """Преобразует объект Person в словарь."""
        return asdict(self)
