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
    raa_number: str
    link: str
    start_page: int
    end_page: int
    
    doc_type: DocumentType
    number: str
    title: str
    publication_date: date
    signing_date: date
    
    # Specific for our use
    campaign: Campaign
    topic: DecreeTopic
    treated: bool
    comment: str = ""