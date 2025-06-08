from PySide6 import QtWidgets, QtCore

from typing import Callable, Iterable, TypeVar, Generic

T = TypeVar('T')


class SingleComboBox(QtWidgets.QComboBox, Generic[T]):

    selectedItemChanged = QtCore.Signal(object)

    def __init__(self, items: Iterable[T], selectedItem: T, /, parent: QtWidgets.QWidget | None = None, *,
                 label: Callable[[T], str] = str):
        super().__init__(parent)
        self._label = label

        [self.addItem(i) for i in items]
        self.setSelectedItem(selectedItem)

        self.setEditable(True)
        if (lineEdit := self.lineEdit()) and (completer := self.completer()):
            lineEdit.installEventFilter(self)
            completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
            completer.setCompletionMode(QtWidgets.QCompleter.CompletionMode.UnfilteredPopupCompletion)

        self.currentIndexChanged.connect(lambda i: self.selectedItemChanged.emit(self.item(i)))

    def eventFilter(self, watched, event, /):
        if (lineEdit:= self.lineEdit()) and  watched == lineEdit:
            if event.type() == QtCore.QEvent.Type.MouseButtonRelease or event.type() == QtCore.QEvent.Type.FocusIn:
                lineEdit.selectAll()
        return super().eventFilter(watched, event)

    def addItem(self, item: T):  # type: ignore
        super().addItem(self._label(item), item)

    def insertItem(self, index: int, item: T):  # type: ignore
        super().insertItem(index, self._label(item), item)

    def setItems(self, items: Iterable[T]):
        self.clear()
        [self.addItem(i) for i in items]

    def items(self) -> list[T]:
        return [self.itemData(i) for i in range(self.count())]

    def setItem(self, index: int, item: T):
        self.setItemText(index, self._label(item))
        self.setItemData(index, item)

    def item(self, index: int) -> T:
        return self.itemData(index)

    def setSelectedItem(self, item: T):
        index = self.findData(item)
        if index != -1:
            self.setCurrentIndex(index)

    def selectedItem(self) -> T:
        return self.currentData()
