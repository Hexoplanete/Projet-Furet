from PySide6 import QtCore, QtWidgets

from furet import repository
from furet.app.widgets.multiComboBox import MultiComboBox
from furet.app.widgets.sectionHeaderWidget import SectionHeaderWidget
from furet.models.campaign import Campaign, Topic


class CampaignsEditWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Campagnes")

        self._layout = QtWidgets.QVBoxLayout(self)

        self._layout.addWidget(SectionHeaderWidget("Campagnes"))
        campaignsHeaders = QtWidgets.QGridLayout()
        campaignsHeaders.setContentsMargins(0, 0, 0, 0)
        campaignsHeaders.setColumnStretch(0, 1)
        campaignsHeaders.setColumnStretch(1, 3)
        campaignsHeaders.addWidget(QtWidgets.QLabel("Campagne", alignment=QtCore.Qt.AlignmentFlag.AlignCenter), 0, 0)
        campaignsHeaders.addWidget(QtWidgets.QLabel("Sujets", alignment=QtCore.Qt.AlignmentFlag.AlignCenter), 0, 1)
        self._layout.addLayout(campaignsHeaders)
        campaignsView = QtWidgets.QScrollArea(widgetResizable=True)
        campaignsView.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        self._layout.addWidget(campaignsView)
        campaignsView.setBackgroundRole(self.backgroundRole())
        campaignsWidget = QtWidgets.QWidget()
        self._campaignsLayout = QtWidgets.QGridLayout(campaignsWidget)
        self._campaignsLayout.setContentsMargins(0, 0, 0, 0)
        self._campaignsLayout.setColumnStretch(0, 1)
        self._campaignsLayout.setColumnStretch(1, 3)
        self._topicsList = repository.getTopics()
        self._campaigns: list[tuple[int,
                                    QtWidgets.QLineEdit, MultiComboBox[Topic]]] = []
        [self._addCampaign(c) for c in repository.getCampaigns()]
        self._campaignsButton = QtWidgets.QPushButton("Ajouter une campagne")
        self._campaignsButton.clicked.connect(self.createCampaign)
        self._layout.addWidget(self._campaignsButton)
        campaignsView.setWidget(campaignsWidget)

        self._layout.addWidget(SectionHeaderWidget("Sujets"))
        topicsView = QtWidgets.QScrollArea(widgetResizable=True)
        topicsView.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        topicsView.setBackgroundRole(self.backgroundRole())
        self._layout.addWidget(topicsView)
        topicsWidget = QtWidgets.QWidget()
        self._topicsLayout = QtWidgets.QVBoxLayout(topicsWidget)
        self._topicsLayout.setContentsMargins(0, 0, 0, 0)
        self._topics: list[tuple[int, QtWidgets.QLineEdit]] = []
        [self._addTopic(c) for c in repository.getTopics()]
        self._topicsButton = QtWidgets.QPushButton("Ajouter un sujet")
        self._topicsButton.clicked.connect(self.createTopic)
        self._layout.addWidget(self._topicsButton)
        topicsView.setWidget(topicsWidget)

        self._layout.addStretch(stretch=1)
        self._buttons = QtWidgets.QDialogButtonBox(standardButtons=QtWidgets.QDialogButtonBox.StandardButton.Save | QtWidgets.QDialogButtonBox.StandardButton.Close)
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)
        self._layout.addWidget(self._buttons)

    def createCampaign(self):
        campaign = Campaign(0, "", [])
        self._addCampaign(campaign)

    def _addCampaign(self, campaign: Campaign):
        label = QtWidgets.QLineEdit(campaign.label)
        topics = MultiComboBox(self._topicsList, campaign.topics)
        topics.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.InsertAtBottom)
        self._campaigns.append((campaign.id, label, topics))
        row = self._campaignsLayout.rowCount()
        self._campaignsLayout.addWidget(label, row, 0)
        self._campaignsLayout.addWidget(topics, row, 1)

    def createTopic(self):
        topic = Topic(0, "")
        self._addTopic(topic)
        for _, _, topics in self._campaigns:
            topics.addItem(topic)

    def _addTopic(self, topic: Topic):
        label = QtWidgets.QLineEdit(topic.label)
        label.textChanged.connect(lambda: self.updateTopics())
        self._topics.append((topic.id, label))
        self._topicsLayout.addWidget(label)

    def updateTopics(self):
        for i, (id, label) in enumerate(self._topics):
            for _, _, topics in self._campaigns:
                topics.setItem(i, Topic(id, label.text()))

    def accept(self) -> None:
        for id, label in self._topics:
            if len(label.text()) == 0:
                return

        for id, label, topics in self._campaigns:
            if len(label.text()) == 0:
                return

        for id, label in self._topics:
            topic = Topic(id=id, label=label.text())
            if topic.id == 0:
                repository.addTopic(topic)
            else:
                repository.updateTopic(topic.id, topic)

        for id, label, topics in self._campaigns:
            campaign = Campaign(id=id, label=label.text(),
                                topics=topics.selectedItems())
            if campaign.id == 0:
                repository.addCampaign(campaign)
            else:
                repository.updateCampaign(campaign.id, campaign)
        super().accept()
