from furet.types.base import dbclass
from furet.types.department import Department
from datetime import date

@dbclass(sort="number")
class RAA:
    department: Department
    number: str
    link: str
    publicationDate: date

    def __str__(self):
        return self.number
