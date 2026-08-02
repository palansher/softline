"""Модель данных Car."""

import uuid
from dataclasses import asdict, dataclass, field
from typing import Any

from car_brand import CarBrand


@dataclass(slots=True, frozen=True)
class Car:
    brand: CarBrand
    model: str
    year: int
    category: str
    vin: str
    color: str
    # default_factory автоматически вызывается при создании каждого нового Car()
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict[str, Any]:
        """Преобразует объект в словарь."""
        return asdict(self)
