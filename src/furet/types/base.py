from dataclasses import dataclass
from functools import total_ordering

@total_ordering
@dataclass(eq=False)
class BaseData:
    id: int

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.id < other.id
