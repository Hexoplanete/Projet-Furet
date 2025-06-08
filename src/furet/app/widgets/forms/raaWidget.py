from PySide6 import QtCore, QtWidgets, QtGui

from furet import repository
from furet.app.widgets.formWidget import FormWidget
from furet.app.widgets.optionalDateEdit import OptionalDateEdit
from furet.app.widgets.singleComboBox import SingleComboBox
from furet.types.raa import RAA


class UrlEdit(QtWidgets.QWidget):

    urlChanged = QtCore.Signal(str)

    def __init__(self, link: str | None = None, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
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


class RaaWidget(FormWidget):

    def __init__(self, raa: RAA, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._raa = raa

        self._department = SingleComboBox([None, *repository.getDepartments()], raa.department, label=lambda v: "Non défini" if v is None else str(v))
        self.addRow("Département", self._department)
        self.installMissingBackground(self._department, "selectedItem", lambda v: v is None)

        self._publicationDate = OptionalDateEdit(raa.publicationDate)
        self.addRow("Date de publication", self._publicationDate)
        self.installMissingBackground(self._publicationDate, "qdate", lambda v: v is None)

        self._expireDate = OptionalDateEdit(raa.expireDate())
        self._expireDate.setReadOnly(True)
        self._publicationDate.dateChanged.connect(lambda v: self._expireDate.setQdate(RAA.getExpireDate(v)))
        self.addRow("Date d'expiration", self._expireDate)

        self._url = UrlEdit(raa.url)
        self.addRow("Lien", self._url)
        self.installMissingBackground(self._url, "url", lambda v: len(v) == 0)

        self._number = QtWidgets.QLineEdit(text=raa.number)
        self.addRow("Numéro RAA", self._number)
        self.installMissingBackground(self._number, "text", lambda v: len(v) == 0)

    # # TODO reset form fields
    # def setRaa(self, raa: RAA):
    #     self._raa = raa

    def raa(self) -> RAA:
        return RAA(
            id=self._raa.id,
            fileHash=self._raa.fileHash,
            decreeCount=self._raa.decreeCount,
            number=self._number.text(),
            department=self._department.currentData(),
            publicationDate=self._publicationDate.qdate(),
            url=self._url.url()
        )
