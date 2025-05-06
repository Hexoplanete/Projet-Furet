from PySide6 import QtWidgets, QtCore
from furet.types.Decree import *

from furet.ui.widgets.ObjectTableModel import ObjectTableModel, TableColumn
from furet.ui.widgets.DecreeFilterWidget import DecreeFilterWidget


def getFakeData() -> list[Decree]:
    return [
        Decree(0,73, None, "Test 1", None, None),
        Decree(1,73, None, "Test 2", None, None),
        Decree(2,73, None, "Test 3", None, None),
        Decree(3,73, None, "Test 5", None, None),
    ]


class DecreeTableWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fouille Universelle de Recueils pour Entreposage et Traitement")
        self._content = QtWidgets.QWidget()
        self._layout = QtWidgets.QVBoxLayout(self._content)
        self.setCentralWidget(self._content)

        columns = [
            TableColumn[str]("department", lambda: "Département"),
            TableColumn[DecreeTopic]("topic", lambda: "Sujet", lambda v: "" if v is None else v.label),
            TableColumn[str]("title", lambda: "Titre"),
            TableColumn[date]("publication_date", lambda: "Date de publication"),
            TableColumn[DecreeState]("state", lambda: "État", lambda v: "" if v is None else v.label)
        ]
        self.decrees = ObjectTableModel(getFakeData(), columns)

        self._topBar = QtWidgets.QHBoxLayout()
        self._layout.addLayout(self._topBar)

        filters = DecreeFilterWidget()
        filters.setModel(self.decrees)
        self._topBar.addWidget(filters)
        
        self._paramButton = QtWidgets.QPushButton('Paramètres')
        self._paramButton.clicked.connect(self.onClickParamButton)
        self._topBar.addWidget(self._paramButton)
        
        self._table = QtWidgets.QTableView()
        self._table.setModel(filters.proxyModel())
        self._layout.addWidget(self._table, 1)
        self._table.doubleClicked.connect(self.onDblClickTableRow)

        self._table.setEditTriggers(QtWidgets.QTableView.EditTrigger.NoEditTriggers)
        self._table.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)
        self._table.horizontalHeader().setSectionResizeMode(len(columns)-1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self._table.setSortingEnabled(True)
    
    def onSearchDecrees(self):
        pass
        # row = ["fuck", "fuck", "fuck", "fuck", "fuck"]
        # items = [QtGui.QStandardItem(str(name)) for name in row]
        # self.model.appendRow(items)

    def onClickParamButton(self):
        pass
        # row = ["shit", "shit", "shit", "shit", "shit"]
        # items = [QtGui.QStandardItem(str(name)) for name in row]
        # self.model.appendRow(items)

    def onDblClickTableRow(self, index: QtCore.QModelIndex):
        print(self.decrees.itemAt(index.row()).title)
