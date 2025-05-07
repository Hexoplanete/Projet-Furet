from PySide6 import QtWidgets, QtCore

from furet.types.decree import *
from furet.app.widgets.objectTableModel import ObjectFilterProxy, ObjectTableModel
from furet import repository

class DecreeFilterWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QtWidgets.QHBoxLayout(self)

        self._proxy = ObjectFilterProxy[Decree](filterer=self.filterDecrees)
        
        self._department = QtWidgets.QComboBox()
        self._department.addItem(f"Choisir un département", 0)
        for d in repository.getDepartments():
            self._department.addItem(str(d), d.id)
        self._department.setEditable(True)
        self._layout.addWidget(self._department)


        self._topic = QtWidgets.QComboBox()
        self._topic.addItem(f"Choisir un topic", 0)
        for t in repository.getTopic():
            self._topic.addItem(t.label, t.id)
        self._topic.setEditable(True)
        self._layout.addWidget(self._topic)

        self._name = QtWidgets.QLineEdit()
        self._layout.addWidget(self._name)

        self._date = QtWidgets.QDateEdit()
        self._layout.addWidget(self._date)

        self._state = QtWidgets.QCheckBox()
        self._layout.addWidget(self._state)

        
        self._researchButton = QtWidgets.QPushButton('Rechercher')
        self._researchButton.clicked.connect(self.onClickResearchButton)
        self._layout.addWidget(self._researchButton)

        self._departementValue = 0
        self._topicValue = 0
        self._nameValue = ""
        self._dateValue = None
        self._stateValues = None


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
        self._stateValues = self._state.checkState()

        self._proxy.invalidateFilter()

        return
    
    def filterDecrees(self, decree: Decree):
        if self._departementValue > 0 and decree.department.id != self._departementValue: return False
        # if self._topicValue != 0 and decree.topic.id != self._topicValue: return False

        # if self._nameValue != "" and decree.title.find(self._nameValue) == -1: return False

        return True
