from PySide6 import QtWidgets

from furet import repository
from furet.app.widgets.formWidget import FormWidget
from furet.app.widgets.optionalDateEdit import OptionalDateEdit
from furet.app.widgets.singleComboBox import SingleComboBox
from furet.models.decree import Decree


class DecreeEdit(FormWidget[Decree]):

    def __init__(self, decree: Decree, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)

        self._id = decree.id
        self._raa = decree.raa

        self._title = QtWidgets.QLineEdit(decree.title)
        self.addRow("Titre", self._title)
        self.installMissingBackground(self._title, "text", lambda v: len(v) == 0)

        self._number = QtWidgets.QLineEdit(decree.number)
        self.addRow("N° de l'arrêté", self._number)
        self.installMissingBackground(self._number, "text", lambda v: len(v) == 0)

        self._documentType = SingleComboBox([None, *repository.getDocumentTypes()], decree.docType, label=lambda v: "Non défini" if v is None else str(v))
        self.addRow("Type de document", self._documentType)
        self.installMissingBackground(self._documentType, "selectedItem", lambda v: v is None)

        self._signingDate = OptionalDateEdit(decree.signingDate)
        self.addRow("Date de signature", self._signingDate)
        self.installMissingBackground(self._signingDate, "qdate", lambda v: v is None)

        pagesWidget = QtWidgets.QWidget()
        pagesLayout = QtWidgets.QHBoxLayout(pagesWidget)
        pagesLayout.setContentsMargins(0, 0, 0, 0)
        self._startPage = QtWidgets.QSpinBox(minimum=1, maximum=9999, value=decree.startPage)
        pagesSep = QtWidgets.QLabel("à")
        self._endPage = QtWidgets.QSpinBox(minimum=1, maximum=9999, value=decree.endPage)
        pagesLayout.addWidget(self._startPage)
        pagesLayout.addWidget(pagesSep)
        pagesLayout.addWidget(self._endPage)
        pagesLayout.addStretch(1)
        self.addRow("Pages", pagesWidget)

    def value(self) -> Decree:
        return Decree(
            id=self._id,

            raa=self._raa,
            startPage=self._startPage.value(),
            endPage=self._endPage.value(),

            docType=self._documentType.selectedItem(),
            number=self._number.text(),
            title=self._title.text(),
            signingDate=self._signingDate.qdate()
        )