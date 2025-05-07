from datetime import date

from . import department
from furet.types.base import dbclass

@dbclass
class DecreeTopic:
    id: int
    label: str
    

@dbclass
class DecreeState:
    id: int
    label: str


@dbclass
class Decree:
    id: int
    department: department.Department
    topic: DecreeTopic
    title: str
    publication_date: date
    state: DecreeState