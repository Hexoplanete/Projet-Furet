from dataclasses import dataclass
from furet.repository.csvdb import TableObject
from datetime import date
from dateutil.relativedelta import relativedelta


@dataclass(eq=False)
class Department(TableObject):
    id: int
    number: str
    label: str

    def __str__(self):
        return f"{self.number} - {self.label}"

@dataclass(eq=False)
class RAA(TableObject):
    id: int
    fileHash: str
    decreeCount: int = 0
    number: str = ""
    department: Department | None = None
    publicationDate: date | None = None
    url: str = ""
    def __str__(self):
        return self.number

    def expireDate(self):
        return self.getExpireDate(self.publicationDate)

    @classmethod
    def getExpireDate(cls, date: date | None):
        return None if date is None else date + relativedelta(months=2)

    def missingValues(self):
        return (len(self.number) == 0) + (self.department is None) + (self.publicationDate is None) + (len(self.url) == 0)

    # TODO find out if its necessary
    # def fileSubPath(self) -> str | None:
        # if self.missingValues():
        #     return "00.csv"
        # return f"{self.department.number}.csv"  # type: ignore
