from PySide6 import QtWidgets

from furet import repository
from furet.app.widgets.formWidget import FormWidget
from furet.app.widgets.optionalDateEdit import OptionalDateEdit
from furet.app.widgets.singleComboBox import SingleComboBox
from furet.app.widgets.urlEdit import UrlEdit
from furet.models.raa import RAA


class RaaEdit(FormWidget[RAA]):

    def __init__(self, raa: RAA, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._id = raa.id
        self._fileHash = raa.fileHash
        self._decreeCount = raa.decreeCount

        self._department = SingleComboBox([None, *repository.getDepartments()], raa.department, label=lambda v: "Non défini" if v is None else str(v))
        self.addRow("Département", self._department)
        self.installMissingBackground(self._department, "selectedItem", lambda v: v is None)

        self._publicationDate = OptionalDateEdit(raa.publicationDate)
        self.addRow("Date de publication", self._publicationDate)
        self.installMissingBackground(self._publicationDate, "qdate", lambda v: v is None)

        self._expireDate = OptionalDateEdit(raa.expireDate())
        self._expireDate.setReadOnly(True)
        self._publicationDate.qdateChanged.connect(lambda v: self._expireDate.setQdate(RAA.getExpireDate(v)))
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

    def value(self) -> RAA:
        return RAA(
            id=self._id,
            fileHash=self._fileHash,
            decreeCount=self._decreeCount,
            number=self._number.text(),
            department=self._department.selectedItem(),
            publicationDate=self._publicationDate.qdate(),
            url=self._url.url()
        )
