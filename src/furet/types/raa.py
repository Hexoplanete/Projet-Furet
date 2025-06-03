from dataclasses import dataclass
from furet.repository.csvdb import TableObject
from furet.types.department import Department
from datetime import date


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

    def isIncomplete(self):
        return len(self.number) == 0 or self.department is None or self.publicationDate is None or len(self.url) == 0

    def fileSubPath(self) -> str | None:
        if self.isIncomplete():
            return "00.csv"
        return f"{self.department.number}.csv"  # type: ignore
