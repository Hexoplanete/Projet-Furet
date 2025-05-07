from dataclasses import dataclass
from typing import Self


def dbclass(cls=None, /, *, id: str = "id", key: str = "id"):
    
    def wrap(cls):
        def eq(self, other: Self):
            return getattr(self, id) == getattr(other, id)
        def ne(self, other: Self):
            return getattr(self, id) != getattr(other, id)
        def lt(self, other: Self):
            return getattr(self, key) < getattr(other, key)
        def le(self, other: Self):
            return getattr(self, key) <= getattr(other, key)
        def gt(self, other: Self):
            return getattr(self, key) > getattr(other, key)
        def ge(self, other: Self):
            return getattr(self, key) >= getattr(other, key)
        cls.__eq__ = eq
        cls.__ne__ = ne
        cls.__lt__ = lt
        cls.__le__ = le
        cls.__gt__ = gt
        cls.__ge__ = ge
        return dataclass(cls, eq=False)

    # See if we're being called as @dbclass or @dbclass().
    if cls is None:
        # We're called with parens.
        return wrap

    # We're called as @dbclass without parens.
    return wrap(cls)