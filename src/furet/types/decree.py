from datetime import date
from typing import Optional

from furet.types.base import dbclass
from furet.types.department import Department

@dbclass
class DocumentType:
    id: int
    label: str

    def __str__(self):
        return self.label

@dbclass
class DecreeTopic:
    id: int
    label: str
    #nb Occurences de chaque topic dans un arrêté :int ?

    def __str__(self):
        return self.label
    
    def toCsvLine(self):
        return [self.id, self.label]

@dbclass
class Campaign:
    id: int
    label: str
    topicList: list[DecreeTopic]

    def __str__(self):
        return self.label
    
    def toCsvLine(self):
        topList = "-".join(map(lambda t: str(t.id),self.topicList))
        return [self.id, self.label, topList]

@dbclass
class Decree:
    id: int

    # raa: RAA Obligatoire
    department: Department
    link: str
    startPage: int
    endPage: int
    publicationDate : date

    # Decree Obligatoire
    treated: bool
    #text_content : str

    # RAA facultatif
    raaNumber: str = "0"

    # Decree
    comment: str = "0"
    docType: Optional[DocumentType] = None
    number: Optional[str] = "0"
    title: Optional[str] = None
    signingDate: Optional[date] = None

    campaign: Optional[Campaign] = None
    topic: list[DecreeTopic] = None

    def toCsvLine(self):
        return [
            self.id, self.department.id, self.docType.id, self.number, self.title, self.signingDate.strftime("%d/%m/%Y"), 
            self.raaNumber, self.publicationDate.strftime("%d/%m/%Y"), self.link, self.startPage, self.endPage, 
            self.campaign.id, "-".join(map(lambda t: str(t.id), self.topic)), int(self.treated), self.comment
        ]