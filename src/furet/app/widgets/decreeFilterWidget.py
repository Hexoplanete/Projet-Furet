from typing import Callable
from PySide6 import QtWidgets, QtCore
from datetime import date
from dateutil.relativedelta import relativedelta

from furet.app.utils import buildDatePicker, buildMultiComboBox, formatDate
from furet.types.decree import *
from furet import repository, settings

class DecreeFilterWidget(QtWidgets.QWidget):
    def __init__(self, onResearch: Callable[[], None]):
        super().__init__()

        self._onResearch = onResearch
        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setContentsMargins(0,0,0,0)
        
        self._addDateFilter()
        
        self._department = buildMultiComboBox(repository.getDepartments(), [], "Tous les départements")
        self._layout.addWidget(self._department)


        self._campaign = buildMultiComboBox(repository.getCampaigns(), [], "Toutes les campagnes")
        self._layout.addWidget(self._campaign)

        self._topic = buildMultiComboBox(repository.getTopics(), [], "Tous les sujets")
        self._layout.addWidget(self._topic)

        self._unselectTopic = QtWidgets.QPushButton('X')
        self._unselectTopic.setFixedSize(20,20)
        self._unselectTopic.setContentsMargins(0,0,0,0)
        self._unselectTopic.setToolTip("Bouton qui désélectionne tous les sujets de la liste.")
        self._unselectTopic.clicked.connect(self.onClickUnselectTopic)
        self._layout.addWidget(self._unselectTopic, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

        self._name = QtWidgets.QLineEdit(placeholderText="Tous les titres")
        self._layout.addWidget(self._name)

        self._addTreatedFilter()

        self._researchButton = QtWidgets.QPushButton('Rechercher')
        self._researchButton.clicked.connect(self.onClickResearchButton)
        self._layout.addWidget(self._researchButton)

    def _addDateFilter(self):
        self._datePopup = QtWidgets.QWidget()
        self._datePopupLayout = QtWidgets.QVBoxLayout(self._datePopup)
        self._dateAfterToggle = QtWidgets.QCheckBox("Publié après le")
        self._datePopupLayout.addWidget(self._dateAfterToggle)
        self._dateAfter = buildDatePicker(date.today() - relativedelta(months=2))
        self._datePopupLayout.addWidget(self._dateAfter)
        self._dateAfter.setEnabled(False)
        self._dateAfterToggle.stateChanged.connect(self._dateAfter.setEnabled)
        self._dateSep = QtWidgets.QFrame(frameShape=QtWidgets.QFrame.Shape.HLine)
        self._datePopupLayout.addWidget(self._dateSep)
        self._dateBeforeToggle = QtWidgets.QCheckBox("Publié avant le")
        self._datePopupLayout.addWidget(self._dateBeforeToggle)
        self._dateBefore = buildDatePicker(date.today())
        self._datePopupLayout.addWidget(self._dateBefore)
        self._dateBefore.setEnabled(False)
        self._dateBeforeToggle.stateChanged.connect(self._dateBefore.setEnabled)

        self._dateRangeButton = QtWidgets.QPushButton("")
        self._layout.addWidget(self._dateRangeButton)
        self._dateMenu = QtWidgets.QMenu("Date range")
        self._dateMenu.aboutToHide.connect(self.syncDateFilterLabel)
        self._dateAction = QtWidgets.QWidgetAction(self._dateRangeButton)
        self._dateAction.setDefaultWidget(self._datePopup)
        self.syncDateFilterLabel()

        self._dateMenu.addAction(self._dateAction)
        self._dateRangeButton.setMenu(self._dateMenu)

    def _addTreatedFilter(self):
        self._state = QtWidgets.QComboBox()
        self._state.setEditable(True)
        self._state.addItem("Tous les statuts", None)
        self._state.addItem("Traité", True)
        self._state.addItem("Non traité", False)
        self._state.setCurrentIndex(2 if settings.value("app.filter-treated") else 0)
        self._dateAfterToggle.setChecked(settings.value("app.filter-expired"))
        self._dateBeforeToggle.setChecked(settings.value("app.filter-expired"))
        self.syncDateFilterLabel()
        self._layout.addWidget(self._state)


    def onClickResearchButton(self):
        self._onResearch()

    def filters(self) -> repository.decrees.DecreeFilters:
        return repository.decrees.DecreeFilters(
            after=None if not self._dateAfterToggle.isChecked() else self._dateAfter.date().toPython(),
            before=None if not self._dateBeforeToggle.isChecked() else self._dateBefore.date().toPython(),
            departments=list(map(lambda v: v.id, self._department.currentData())),
            campaigns=list(map(lambda v: v.id, self._campaign.currentData())),
            topics=list(map(lambda v: v.id, self._topic.currentData())),
            name=self._name.text(),
            treated=self._state.currentData(),
        )

    def syncDateFilterLabel(self):
        if not self._dateBeforeToggle.isChecked() and not self._dateAfterToggle.isChecked():
            self._dateRangeButton.setText("Choisir une date de publication")
        elif self._dateBeforeToggle.isChecked() and not self._dateAfterToggle.isChecked():
            self._dateRangeButton.setText(f"Publié avant le {formatDate(self._dateBefore.date().toPython())}")
        elif not self._dateBeforeToggle.isChecked() and self._dateAfterToggle.isChecked():
            self._dateRangeButton.setText(f"Publié après le {formatDate(self._dateAfter.date().toPython())}")
        else:
            self._dateRangeButton.setText(f"Publié du {formatDate(self._dateAfter.date().toPython())} au {formatDate(self._dateBefore.date().toPython())}")
    
    def onClickUnselectTopic(self):
        self._topic.unselectAllItems()

    def updateTopicsComboBox(self):
        self._topic.blockSignals(True)
        isChecked = []
        for i in range(self._topic.length()):
            isChecked.append(self._topic.isChecked(i))
        while self._topic.length():
            self._topic.removeItem(1)
        i = 0
        for t in repository.getTopics():
            self._topic.addItem(str(t), userData = t)
            self._topic.setSelectedIndex(i, isChecked[i])
            i += 1
        self._topic.blockSignals(False)

    def updateCampaignsComboBox(self):
        self._campaign.blockSignals(True)
        index = self._campaign.currentIndex()
        self._campaign.clear()
        self._campaign.addItem("Toutes les campagnes", None)
        for c in repository.getCampaigns():
            self._campaign.addItem(str(c), c)
        self._campaign.setCurrentIndex(index)
        self._campaign.blockSignals(False)
