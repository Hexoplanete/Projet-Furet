from PySide6 import QtWidgets
from furet.app.widgets.formWidget import FormWidget
from furet.configs import AppConfig


class AppConfigEdit(FormWidget[AppConfig]):

    def __init__(self, value: AppConfig, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)

        self._scale = QtWidgets.QDoubleSpinBox(value=value.scale, minimum=0.5, maximum=5)
        self.addRow("Échelle de l'interface", self._scale,"L'échelle de l'interface")

        self._filterTreated = QtWidgets.QCheckBox("")
        self._filterTreated.setChecked(value.filterTreated)
        self.addRow("Filter les arrêtés traités", self._filterTreated,"Filter automatiquement les arrêtés traites lors du lancement de l'application")

        self._filterExpired = QtWidgets.QCheckBox("")
        self._filterExpired.setChecked(value.filterExpired)
        self.addRow("Filter les arrêtés expirés", self._filterExpired,"Filter automatiquement les arrêtés de plus de 2 mois lors du lancement de l'application")

    def value(self) -> AppConfig:
        return AppConfig(
            scale=self._scale.value(),
            filterTreated=self._filterTreated.isChecked(),
            filterExpired=self._filterExpired.isChecked(),
        )
