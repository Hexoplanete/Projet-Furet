from typing import Callable
from PySide6 import QtWidgets, QtCore
from datetime import date
from dateutil.relativedelta import relativedelta

from furet.app.utils import addFormRow, buildDatePicker, buildMultiComboBox, formatDate
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
        self._datePopupLayout = QtWidgets.QFormLayout(self._datePopup)
        self._dateAfter = buildDatePicker(None)
        addFormRow(self._datePopupLayout, "Publié après le", self._dateAfter)
        self._dateBefore = buildDatePicker(None)
        addFormRow(self._datePopupLayout, "Publié avant le", self._dateBefore)

        if settings.value("app.filter-expired"):
            self._dateAfter.setDate(date.today() - relativedelta(months=2)) # type: ignore

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
        self.syncDateFilterLabel()
        self._layout.addWidget(self._state)


    def onClickResearchButton(self):
        self._onResearch()

    def filters(self) -> repository.DecreeFilters:
        return repository.DecreeFilters(
            after=None if self._dateAfter.date() is None else self._dateAfter.date().toPython(), # type: ignore
            before=None if self._dateBefore.date() is None else self._dateBefore.date().toPython(), # type: ignore
            departments=list(map(lambda v: v.id, self._department.currentData())),
            campaigns=list(map(lambda v: v.id, self._campaign.currentData())),
            topics=list(map(lambda v: v.id, self._topic.currentData())),
            name=self._name.text(),
            treated=self._state.currentData(),
        )

    def syncDateFilterLabel(self):
        dateAfter, dateBefore = self._dateAfter.date(), self._dateBefore.date()
        if dateAfter is None and dateBefore is None:
            self._dateRangeButton.setText("Toutes les dates de publication")
        elif dateAfter is not None and dateBefore is None:
            self._dateRangeButton.setText(f"Publié après le {formatDate(dateAfter.toPython())}") # type: ignore
        elif dateAfter is None and dateBefore is not None:
            self._dateRangeButton.setText(f"Publié avant le {formatDate(dateBefore.toPython())}") # type: ignore
        else:
            self._dateRangeButton.setText(f"Publié du {formatDate(dateAfter.toPython())} au {formatDate(dateBefore.toPython())}") # type: ignore
    
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
