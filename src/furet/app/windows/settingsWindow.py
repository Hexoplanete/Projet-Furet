from PySide6 import QtWidgets, QtCore, QtGui

from furet import settings
from furet.app.widgets.filePickerWidget import FilePickerWidget, PickMode
from furet.app.widgets.textSeparatorWidget import TextSeparatorWidget
from furet.app.utils import addFormRow


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
        
        form = addSection("Interface")
        self.scale = QtWidgets.QLineEdit(str(settings.value("app.scale")))
        validator = QtGui.QDoubleValidator()
        validator.setLocale(QtCore.QLocale.English)
        self.scale.setValidator(validator)
        self.scale.textChanged.connect(lambda v: settings.setValue("app.scale", min(max(1, int(v)), 2)))
        addFormRow(form, "Échelle de l'interface", self.scale, "Change l'échelle de l'interface. Relancez l'application pour appliquer les changements.")

        self.treaded = QtWidgets.QCheckBox("")
        self.treaded.setChecked(settings.value("app.filter-treated"))
        self.treaded.stateChanged.connect(lambda v: settings.setValue("app.filter-treated", bool(v)))
        addFormRow(form, "Filter les arrêtés traités", self.treaded, "Filter automatiquement les arrêtés traites lors du lancement de l'application")

        self.expired = QtWidgets.QCheckBox("")
        self.expired.setChecked(settings.value("app.filter-expired"))
        self.expired.stateChanged.connect(lambda v: settings.setValue("app.filter-expired", bool(v)))
        addFormRow(form, "Filter les arrêtés expirés", self.expired, "Filter automatiquement les arrêtés de plus de 2 mois lors du lancement de l'application")

        form = addSection("Stockage")
        self.csvRoot = FilePickerWidget(settings.value("repository.csv-root"), pickMode=PickMode.Folder, onDataChange=lambda p: settings.setValue("repository.csv-root", p))
        addFormRow(form, "Dossier de stockage des arrêtés", self.csvRoot, "Le dossier où sont enregistrées les données des arrêtés")