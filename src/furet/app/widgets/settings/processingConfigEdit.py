from PySide6 import QtWidgets
from furet.app.widgets.singlePathEdit import SinglePathEdit
from furet.app.widgets.formWidget import FormWidget
from furet.configs import ProcessingConfig


class ProcessingConfigEdit(FormWidget[ProcessingConfig]):

    def __init__(self, value: ProcessingConfig, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)

        self._pdfDir = SinglePathEdit(value.pdfDir, folder=True)
        self.addRow("Dossier de stockage des pdfs", self._pdfDir, "Le dossier où sont enregistrés les pdf des recueils")

        self._debug = QtWidgets.QCheckBox()
        self._debug.setChecked(value.debug)
        self.addRow("Conserver les fichiers intermédiaires", self._debug, "Conserver les fichiers intermédiaires générés par le traitement des recueils dans le sous dossier \".steps\"")

    # # TODO reset form fields
    # def setRaa(self, raa: RAA):
    #     self._raa = raa

    def value(self) -> ProcessingConfig:
        return ProcessingConfig(
            pdfDir=self._pdfDir.path(),
            debug=self._debug.isChecked()
        )
