from dataclasses import dataclass
from PySide6 import QtCore

from typing import Callable, TypeVar, Generic

T = TypeVar('T')

@dataclass
class TableColumn(Generic[T]):
    name: str
    formatHeader: Callable[[], str] | None = None
    format: Callable[[T], str] = lambda v: str(v)

class ObjectTableModel(Generic[T], QtCore.QAbstractTableModel):
    def __init__(self, data: list[T], fields: list[TableColumn]):
        super().__init__()
        self._data = data
        self._fields = fields
        
    def headerData(self, section, orientation, /, role = ...):
        if orientation == QtCore.Qt.Orientation.Horizontal and role == QtCore.Qt.ItemDataRole.DisplayRole:
            field = self._fields[section]
            return field.name if field.formatHeader is None else self._fields[section].formatHeader()

    def data(self, index, /, role=...):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            field = self._fields[index.column()]
            return field.format(getattr(self._data[index.row()], field.name))

    def rowCount(self, /, parent=...):
        return len(self._data)

    def columnCount(self, /, parent=...):
        return len(self._fields)

    def itemAt(self, index: int):
        return self._data[index]

    def sort(self, column, /, order = ...):
        self.beginResetModel()
        print(self._data[0], self._data[0])
        self._data.sort(key=lambda d: getattr(d, self._fields[column].name), reverse=order == QtCore.Qt.SortOrder.DescendingOrder)
        self.endResetModel()


class ObjectFilterProxy(Generic[T], QtCore.QSortFilterProxyModel):

    def __init__(self, filterer: Callable[[int, QtCore.QModelIndex | QtCore.QPersistentModelIndex], bool], parent=None):
        super().__init__(parent)
        self._filterer = filterer

    def setSourceModel(self, model: ObjectTableModel[T]):
        super().setSourceModel(model)

    def sourceModel(self) -> ObjectTableModel[T]:
        return super().sourceModel()

    def filterAcceptsRow(self, source_row, source_parent, /):
        return self._filterer(self.sourceModel().itemAt(source_row))
