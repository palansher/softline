from dataclasses import dataclass,asdict
from typing import Any


@dataclass
class Brand:
    name: str # Наименование брэнда
    dop: int # Дата производства

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)