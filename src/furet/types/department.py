
from dataclasses import dataclass

from furet.repository.csvdb import TableObject


@dataclass(eq=False)
class Department(TableObject):
    id: int
    number: str
    label: str

    def __str__(self):
        return f"{self.number} - {self.label}"