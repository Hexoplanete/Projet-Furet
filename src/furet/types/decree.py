from dataclasses import dataclass
from typing import Self
from datetime import date

from furet.types import department
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
    department: department
    topic: DecreeTopic
    title: str
    publication_date: date
    state: DecreeState