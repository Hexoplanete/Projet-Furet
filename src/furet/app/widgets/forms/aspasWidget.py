from PySide6 import QtCore, QtWidgets

from furet import repository
from furet.app.utils import buildMultiComboBox
from furet.app.widgets.formWidget import FormWidget
from furet.types.decree import AspasInfo


class AspasInfoWidget(FormWidget):

    def __init__(self, info: AspasInfo, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._info = info

        self._campaign = buildMultiComboBox(repository.getCampaigns(), info.campaigns)
        self.addRow("Campagne", self._campaign)

        topicWidget = QtWidgets.QWidget()
        topicLayout = QtWidgets.QHBoxLayout(topicWidget)
        topicLayout.setContentsMargins(0, 0, 0, 0)
        topicLayout.setSpacing(0)

        self._topic = buildMultiComboBox(repository.getTopics(), info.topics)
        self._topic.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        topicLayout.addWidget(self._topic)

        self._unselectTopic = QtWidgets.QPushButton()
        self._unselectTopic.setIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_TrashIcon))
        self._unselectTopic.setContentsMargins(0, 0, 0, 0)
        self._unselectTopic.setToolTip("Bouton qui désélectionne tous les sujets de la liste.")
        self._unselectTopic.clicked.connect(self.onClickUnselectTopic)
        topicLayout.addWidget(self._unselectTopic, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        self.addRow("Sujet", topicWidget)

        self._treated = QtWidgets.QCheckBox("", )
        self._treated.setChecked(info.treated)
        self.addRow("Traité", self._treated)

        self._comment = QtWidgets.QTextEdit(plainText=info.comment)
        self.addRow("Commentaire", self._comment)

    # # TODO reset form fields
    # def setInfo(self, decree: DECREE):
    #     self._decree = decree

    def info(self) -> AspasInfo:
        return AspasInfo(
            treated=self._treated.isChecked(),
            campaigns=self._campaign.currentData(),
            topics=self._topic.currentData(),
            comment=self._comment.toPlainText(),
        )

    def onClickUnselectTopic(self):
        self._topic.unselectAllItems()
