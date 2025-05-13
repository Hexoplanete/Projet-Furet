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

    department: Department

    #arrete
    docType: DocumentType
    number: str
    title: str
    signingDate: date 

    # raa: RAA
    raaNumber: str
    publicationDate: date
    link: str
    startPage: int
    endPage: int
    
    docType: DocumentType
    number: str
    title: str
    publicationDate: date
    signingDate: date
    
    # Specific for our use
    campaign: Campaign
    topic: list[DecreeTopic] # TODO rename to topics
    treated: bool
    comment: str = ""

    def toCsvLine(self):
        return [
            self.id, self.department.id, self.docType.id, self.number, self.title, self.signingDate.strftime("%d/%m/%Y"), 
            self.raaNumber, self.publicationDate.strftime("%d/%m/%Y"), self.link, self.startPage, self.endPage, 
            self.campaign.id, "-".join(map(lambda t: str(t.id),self.topic)), int(self.treated), self.comment
        ]