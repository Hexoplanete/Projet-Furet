from dataclasses import dataclass, field
from datetime import date

from furet.types.dbclass import dbclass
from furet.types.department import Department


@dbclass
@dataclass(eq=False)
class DocumentType:
    id: int
    label: str

    def __str__(self):
        return self.label


@dbclass
@dataclass(eq=False)
class DecreeTopic:
    id: int
    label: str

    def __str__(self):
        return self.label


@dbclass
@dataclass(eq=False)
class Campaign:
    id: int
    label: str
    topicList: list[DecreeTopic]

    def __str__(self):
        return self.label


@dbclass
@dataclass(eq=False)
class Decree:
    id: int

    # raa: RAA Obligatoire
    startPage: int
    endPage: int

    # Decree Obligatoire
    treated: bool
    # text_content : str

    # RAA facultatif
    raaNumber: str = ""

    # Decree
    department: Department | None = None
    link: str = ""
    publicationDate: date | None = None
    comment: str = ""
    docType: DocumentType | None = None
    number: str = ""
    title: str = ""
    signingDate: date | None = None

    campaigns: list[Campaign] = field(default_factory=list)
    topics: list[DecreeTopic] = field(default_factory=list)

    def isIncomplete(self):
        return len(self.title) == 0 or len(self.number) == 0 or len(self.raaNumber) == 0 or self.department is None or len(self.link) == 0 or self.publicationDate is None or self.signingDate is None or self.docType is None
