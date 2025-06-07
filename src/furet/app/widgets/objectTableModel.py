from dataclasses import dataclass
from PySide6 import QtCore, QtWidgets

from typing import Any, Callable, TypeVar, Generic

T = TypeVar('T')
TV = TypeVar('TV')

@dataclass
class ObjectTableColumn(Generic[T, TV]):
    formatHeader: Callable[[], str] | str
    value: Callable[[T], TV]
    format: Callable[[TV], str] = lambda v: str(v)
    _sortKey: Callable[[TV], Any] = lambda v: v

    def headerData(self, role: QtCore.Qt.ItemDataRole) -> Any:
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.formatHeader if type(self.formatHeader) is str else self.formatHeader()  # type: ignore

    def data(self, item: T, /, role: QtCore.Qt.ItemDataRole) -> Any:
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.format(self.value(item))
    
    def sortKey(self, item: T):
        return self._sortKey(self.value(item))


class ObjectTableModel(Generic[T], QtCore.QAbstractTableModel):
    def __init__(self, items: list[T], columns: list[ObjectTableColumn]):
        super().__init__()
        self._items = items
        self._columns = columns

    def setItems(self, data: list[T]):
        self.beginResetModel()
        self._items = data
        self.endResetModel()
    
    def items(self) -> list[T]:
        return self._items

    def setItemAt(self, index: int, item: T):
        self._items[index] = item
        self.dataChanged.emit(self.index(index, 0), self.index(index, self.columnCount()-1))

    def itemAt(self, index: int) -> T:
        return self._items[index]

    def setColumns(self, columns: list[ObjectTableColumn]):
        self.beginResetModel()
        self._columns = columns
        self.endResetModel()
        
    def columns(self) -> list[ObjectTableColumn]:
        return self._columns
    
    def headerData(self, section, orientation, /, role=...):
        if orientation == QtCore.Qt.Orientation.Horizontal and role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self._columns[section].headerData(role)  # type: ignore
    
    def data(self, index, /, role=...) -> Any:
        return self._columns[index.column()].data(self._items[index.row()], role)  # type: ignore

    def rowCount(self, /, parent=...):
        return len(self._items)

    def columnCount(self, /, parent=...):
        return len(self._columns)

    def sort(self, column, /, order=...):
        self.beginResetModel()
        self._items.sort(key=lambda v: self._columns[column].sortKey(v), reverse=order == QtCore.Qt.SortOrder.DescendingOrder)
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
