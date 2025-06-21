from PySide6 import QtWidgets, QtCore, QtGui
from typing import Callable, Iterable, TypeVar, Generic

T = TypeVar('T')

class MultiComboBox(QtWidgets.QComboBox, Generic[T]):

    selectedItemsChanged = QtCore.Signal(list)

    def __init__(self, items: Iterable[T], selectedItems: list[T], /, parent: QtWidgets.QWidget | None = None, *,
                 label: Callable[[T], str] = str,
                 placeholder:str = ""):
        super().__init__(parent)
        self._label = label
        self._placeholder = placeholder

        self._clearAction = QtGui.QAction(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_LineEditClearButton), "", parent=self)
        self._clearAction.triggered.connect(lambda: self.setSelectedItems([]))

        self.setEditable(True)
        self.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.NoInsert)
        if (lineEdit := self.lineEdit()) and (completer := self.completer()):
            lineEdit.installEventFilter(self)
            lineEdit.addAction(self._clearAction,QtWidgets.QLineEdit.ActionPosition.TrailingPosition)
            completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
            completer.setCompletionMode(QtWidgets.QCompleter.CompletionMode.PopupCompletion)
            completer.setCompletionRole(QtCore.Qt.ItemDataRole.DisplayRole)

        self.activated.connect(self._activated)

        [self.addItem(i) for i in items]
        self.setSelectedItems(selectedItems)

        self.updateText()

    def eventFilter(self, watched, event, /):
        if watched == self.lineEdit():
            if event.type() == QtCore.QEvent.Type.MouseButtonRelease or event.type() == QtCore.QEvent.Type.FocusIn:
                self.lineEdit().selectAll()  # type: ignore
        return super().eventFilter(watched, event)

    def addItem(self, item: T):  # type: ignore
        super().addItem(self._label(item), item)
        self._setupIndex(self.count()-1)

    def insertItem(self, index: int, item: T):  # type: ignore
        super().insertItem(index, self._label(item), item)
        self._setupIndex(index)

    def _setupIndex(self, index: int):
        entry = self.model().item(index)
        entry.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsSelectable)
        entry.setData(QtCore.Qt.CheckState.Unchecked, QtCore.Qt.ItemDataRole.CheckStateRole)

    def setItems(self, items: Iterable[T]):
        self.clear()
        [self.addItem(i) for i in items]

    def items(self) -> list[T]:
        return [self.itemData(i) for i in range(self.count())]

    def setItem(self, index: int, item: T):
        self.setItemText(index, self._label(item))
        self.setItemData(index, item)
        self.updateText()

    def item(self, index: int) -> T:
        return self.itemData(index)

    def setSelectedItem(self, item: T, checked: bool | None = None):
        index = self.findData(item)
        if index != -1:
            if checked is None:
                checked = not self.model().item(index, self.modelColumn()).checkState() == QtCore.Qt.CheckState.Checked
            self.model().item(index, self.modelColumn()).setCheckState(QtCore.Qt.CheckState.Checked if checked else QtCore.Qt.CheckState.Unchecked)
            self.updateText()

        self.selectedItemsChanged.emit(self.selectedItems())

    def setSelectedItems(self, items: list[T]):
        [self.setSelectedItem(i, i in items) for i in self.items()]
    
    def selectedItem(self, item: T) -> bool:
        index = self.findData(item)
        return self.model().item(index, self.modelColumn()).checkState() == QtCore.Qt.CheckState.Checked
    
    def selectedItems(self) -> list[T]:
        return [self.itemData(i) for i in range(self.count()) if self.model().item(i, self.modelColumn()).checkState() == QtCore.Qt.CheckState.Checked]

    def model(self) -> QtGui.QStandardItemModel:
        return super().model()  # type: ignore
    
    def _activated(self, index: int):
        self.setSelectedItem(self.item(index))
        self.showPopup()

    def updateText(self):
        selectedItems = self.selectedItems()
        if lineEdit:= self.lineEdit():
            lineEdit.clear()
            lineEdit.setPlaceholderText(self._placeholder if len(selectedItems) == 0 else ", ".join([self._label(i) for i in selectedItems]))
        self._clearAction.setVisible(len(selectedItems) > 0)