from dataclasses import dataclass,asdict
from typing import Any


@dataclass
class Person:
    id:int
    firstname:str
    lastname:str
    salary:int

    def to_dict(self)->dict[str, Any]:
        return asdict(self)

