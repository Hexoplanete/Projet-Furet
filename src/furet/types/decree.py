from datetime import date

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

    # raa: RAA
    department: Department
    raaNumber: str
    link: str
    startPage: int
    endPage: int
    
    doc_type: DocumentType
    number: str
    title: str
    publicationDate: date
    signingDate: date
    
    # Specific for our use
    campaign: Campaign
    topic: DecreeTopic
    treated: bool
    comment: str = ""