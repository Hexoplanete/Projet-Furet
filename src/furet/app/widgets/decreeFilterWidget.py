from PySide6 import QtWidgets, QtCore
from datetime import date
from dateutil.relativedelta import relativedelta

from furet.app.utils import buildComboBox, buildDatePicker, buildMultiComboBox, formatDate
from furet.types.decree import *
from furet.app.widgets.objectTableModel import ObjectFilterProxy, ObjectTableModel
from furet import repository, settings

class DecreeFilterWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setContentsMargins(0,0,0,0)

        self._proxy = ObjectFilterProxy[Decree](filterer=self.filterDecrees)
        
        self._addDateFilter()
        
        self._department = buildComboBox(repository.getDepartments(), None, ("Choisir un département", None))
        self._layout.addWidget(self._department)


        self._campaign = buildComboBox(repository.getCampaigns(), None, ("Choisir une campagne", None))
        self._layout.addWidget(self._campaign)

        self._topic = buildMultiComboBox(repository.getTopics(), [], "Choisir un sujet")
        self._layout.addWidget(self._topic)

        self._name = QtWidgets.QLineEdit(placeholderText="Choisir un titre")
        self._layout.addWidget(self._name)

        self._addTreatedFilter()

        self._researchButton = QtWidgets.QPushButton('Rechercher')
        self._researchButton.clicked.connect(self.onClickResearchButton)
        self._layout.addWidget(self._researchButton)

        self.syncFilters()

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
        self._state.addItem("Choisir un statut", None)
        self._state.addItem("Traité", True)
        self._state.addItem("Non traité", False)
        self._state.setCurrentIndex(2 if settings.value("app.filter-treated") else 0)
        self._dateAfterToggle.setChecked(settings.value("app.filter-expired"))
        self._dateBeforeToggle.setChecked(settings.value("app.filter-expired"))
        self.syncDateFilterLabel()
        self._layout.addWidget(self._state)


    def syncFilters(self):
        self._departementValue = self._department.currentData()
        self._topicValue = self._topic.currentData()
        self._nameValue = self._name.text()
        self._dateAfterValue = None if not self._dateAfterToggle.isChecked() else self._dateAfter.date().toPython()
        self._dateBeforeValue = None if not self._dateBeforeToggle.isChecked() else self._dateBefore.date().toPython()
        self._stateValues = self._state.currentData()
        self._campaignValues = self._state.currentData()


    def data(self, index, /, role = ...):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return getattr(self._data[index.row()], self._fields[index.column()])

    def rowCount(self, /, parent = ...):
        return len(self._data)
    
    def setModel(self, model: ObjectTableModel[Decree]):
        self._model = model
        self._proxy.setSourceModel(model)

    def proxyModel(self) -> ObjectFilterProxy[Decree]:
        return self._proxy
    
    def onClickResearchButton(self):
        self.syncFilters()
        self._proxy.invalidateFilter()
        return
    
    def filterDecrees(self, decree: Decree):
        if self._departementValue is not None and decree.department.id != self._departementValue.id: return False
        if self._stateValues is not None and decree.treated != self._stateValues: return False
        if self._campaignValues is not None and self._campaignValues not in decree.campaigns: return False
        if self._nameValue != "" and decree.title.lower().find(self._nameValue.lower()) == -1: return False
        if self._dateAfterValue is not None and decree.publicationDate < self._dateAfterValue: return False
        if self._dateBeforeValue is not None and decree.publicationDate > self._dateBeforeValue: return False
        if len(self._topicValue) > 0:
            for id in self._topicValue:
                if id not in decree.topics: return False
        
        if len(self._topicValue) > 0:
            if id not in decree.topics: return False
    
        return True

    def syncDateFilterLabel(self):
        if not self._dateBeforeToggle.isChecked() and not self._dateAfterToggle.isChecked():
            self._dateRangeButton.setText("Choisir une date de publication")
        elif self._dateBeforeToggle.isChecked() and not self._dateAfterToggle.isChecked():
            self._dateRangeButton.setText(f"Publié avant le {formatDate(self._dateBefore.date().toPython())}")
        elif not self._dateBeforeToggle.isChecked() and self._dateAfterToggle.isChecked():
            self._dateRangeButton.setText(f"Publié après le {formatDate(self._dateAfter.date().toPython())}")
        else:
            self._dateRangeButton.setText(f"Publié du {formatDate(self._dateAfter.date().toPython())} au {formatDate(self._dateBefore.date().toPython())}")