from PySide6 import QtWidgets, QtCore, QtGui

NONE_DATE = QtCore.QDate(1900, 1, 1)

class OptionalDateEdit(QtWidgets.QDateEdit):

    def __init__(self, date: QtCore.QDate | None, /, parent: QtWidgets.QWidget | None = None, readOnly: bool | None = None):
        super().__init__(NONE_DATE if date is None else date, parent=parent)
        self.setMinimumDate(NONE_DATE)
        self.setSpecialValueText("Non définie")

        self._clearAction = QtGui.QAction(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_LineEditClearButton), "", parent=self)
        self._clearAction.triggered.connect(lambda: self.setDate(NONE_DATE))
        
        if not readOnly:
            self.lineEdit().addAction(self._clearAction, QtWidgets.QLineEdit.ActionPosition.TrailingPosition)
            self.uptadeClearAction(super().date())
        
        self.dateChanged.connect(self.uptadeClearAction)

    def uptadeClearAction(self, date: QtCore.QDate):
        self._clearAction.setVisible(date != NONE_DATE)

    def setDate(self, date: QtCore.QDate | None, /) -> None:
        QtWidgets.QDateTimeEdit.setDate(self, NONE_DATE if date is None else date)
    
    def date(self): # type: ignore
        d = QtWidgets.QDateTimeEdit.date(self)
        return None if d == NONE_DATE else d

    def setReadOnly(self, r: bool, /) -> None:
        QtWidgets.QDateEdit.setReadOnly(self, r)
        if r: self.lineEdit().removeAction(self._clearAction)
        else: self.lineEdit().addAction(self._clearAction)