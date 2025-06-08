from dataclasses import dataclass, field
from datetime import date
import os

from furet.repository.csvdb import TableObject
from furet.types.raa import RAA
from furet.types.campaign import Campaign, Topic


@dataclass(eq=False)
class DocumentType(TableObject):
    id: int
    label: str

    def __str__(self):
        return self.label


@dataclass
class AspasInfo:
    treated: bool
    campaigns: list[Campaign]
    topics: list[Topic]
    comment: str


@dataclass(eq=False)
class Decree(TableObject):
    id: int

    raa: RAA
    startPage: int
    endPage: int
    
    docType: DocumentType | None = None
    number: str = ""
    title: str = ""
    signingDate: date | None = None

    treated: bool = False
    campaigns: list[Campaign] = field(default_factory=list)
    topics: list[Topic] = field(default_factory=list)
    comment: str = ""

    def setAspasInfo(self, info: AspasInfo):
        self.treated = info.treated
        self.campaigns = info.campaigns
        self.topics = info.topics
        self.comment = info.comment

    def aspasInfo(self) -> AspasInfo:
        return AspasInfo(
            treated = self.treated,
            campaigns = self.campaigns,
            topics = self.topics,
            comment = self.comment,
        )

    def missingValues(self, includeRaa: bool = True):
        return (includeRaa and self.raa.missingValues()) + (self.docType is None) + (len(self.number) == 0) + (len(self.title) == 0) + (self.signingDate is None)

    # TODO find out if its necessary and make it work if raa data changes
    # def fileSubPath(self) -> str | None:
    #     if self.missingValues():
    #         return "00.csv"
    #     return os.path.join(self.raa.department.number, f"{self.raa.department.number}_{self.raa.publicationDate.strftime("%Y-%m")}_RAA.csv")  # type: ignore
