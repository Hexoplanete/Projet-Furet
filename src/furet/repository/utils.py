
from typing import Iterable


def splitIdList(value: str) -> Iterable[int]:
    if len(value) == 0:
        return []
    else:
        return map(int, value.split('-'))

def joinIdList(values: Iterable[int]) -> str:
    return '-'.join(map(str, values))