from dataclasses import dataclass,asdict
from typing import Any

@dataclass
class CarMark:
    mark:str

@dataclass
class CarModel(CarMark):
    id:int
    model:str

    def to_dict(self)->dict[str, Any]:
        return asdict(self)
