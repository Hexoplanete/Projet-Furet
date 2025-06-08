from PySide6 import QtWidgets

from furet import repository
from furet.app.utils import buildComboBox, buildDatePicker
from furet.app.widgets.formWidget import FormWidget
from furet.app.widgets.optionalDateEdit import NONE_DATE
from furet.types.decree import Decree


class DecreeWidget(FormWidget):

    def __init__(self, decree: Decree, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)

        self._decree = decree

        self._title = QtWidgets.QLineEdit(decree.title)
        self.addRow("Titre", self._title)
        self.installMissingBackground(self._title, "text", lambda v: len(v) == 0)

        self._number = QtWidgets.QLineEdit(decree.number)
        self.addRow("N° de l'arrêté", self._number)
        self.installMissingBackground(self._number, "text", lambda v: len(v) == 0)

        self._documentType = buildComboBox(repository.getDocumentTypes(), decree.docType, ("Non défini", None))
        self.addRow("Type de document", self._documentType)
        self.installMissingBackground(self._documentType, "currentIndex", lambda v: v == 0)

        self._signingDate = buildDatePicker(decree.signingDate)
        self.addRow("Date de signature", self._signingDate)
        self.installMissingBackground(self._signingDate, "date", lambda v: v is None or v == NONE_DATE)

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

    # # TODO reset form fields
    # def setDecree(self, decree: DECREE):
    #     self._decree = decree

    def decree(self) -> Decree:
        signingDate = self._signingDate.date()
        return Decree(
            id=self._decree.id,

            raa=self._decree.raa,
            startPage=self._startPage.value(),
            endPage=self._endPage.value(),

            docType=self._documentType.currentData(),
            number=self._number.text(),
            title=self._title.text(),
            signingDate=None if signingDate is None else signingDate.toPython(),  # type: ignore
        )
