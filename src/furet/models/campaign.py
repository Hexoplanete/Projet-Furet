from dataclasses import dataclass

from furet.repository.csvdb import TableObject

@dataclass(eq=False)
class Topic(TableObject):
    id: int
    label: str

    def __str__(self):
        return self.label


@dataclass(eq=False)
class Campaign(TableObject):
    id: int
    label: str
    topics: list[Topic]

    def __str__(self):
        return self.label
