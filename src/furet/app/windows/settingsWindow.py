from PySide6 import QtWidgets

from furet import settings
from furet.app.widgets.textSeparatorWidget import TextSeparatorWidget

class SettingsWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paramètres")

        self._rootLayout = QtWidgets.QVBoxLayout(self)

        def addSection(label: str):
            if self._rootLayout.count() > 0:
                self._rootLayout.addSpacing(20)
            sep = TextSeparatorWidget(label)
            sep = self._rootLayout.addWidget(sep)
            form = QtWidgets.QFormLayout()
            self._rootLayout.addLayout(form)
            return form
        
        form = addSection("Filtres par défaut")
        self._treatedOnOpen = QtWidgets.QCheckBox("")
        self._treatedOnOpen.setChecked(settings.value("app.filters.treatedOnly"))
        self._treatedOnOpen.stateChanged.connect(lambda v: settings.setValue("app.filters.treatedOnly", bool(v)))
        form.addRow("Non traités par défaut", self._treatedOnOpen)
        
        self._notExpired = QtWidgets.QCheckBox("")
        self._notExpired.setChecked(settings.value("app.filters.notExpired"))
        self._notExpired.stateChanged.connect(lambda v: settings.setValue("app.filters.notExpired", bool(v)))
        form.addRow("Non expirés", self._notExpired)