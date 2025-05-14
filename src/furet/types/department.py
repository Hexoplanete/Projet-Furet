
from furet.types.base import dbclass


@dbclass(sort="number")
class Department:
    id: int
    number: str
    label: str

    def __str__(self):
        return f"{self.number} - {self.label}"
    
    def toCsvLine(self):
        return [self.id, self.number, self.label]
