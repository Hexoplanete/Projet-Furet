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
        
        # if orientation == QtCore.Qt.Orientation.Vertical and role == QtCore.Qt.ItemDataRole.DisplayRole:
        #     return self.rowCount() - section

    def data(self, index, /, role=...):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            field = self._fields[index.column()]
            return field.format(getattr(self._data[index.row()], field.name))

    def rowCount(self, /, parent=...):
        return len(self._data)

    def columnCount(self, /, parent=...):
        return len(self._fields)

    def setItemAt(self, index: int, item: T):
        self._data[index] = item
        self.dataChanged.emit(self.index(index, 0), self.index(index, self.columnCount()-1))

    def itemAt(self, index: int):
        return self._data[index]

    def lessThan(self, indexLeft: QtCore.QModelIndex | QtCore.QPersistentModelIndex, indexRight: QtCore.QModelIndex | QtCore.QPersistentModelIndex, /):
        fieldLeft = self._fields[indexLeft.column()]
        fieldRight = self._fields[indexRight.column()]
        return getattr(self._data[indexLeft.row()], fieldLeft.name) < getattr(self._data[indexRight.row()], fieldRight.name)

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
    
    def lessThan(self, source_left, source_right, /):
        return self.sourceModel().lessThan(source_left, source_right)
