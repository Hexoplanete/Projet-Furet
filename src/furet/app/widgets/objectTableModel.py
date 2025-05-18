from dataclasses import dataclass
from PySide6 import QtCore, QtGui

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
            return field.name if field.formatHeader is None else field.formatHeader()
        
        # if orientation == QtCore.Qt.Orientation.Vertical and role == QtCore.Qt.ItemDataRole.DisplayRole:
        #     return self.rowCount() - section

    def resetData(self, data: list[T]):
        self.beginResetModel()
        self._data = data
        self.endResetModel()
    
    def data(self, index, /, role=...):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            field = self._fields[index.column()]
            return field.format(getattr(self._data[index.row()], field.name))
        elif role == QtCore.Qt.ItemDataRole.ForegroundRole:
            if index.column() == 6:
                field = self._fields[index.column()]
                return QtGui.QColor("green") if getattr(self._data[index.row()], field.name) else QtGui.QColor("red")
            if index.column() == 7:
                field = self._fields[index.column()]
                return QtGui.QColor("green") if not getattr(self._data[index.row()], field.name) else QtGui.QColor("red")

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
    