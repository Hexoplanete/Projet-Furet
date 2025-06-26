from PySide6 import QtWidgets
from furet.app.widgets.singlePathEdit import SinglePathEdit
from furet.app.widgets.formWidget import FormWidget
from furet.settings.configs import RepositoryConfig


class RepositoryConfigEdit(FormWidget[RepositoryConfig]):

    def __init__(self, value: RepositoryConfig, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)

        self._csvRoot = SinglePathEdit(value.csvRoot, id="csv-root", folder=True)
        self.addRow("Dossier de stockage des arrêtés", self._csvRoot,"Le dossier où sont enregistrées les données des arrêtés")

    def value(self) -> RepositoryConfig:
        return RepositoryConfig(
            csvRoot=self._csvRoot.path()
        )
