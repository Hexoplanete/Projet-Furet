from dataclasses import dataclass
from furet.repository.csvdb import TableObject
from furet.types.department import Department
from datetime import date


@dataclass(eq=False)
class RAA(TableObject):
    id: int
    department: Department
    number: str
    link: str
    publicationDate: date

    def __str__(self):
        return self.number

    def isIncomplete(self):
        return len(self.number) == 0 or self.department is None or len(self.link) == 0 or self.publicationDate is None
