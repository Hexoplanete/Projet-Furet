from PySide6 import QtWidgets, QtCore, QtGui

from furet import settings
from furet.app.widgets.filePickerWidget import FilePickerWidget, PickMode
from furet.app.widgets.textSeparatorWidget import TextSeparatorWidget
from furet import repository
from furet.app.utils import addFormRow
from furet.types.decree import *
from furet.app.widgets.objectTableModel import singleRowEditableModel


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
        self.scale.textChanged.connect(lambda v: settings.setValue("app.scale", min(max(1, float(v)), 2)))
        addFormRow(form, "Échelle de l'interface", self.scale, "Change l'échelle de l'interface. Relancez l'application pour appliquer les changements.")

        self.treaded = QtWidgets.QCheckBox("")
        self.treaded.setChecked(settings.value("app.filter-treated"))
        self.treaded.stateChanged.connect(lambda v: settings.setValue("app.filter-treated", bool(v)))
        addFormRow(form, "Filter les arrêtés traités", self.treaded, "Filter automatiquement les arrêtés traites lors du lancement de l'application")

        self.expired = QtWidgets.QCheckBox("")
        self.expired.setChecked(settings.value("app.filter-expired"))
        self.expired.stateChanged.connect(lambda v: settings.setValue("app.filter-expired", bool(v)))
        addFormRow(form, "Filter les arrêtés expirés", self.expired, "Filter automatiquement les arrêtés de plus de 2 mois lors du lancement de l'application")

        topicCampaignSection = addSection("Sujet et Campagne")

        topicCampaign = QtWidgets.QHBoxLayout()
        
        def onCampaignChanged(topLeft, bottomRight, roles):
            for row in range(topLeft.row(), bottomRight.row() + 1):
                campaign = repository.getCampaigns()[1:][row]
                print(f"Modifié : ID={campaign.id}, Nouveau label='{campaign.label}'")

        self.modelCampaign = singleRowEditableModel(repository.getCampaigns()[1:], "Campagne")
        self.modelCampaign.dataChanged.connect(onCampaignChanged)
        self.viewCampaign = QtWidgets.QTableView()
        self.viewCampaign.setModel(self.modelCampaign)
        self.viewCampaign.verticalHeader().setVisible(False)
        self.viewCampaign.horizontalHeader().setStretchLastSection(True)

        def onTopicChanged(topLeft, bottomRight, roles):
            for row in range(topLeft.row(), bottomRight.row() + 1):
                topic = repository.getTopics()[row]
                print(f"Modifié : ID={topic.id}, Nouveau label='{topic.label}'")

        self.modelTopic = singleRowEditableModel(repository.getTopics(), "Sujet")
        self.modelTopic.dataChanged.connect(onTopicChanged)
        self.viewTopic = QtWidgets.QTableView()
        self.viewTopic.setModel(self.modelTopic)
        self.viewTopic.verticalHeader().setVisible(False)
        self.viewTopic.horizontalHeader().setStretchLastSection(True)

        topicCampaign.addWidget(self.viewCampaign)
        topicCampaign.addWidget(self.viewTopic)

        self._rootLayout.addLayout(topicCampaign)

        topicCampaignSection = addSection("Sujet et Campagne")

        topicCampaign = QtWidgets.QHBoxLayout()
        
        def onCampaignChanged(topLeft, bottomRight, roles):
            for row in range(topLeft.row(), bottomRight.row() + 1):
                campaign = repository.getCampaigns()[1:][row]
                print(f"Modifié : ID={campaign.id}, Nouveau label='{campaign.label}'")

        self.modelCampaign = singleRowEditableModel(repository.getCampaigns()[1:], "Campagne")
        self.modelCampaign.dataChanged.connect(onCampaignChanged)
        self.viewCampaign = QtWidgets.QTableView()
        self.viewCampaign.setModel(self.modelCampaign)
        self.viewCampaign.verticalHeader().setVisible(False)
        self.viewCampaign.horizontalHeader().setStretchLastSection(True)

        def onTopicChanged(topLeft, bottomRight, roles):
            for row in range(topLeft.row(), bottomRight.row() + 1):
                topic = repository.getTopics()[row]
                print(f"Modifié : ID={topic.id}, Nouveau label='{topic.label}'")

        self.modelTopic = singleRowEditableModel(repository.getTopics(), "Sujet")
        self.modelTopic.dataChanged.connect(onTopicChanged)
        self.viewTopic = QtWidgets.QTableView()
        self.viewTopic.setModel(self.modelTopic)
        self.viewTopic.verticalHeader().setVisible(False)
        self.viewTopic.horizontalHeader().setStretchLastSection(True)

        topicCampaign.addWidget(self.viewCampaign)
        topicCampaign.addWidget(self.viewTopic)

        self._rootLayout.addLayout(topicCampaign)

        form = addSection("Stockage")
        self.csvRoot = FilePickerWidget(settings.value("repository.csv-root"), pickMode=PickMode.Folder, onDataChange=lambda p: settings.setValue("repository.csv-root", p))
        addFormRow(form, "Dossier de stockage des arrêtés", self.csvRoot, "Le dossier où sont enregistrées les données des arrêtés")