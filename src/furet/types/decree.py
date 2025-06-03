from dataclasses import dataclass, field
from datetime import date
import os

from furet.repository.csvdb import TableObject
from furet.types.department import Department
from furet.types.raa import RAA


@dataclass(eq=False)
class DocumentType(TableObject):
    id: int
    label: str

    def __str__(self):
        return self.label


@dataclass(eq=False)
class Topic(TableObject):
    id: int
    label: str

    def __str__(self):
        return self.label


@dataclass(eq=False)
class Campaign(TableObject):
    id: int
    label: str
    topics: list[Topic]

    def __str__(self):
        return self.label


@dataclass(eq=False)
class Decree(TableObject):
    id: int

    # raa: RAA
    startPage: int
    endPage: int
    
    raaNumber: str = ""
    department: Department | None = None
    link: str = ""
    publicationDate: date | None = None

    docType: DocumentType | None = None
    number: str = ""
    title: str = ""
    signingDate: date | None = None

    treated: bool = False
    campaigns: list[Campaign] = field(default_factory=list)
    topics: list[Topic] = field(default_factory=list)
    comment: str = ""

    def isIncomplete(self):
        return len(self.title) == 0 or len(self.number) == 0 or len(self.raaNumber) == 0 or self.department is None or len(self.link) == 0 or self.publicationDate is None or self.signingDate is None or self.docType is None
        # return self.raa.isIncomplete() or self.docType is None or len(self.number) == 0 or len(self.title) == 0 or self.signingDate is None

    def fileSubPath(self) -> str | None:
        if self.department is None or self.publicationDate is None:
            return "00.csv"
        return os.path.join(self.department.number, f"{self.department.number}_{self.publicationDate.strftime("%Y-%m")}_RAA.csv")
