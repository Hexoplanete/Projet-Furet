from dataclasses import dataclass
from datetime import date
import enum

class Topic(enum.Enum):
    Wolf = enum.auto()


class DecreeState(enum.Enum):
    Done = enum.auto()
    TBD = enum.auto()

@dataclass
class Decree:
    department: int
    topic: Topic
    name: str
    publication_date: date
    state: DecreeState