from PySide6 import QtWidgets

from furet import repository
from furet.app.widgets.formWidget import FormWidget
from furet.app.widgets.multiComboBox import MultiComboBox
from furet.models.decree import AspasInfo


class AspasInfoEdit(FormWidget[AspasInfo]):

    def __init__(self, info: AspasInfo, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)

        self._campaign = MultiComboBox(repository.getCampaigns(), info.campaigns)
        self.addRow("Campagne", self._campaign)
    
        self._topic = MultiComboBox(repository.getTopics(), info.topics)
        self.addRow("Sujet", self._topic)

        self._treated = QtWidgets.QCheckBox("", )
        self._treated.setChecked(info.treated)
        self.addRow("Traité", self._treated)

        self._comment = QtWidgets.QTextEdit(plainText=info.comment)
        self.addRow("Commentaire", self._comment)

    # # TODO reset form fields
    # def setInfo(self, decree: DECREE):
    #     self._decree = decree

    def value(self) -> AspasInfo:
        return AspasInfo(
            treated=self._treated.isChecked(),
            campaigns=self._campaign.selectedItems(),
            topics=self._topic.selectedItems(),
            comment=self._comment.toPlainText(),
        )
