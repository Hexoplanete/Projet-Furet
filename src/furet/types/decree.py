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
    
    def toCsvLine(self):
        return [self.id, self.label]

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
    startPage: int
    endPage: int
    

    # Decree Obligatoire
    treated: bool
    #text_content : str

    # RAA facultatif
    raaNumber: str = "0"

    # Decree
    department:Optional[Department] = None
    link: Optional[str] = None
    publicationDate: Optional[date] = None 
    comment: str = "0"
    docType: Optional[DocumentType] = None
    number: Optional[str] = "0"
    title: Optional[str] = None
    signingDate: Optional[date] = None

    campaigns: list[Campaign] = None
    topics: list[DecreeTopic] = None
    
    missingData: bool = True

    def toCsvLine(self):
        return [
            self.id, self.department.id, self.docType.id, self.number, self.title, self.signingDate.strftime("%d/%m/%Y"), 
            self.raaNumber, self.publicationDate.strftime("%d/%m/%Y"), self.link, self.startPage, self.endPage, 
            "-".join(map(lambda t: str(t.id), self.campaigns)), "-".join(map(lambda t: str(t.id), self.topics)), int(self.treated), self.comment,
            self.missingData
        ]