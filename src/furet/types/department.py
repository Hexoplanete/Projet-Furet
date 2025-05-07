
from furet.types.base import dbclass


@dbclass
class Department:
    id: int
    number: str
    label: str