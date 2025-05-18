
from dataclasses import dataclass
from furet.types.dbclass import dbclass


@dbclass(sort="number")
@dataclass(eq=False)
class Department:
    id: int
    number: str
    label: str

    def __str__(self):
        return f"{self.number} - {self.label}"