from dataclasses import dataclass
from datetime import date

from furet.types import Department
from furet.types.base import BaseData

class DecreeTopic(BaseData):
    label: str
    
class DecreeState(BaseData):
    label: str

@dataclass
class Decree(BaseData):
    department: Department
    topic: DecreeTopic
    title: str
    publication_date: date
    state: DecreeState