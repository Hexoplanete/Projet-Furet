from typing import Any, Generic, TypeVar, Callable
from dataclasses import dataclass, field
from PySide6 import QtWidgets
from PySide6 import QtCore, QtWidgets


T = TypeVar('T')
TV = TypeVar('TV')


@dataclass
class ObjectTableColumn(Generic[T, TV]):
    formatHeader: Callable[[], str] | str
    value: Callable[[T], TV]
    format: Callable[[TV], str] = field(default=lambda v: str(v))
    valueKey: Callable[[TV], Any] = field(default=lambda v: v)
    resizeMode: QtWidgets.QHeaderView.ResizeMode = QtWidgets.QHeaderView.ResizeMode.Stretch

    def headerData(self, role: QtCore.Qt.ItemDataRole) -> Any:
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.formatHeader if type(self.formatHeader) is str else self.formatHeader()  # type: ignore

    def data(self, item: T, /, role: QtCore.Qt.ItemDataRole) -> Any:
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.format(self.value(item))
    
    def sortKey(self, item: T):
        return self.valueKey(self.value(item))


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


class ObjectTableWidget(QtWidgets.QTableView, Generic[T]):
    def __init__(self, items: list[T], columns: list[ObjectTableColumn[T, Any]], /, parent: QtWidgets.QWidget | None = None, *,
                 sortingEnabled: bool = True,
                 editTrigger: QtWidgets.QTableView.EditTrigger = QtWidgets.QTableView.EditTrigger.NoEditTriggers,
                 selectionMode: QtWidgets.QTableView.SelectionMode = QtWidgets.QTableView.SelectionMode.SingleSelection,
                 selectionBehavior: QtWidgets.QTableView.SelectionBehavior = QtWidgets.QTableView.SelectionBehavior.SelectRows
                 ):
        super().__init__(parent, sortingEnabled=sortingEnabled)
        self.setModel(ObjectTableModel(items, columns))
        [self.horizontalHeader().setSectionResizeMode(i, c.resizeMode) for i, c in enumerate(columns)]
        self.setEditTriggers(editTrigger)
        self.setSelectionMode(selectionMode)
        self.setSelectionBehavior(selectionBehavior)

    def setItems(self, items: list[T]):
        self.model().setItems(items)
    
    def items(self) -> list[T]:
        return self.model().items()
    
    def setItemAt(self, index: int, item: T):
        self.model().setItemAt(index, item)

    def itemAt(self, index: int) -> T:
        return self.model().itemAt(index)

    def setColumns(self, columns: list[ObjectTableColumn]):
        self.model().setColumns(columns)
        [self.horizontalHeader().setSectionResizeMode(c.resizeMode) for c in columns]

    def columns(self) -> list[ObjectTableColumn]:
        return self.model().columns()

    def setModel(self, model: ObjectTableModel, /):  # type: ignore
        super().setModel(model)
        
    def model(self, /) -> ObjectTableModel:
        return super().model()  # type: ignore
    
