from dataclasses import dataclass
from PySide6 import QtCore

from typing import Any, Callable, TypeVar, Generic

T = TypeVar('T')
TV = TypeVar('TV')

class AbstractTableColumn(Generic[T]):
    def headerData(self, role: QtCore.Qt.ItemDataRole) -> Any: ...
    def data(self, item: T, /, role: QtCore.Qt.ItemDataRole) -> Any: ...
    def compareKey(self, item: T) -> Any: ...
        
@dataclass
class FieldColumn(AbstractTableColumn, Generic[T, TV]):
    name: str
    formatHeader: Callable[[], str] | None = None
    format: Callable[[T], str] = lambda v: str(v)

    def headerData(self, role: QtCore.Qt.ItemDataRole) -> Any:
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.name if self.formatHeader is None else self.formatHeader()

    def data(self, item: TV, /, role: QtCore.Qt.ItemDataRole) -> Any:
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.format(getattr(item, self.name))


@dataclass
class ComputedColumn(AbstractTableColumn, Generic[T, TV]):
    value: Callable[[TV], T]
    formatHeader: Callable[[], str] | None
    format: Callable[[T], str] = lambda v: str(v)

    def headerData(self, role: QtCore.Qt.ItemDataRole) -> Any:
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.formatHeader

    def data(self, item: TV, /, role: QtCore.Qt.ItemDataRole) -> Any:
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.format(self.value(item))


class ObjectTableModel(Generic[T], QtCore.QAbstractTableModel):
    def __init__(self, data: list[T], fields: list[AbstractTableColumn]):
        super().__init__()
        self._data = data
        self._fields = fields
        
    def headerData(self, section, orientation, /, role = ...):
        if orientation == QtCore.Qt.Orientation.Horizontal and role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self._fields[section].headerData(role) # type: ignore

    def resetData(self, data: list[T]):
        self.beginResetModel()
        self._data = data
        self.endResetModel()
    
    def data(self, index, /, role=...) -> Any:
        return self._fields[index.column()].data(self._data[index.row()], role) # type: ignore

    def rowCount(self, /, parent=...):
        return len(self._data)

    def columnCount(self, /, parent=...):
        return len(self._fields)

    def setItemAt(self, index: int, item: T):
        self._data[index] = item
        self.dataChanged.emit(self.index(index, 0), self.index(index, self.columnCount()-1))

    def itemAt(self, index: int):
        return self._data[index]
    
    def sort(self, column, /, order = ...):
        self.beginResetModel()
        self._data.sort(key=lambda v: self._fields[column].data(v, QtCore.Qt.ItemDataRole.DisplayRole), reverse=order == QtCore.Qt.SortOrder.DescendingOrder)
        self.endResetModel()

class SingleRowEditableModel[T](QtCore.QAbstractTableModel):
    def __init__(self, data: list[T], columnName):
        super().__init__()
        self.topics = data
        self._columnName = columnName

    def rowCount(self, /, parent=...):
        return len(self.topics)

    def columnCount(self, /, parent=...):
        return 1

    def data(self, index, /, role=...):
        if not index.isValid():
            return None

        topic = self.topics[index.row()]
        if role in (QtCore.Qt.ItemDataRole.DisplayRole, QtCore.Qt.ItemDataRole.EditRole):
            return topic.label

        return None

    def setData(self, index, value, /, role=...):
        if not index.isValid():
            return False

        if role == QtCore.Qt.ItemDataRole.EditRole:
            self.topics[index.row()].label = value
            self.dataChanged.emit(index, index, [QtCore.Qt.ItemDataRole.DisplayRole, QtCore.Qt.ItemDataRole.EditRole])
            return True

        return False

    def flags(self, index):
        return QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEditable

    def headerData(self, section, orientation, /, role=...):
        if role == QtCore.Qt.ItemDataRole.DisplayRole and orientation == QtCore.Qt.Orientation.Horizontal:
            return self._columnName
        return super().headerData(section, orientation, role)
    