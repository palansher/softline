"""Модель данных CarBrand"""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class CarBrand:
    # id: int
    name: str

    def to_dict(self) -> dict[str, Any]:
        """Преобразует объект в словарь."""
        return asdict(self)
