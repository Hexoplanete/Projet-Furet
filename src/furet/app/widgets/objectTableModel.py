from PySide6 import QtCore

from typing import TypeVar

T = TypeVar('T')
TV = TypeVar('TV')


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
