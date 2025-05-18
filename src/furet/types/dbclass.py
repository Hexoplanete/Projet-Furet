def dbclass(cls=None, /, *, id: str = "id", sort: str = "id"):
    
    def wrap(cls):
        def eq(self, other):
            return getattr(self, id) == getattr(other, id)
        def ne(self, other):
            return getattr(self, id) != getattr(other, id)
        def lt(self, other):
            return getattr(self, sort) < getattr(other, sort)
        def le(self, other):
            return getattr(self, sort) <= getattr(other, sort)
        def gt(self, other):
            return getattr(self, sort) > getattr(other, sort)
        def ge(self, other):
            return getattr(self, sort) >= getattr(other, sort)
        cls.__eq__ = eq
        cls.__ne__ = ne
        cls.__lt__ = lt
        cls.__le__ = le
        cls.__gt__ = gt
        cls.__ge__ = ge

        return cls

    # See if we're being called as @dbclass or @dbclass().
    if cls is None:
        # We're called with parens.
        return wrap

    # We're called as @dbclass without parens.
    return wrap(cls)