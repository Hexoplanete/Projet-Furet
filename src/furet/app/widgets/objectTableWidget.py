from typing import Any, Generic, TypeVar
from PySide6 import QtWidgets

from furet.app.widgets.objectTableModel import ObjectTableColumn, ObjectTableModel

T = TypeVar("T")

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
        return super().model() #type: ignore
    
