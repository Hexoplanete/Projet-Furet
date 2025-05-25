from dataclasses import dataclass
from furet.types.department import Department
from datetime import date

@dataclass(eq=False)
class ProcessingRAA:
    department: Department
    number: str
    link: str
    publicationDate: date

    def __str__(self):
        return self.number
