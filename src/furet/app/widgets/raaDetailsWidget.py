from typing import Any, Callable
from PySide6 import QtCore, QtWidgets, QtGui

from furet import repository
from furet.app.utils import addFormRow, addFormSection, buildComboBox, buildDatePicker
from furet.app.widgets.optionalDateEdit import NONE_DATE
from furet.types.raa import RAA

class UrlEdit(QtWidgets.QWidget):

    urlChanged = QtCore.Signal(str)

    def __init__(self, link: str | None = None, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setContentsMargins(0,0,0,0)
        self._layout.setSpacing(0)
        self._urlEdit = QtWidgets.QLineEdit(link if link is not None else "")
        self._urlEdit.textChanged.connect(self.urlChanged.emit)
        self._layout.addWidget(self._urlEdit, stretch=1)
        self._openButton = QtWidgets.QPushButton()
        self._openButton.setIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowRight))
        self._openButton.clicked.connect(self.openUrl)
        self._layout.addWidget(self._openButton)

    def openUrl(self):
        QtGui.QDesktopServices.openUrl(self._urlEdit.text())

    def setUrl(self, url: str):
        self._urlEdit.setText(url)

    def url(self) -> str:
        return self._urlEdit.text()

class RaaDetailsWidget(QtWidgets.QWidget):
    
    def __init__(self, raa: RAA, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.setStyleSheet('*[missingValue="true"] { background-color: rgba(255, 0, 0, 0.2) }')

        self._raa = raa
        self._layout = QtWidgets.QFormLayout(self)
        self._layout.setContentsMargins(0,0,0,0)

        self._department = buildComboBox(repository.getDepartments(), raa.department, ("Non défini", None))
        addFormRow(self._layout, "Département", self._department)
        self.installMissingBackground(self._department, "currentIndex", lambda v: v == 0)

        self._publicationDate = buildDatePicker(raa.publicationDate)
        addFormRow(self._layout, "Date de publication", self._publicationDate)
        self.installMissingBackground(self._publicationDate, "date", lambda v: v is None or v == NONE_DATE)
        
        self._url = UrlEdit(raa.url)
        addFormRow(self._layout, "Lien", self._url)
        self.installMissingBackground(self._url, "url", lambda v: len(v) == 0)

        self._number = QtWidgets.QLineEdit(text=raa.number)
        addFormRow(self._layout, "Numéro RAA", self._number)
        self.installMissingBackground(self._number, "text", lambda v: len(v) == 0)

    # # TODO reset form fields
    # def setRaa(self, raa: RAA):
    #     self._raa = raa

    def raa(self) -> RAA:
        publicationDate = self._publicationDate.date()
        return RAA(
            id=self._raa.id,
            fileHash=self._raa.fileHash,
            decreeCount=self._raa.decreeCount,
            number=self._number.text(),
            department=self._department.currentData(),
            publicationDate=None if publicationDate is None else publicationDate.toPython(),  # type: ignore
            url=self._url.url()
        )

    def installMissingBackground(self, widget: QtWidgets.QWidget, fieldName: str, isMissing: Callable[[Any], bool]):
        signal: QtCore.SignalInstance = getattr(widget, f"{fieldName}Changed")

        def updateProp(value: Any):
            widget.setProperty("missingValue", isMissing(value))
            self.style().unpolish(widget)
            self.style().polish(widget)
        signal.connect(updateProp)
        field = getattr(widget, fieldName)
        updateProp(field())
