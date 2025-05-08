from PySide6 import QtWidgets, QtCore

from furet.app.utils import buildComboBox
from furet.types.decree import *
from furet.app.widgets.objectTableModel import ObjectFilterProxy, ObjectTableModel
from furet import repository

class DecreeFilterWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QtWidgets.QHBoxLayout(self)

        self._proxy = ObjectFilterProxy[Decree](filterer=self.filterDecrees)
        
        self._department = buildComboBox(repository.getDepartments(), None, ("Choisir un département", None))
        self._layout.addWidget(self._department)


        self._topic = buildComboBox(repository.getTopics(), None, ("Choisir un sujet", None))
        self._layout.addWidget(self._topic)

        self._name = QtWidgets.QLineEdit(placeholderText="Choisir un titre")
        self._layout.addWidget(self._name)

        self._date = QtWidgets.QDateEdit() # TODO custom date picker widget
        self._layout.addWidget(self._date)

        self._state = QtWidgets.QComboBox()
        self._state.setEditable(True)
        self._state.addItem("Choisir un status", None)
        self._state.addItem("Traité", True)
        self._state.addItem("Non traité", False)
        self._state.setCurrentIndex(2)
        self._layout.addWidget(self._state)

        
        self._researchButton = QtWidgets.QPushButton('Rechercher')
        self._researchButton.clicked.connect(self.onClickResearchButton)
        self._layout.addWidget(self._researchButton)

        # Donne le numéro du département (0 si aucun)
        self._departementValue = self._department.currentData()
        self._topicValue = self._topic.currentData()
        self._nameValue = self._name.text()
        self._dateValue = self._date.date()
        self._stateValues = self._state.currentData()


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
        self._departementValue = self._department.currentData() # Donne le numéro du département (0 si aucun)
        self._topicValue = self._topic.currentData()
        self._nameValue = self._name.text()
        self._dateValue = self._date.date()
        self._stateValues = self._state.currentData()

        self._proxy.invalidateFilter()

        return
    
    def filterDecrees(self, decree: Decree):
        if self._departementValue is not None and decree.department.id != self._departementValue.id: return False
        if self._topicValue is not None and decree.topic.id != self._topicValue.id: return False
        if self._stateValues is not None and decree.treated != self._stateValues: return False
        if self._nameValue != "" and decree.title.lower().find(self._nameValue.lower()) == -1: return False
        if self._nameValue != "" and decree.title.lower().find(self._nameValue.lower()) == -1: return False

        return True
