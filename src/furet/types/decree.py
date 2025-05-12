from datetime import date
from typing import Optional
from typing import Dict

from furet.types.base import dbclass
from furet.types.department import Department
from furet.types.raa import RAA

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

@dbclass
class Campaign:
    id: int
    label: str

    def __str__(self):
        return self.label

@dbclass
class Decree:
    id: int

    # raa: RAA Obligatoire
    department: Department
    link: str
    startPage: int
    endPage: int

    # Decree Obligatoire
    treated: bool

    # RAA facultatif
    raaNumber: str

    # Decree
    comment: str = ""
    doc_type: Optional[DocumentType] = None
    number: Optional[str] = None
    title: Optional[str] = None
    signingDate: Optional[date] = None

    campaign: Optional[Campaign] = None
    topic: Optional[dict[str, int]] = None

    def toCsvLine(self):
        return [
            self.id, self.department.id, self.docType.id, self.number, self.title, self.signingDate.strftime("%d/%m/%Y"), 
            self.raaNumber, self.publicationDate.strftime("%d/%m/%Y"), self.link, self.startPage, self.endPage, 
            self.campaign.id, "-".join(map(lambda t: str(t.id),self.topic)), int(self.treated), self.comment
        ]