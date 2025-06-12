from PySide6 import QtWidgets

from furet import settings
from furet import repository
from furet.app.utils import addFormSection
from furet.app.widgets.objectTableModel import SingleRowEditableModel
from furet.app.widgets.sectionHeaderWidget import SectionHeaderWidget
from furet.app.widgets.settings.appConfigEdit import AppConfigEdit
from furet.app.widgets.settings.repositoryConfigEdit import RepositoryConfigEdit
from furet.configs import AppConfig, RepositoryConfig


class SettingsWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paramètres")

        self._layout = QtWidgets.QVBoxLayout(self)

        self._layout.addWidget(SectionHeaderWidget("Interface"))
        self._app = AppConfigEdit(settings.config(AppConfig))
        self._layout.addWidget(self._app)

        topicCampaignSection = addFormSection(self._layout, "Sujet et Campagne")

        topicCampaign = QtWidgets.QHBoxLayout()
        
        def onCampaignChanged(topLeft, bottomRight, roles):
            for row in range(topLeft.row(), bottomRight.row() + 1):
                campaign = repository.getCampaigns()[row]
                repository.updateCampaign(campaign.id, campaign)

        self.modelCampaign = SingleRowEditableModel(repository.getCampaigns(), "Campagne")
        self.modelCampaign.dataChanged.connect(onCampaignChanged)
        self.viewCampaign = QtWidgets.QTableView()
        self.viewCampaign.setModel(self.modelCampaign)
        self.viewCampaign.verticalHeader().setVisible(False)
        self.viewCampaign.horizontalHeader().setStretchLastSection(True)

        def onTopicChanged(topLeft, bottomRight, roles):
            for row in range(topLeft.row(), bottomRight.row() + 1):
                topic = repository.getTopics()[row]
                repository.updateTopic(topic.id, topic)

        self.modelTopic = SingleRowEditableModel(repository.getTopics(), "Sujet")
        self.modelTopic.dataChanged.connect(onTopicChanged)
        self.viewTopic = QtWidgets.QTableView()
        self.viewTopic.setModel(self.modelTopic)
        self.viewTopic.verticalHeader().setVisible(False)
        self.viewTopic.horizontalHeader().setStretchLastSection(True)

        topicCampaign.addWidget(self.viewCampaign)
        topicCampaign.addWidget(self.viewTopic)

        self._layout.addLayout(topicCampaign)

        self._layout.addWidget(SectionHeaderWidget("Stockage"))
        self._repository = RepositoryConfigEdit(settings.config(RepositoryConfig))
        self._layout.addWidget(self._repository)

        self._buttons = QtWidgets.QDialogButtonBox(standardButtons=QtWidgets.QDialogButtonBox.StandardButton.Save | QtWidgets.QDialogButtonBox.StandardButton.Close)
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)
        self._layout.addWidget(self._buttons)

    def accept(self) -> None:
        settings.setConfig(self._app.value())
        settings.setConfig(self._repository.value())
        super().accept()
