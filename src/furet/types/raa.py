from furet.types.base import dbclass
from furet.types.department import Department


@dbclass(sort="number")
class RAA:
    id: int
    department: Department
    number: str
    link: str

    def __str__(self):
        return self.number
