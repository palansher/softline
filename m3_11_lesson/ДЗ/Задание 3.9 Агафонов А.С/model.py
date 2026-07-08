from dataclasses import dataclass,asdict
from typing import Any

from brand import Brand


@dataclass
class Model:
    brand: Brand
    model: str
    price: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
