from dataclasses import dataclass
from furet.types.dbclass import dbclass
from furet.types.department import Department
from datetime import date

@dataclass(eq=False)
@dbclass(sort="number")
class RAA:
    department: Department
    number: str
    link: str
    publicationDate: date

    def __str__(self):
        return self.number
