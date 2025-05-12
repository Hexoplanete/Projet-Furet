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

# @dbclass
# class DecreeTopic:
#     id: int
#     label: str

#     def __str__(self):
#         return self.label

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
    raaNumber: Optional[str] = None
    link: str
    startPage: int
    endPage: int

    doc_type: Optional[DocumentType] = None
    number: Optional[str] = None
    title: Optional[str] = None
    signingDate: Optional[date] = None

    # Specific for our use
    campaign: Optional[Campaign] = None
    topic: Optional[dict[str, int]] = None
    treated: bool
    comment: str = ""