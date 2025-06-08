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
        self.lineEdit().installEventFilter(self)  # type: ignore

        self._resetCompleter()

        self.currentIndexChanged.connect(lambda i: self.selectedItemChanged.emit(self.item(i)))

    def eventFilter(self, watched, event, /):
        if watched == self.lineEdit():
            if event.type() == QtCore.QEvent.Type.MouseButtonRelease or event.type() == QtCore.QEvent.Type.FocusIn:
                self.lineEdit().selectAll()  # type: ignore
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

    def _resetCompleter(self):
        completer = QtWidgets.QCompleter([self._label(i) for i in self.items()], self)
        completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        completer.setCompletionMode(QtWidgets.QCompleter.CompletionMode.UnfilteredPopupCompletion)
        self.setCompleter(completer)
