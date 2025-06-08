from datetime import date
from PySide6 import QtWidgets, QtCore, QtGui

NONE_DATE = QtCore.QDate(1900, 1, 1)


class OptionalDateEdit(QtWidgets.QDateEdit):

    qdateChanged = QtCore.Signal(date)

    def __init__(self, date: date | None, /, parent: QtWidgets.QWidget | None = None, *,
                 readOnly: bool | None = None, popup: bool = True, format: str = "dd MMMM yyyy"):
        super().__init__(NONE_DATE if date is None else date, parent=parent)  # type: ignore
        self.setCalendarPopup(popup)
        self.setDisplayFormat(format)
        self.setMinimumDate(NONE_DATE)
        self.setSpecialValueText("Non définie")

        self._clearAction = QtGui.QAction(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_LineEditClearButton), "", parent=self)
        self._clearAction.triggered.connect(lambda: self.setQdate(None))

        if not readOnly:
            self.lineEdit().addAction(self._clearAction,QtWidgets.QLineEdit.ActionPosition.TrailingPosition)
            self.updateClearAction(self.qdate())

        self.dateChanged.connect(lambda d: self.qdateChanged.emit(None if d == NONE_DATE else d.toPython()))
        self.qdateChanged.connect(self.updateClearAction)

    def updateClearAction(self, date: date | None):
        self._clearAction.setVisible(date is not None)

    def setQdate(self, date: date | None, /) -> None:
        super().setDate(NONE_DATE if date is None else date)  # type: ignore

    def qdate(self, /) -> date | None:
        date = super().date()
        return None if date == NONE_DATE else date.toPython()  # type: ignore

    def setReadOnly(self, r: bool, /) -> None:
        super().setReadOnly(r)
        if r:
            self.lineEdit().removeAction(self._clearAction)
        else:
            self.lineEdit().addAction(self._clearAction)
