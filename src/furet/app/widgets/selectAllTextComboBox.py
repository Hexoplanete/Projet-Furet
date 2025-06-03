from PySide6 import QtWidgets, QtCore


class SelectAllTextComboBox(QtWidgets.QComboBox):
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.setEditable(True)
        self.lineEdit().installEventFilter(self)  # type: ignore

    def eventFilter(self, watched, event, /):
        if watched == self.lineEdit():
            if event.type() == QtCore.QEvent.Type.MouseButtonRelease or event.type() == QtCore.QEvent.Type.FocusIn:
                self.lineEdit().selectAll()  # type: ignore
        return super().eventFilter(watched, event)
