from PySide6 import QtWidgets

from furet import settings
from furet.app.widgets.sectionHeaderWidget import SectionHeaderWidget
from furet.app.widgets.settings.appConfigEdit import AppConfigEdit
from furet.app.widgets.settings.processingConfigEdit import ProcessingConfigEdit
from furet.app.widgets.settings.repositoryConfigEdit import RepositoryConfigEdit
from furet.settings.configs import AppConfig, ProcessingConfig, RepositoryConfig


class SettingsWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paramètres")

        self._layout = QtWidgets.QVBoxLayout(self)

        self._layout.addWidget(SectionHeaderWidget("Interface"))
        self._app = AppConfigEdit(settings.config(AppConfig))
        self._layout.addWidget(self._app)

        self._layout.addWidget(SectionHeaderWidget("Stockage"))
        self._repository = RepositoryConfigEdit(settings.config(RepositoryConfig))
        self._layout.addWidget(self._repository)

        self._layout.addWidget(SectionHeaderWidget("Traitement"))
        self._processing = ProcessingConfigEdit(settings.config(ProcessingConfig))
        self._layout.addWidget(self._processing)

        self._layout.addStretch(stretch=1)
        self._buttons = QtWidgets.QDialogButtonBox(standardButtons=QtWidgets.QDialogButtonBox.StandardButton.Save | QtWidgets.QDialogButtonBox.StandardButton.Close)
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)
        self._layout.addWidget(self._buttons)

    def accept(self) -> None:
        settings.setConfig(self._app.value())
        settings.setConfig(self._repository.value())
        settings.setConfig(self._processing.value())
        super().accept()
