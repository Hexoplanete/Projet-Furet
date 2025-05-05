from PySide6 import QtWidgets, QtGui, QtCore
from ..fakedata import *
# from ..widgets.DecreeTableWidget import DecreeTableWidget


def getFakeData() -> list[Decree]:
    return [
        Decree(73, Topic.Wolf, "Test 1", None, DecreeState.Done),
        Decree(73, Topic.Wolf, "Test 2", None, DecreeState.Done),
        Decree(73, Topic.Wolf, "Test 3", None, DecreeState.Done),
        Decree(73, Topic.Wolf, "Test 5", None, DecreeState.Done),
    ]


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MainWindow")

        self._content = QtWidgets.QWidget()
        self.setCentralWidget(self._content)
        self._layout = QtWidgets.QVBoxLayout(self._content)

        self._topBar = QtWidgets.QHBoxLayout()
        self._layout.addLayout(self._topBar)

        self._filter = QtWidgets.QLineEdit()
        self._topBar.addWidget(self._filter)

        self._researchButton = QtWidgets.QPushButton('Rechercher')
        self._researchButton.clicked.connect(self.onClickResearchButton)
        self._topBar.addWidget(self._researchButton)

        self._paramButton = QtWidgets.QPushButton('Paramètres')
        self._paramButton.clicked.connect(self.onClickParamButton)
        self._topBar.addWidget(self._paramButton)
        
        # self._table = DecreeTableWidget()
        self._tableView = QtWidgets.QTableView()
        self._tableView.doubleClicked.connect(self.onDblClickTableRow)

        # Modèle
        cols = ["department", "topic", "name", "publication_date", "state"]
        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(cols)

        # Données (ajoutées ligne par ligne)
        data = getFakeData()

        for row in data:
            items = [QtGui.QStandardItem(str(getattr(row, name))) for name in cols]
            self.model.appendRow(items)

        # Lier le modèle à la table
        self._tableView.setModel(self.model)
        self._tableView.setEditTriggers(QtWidgets.QTableView.EditTrigger.NoEditTriggers)
        self._tableView.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)
        self._tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self._tableView.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self._tableView.horizontalHeader().setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)


        self._layout.addWidget(self._tableView)
    

    def onClickResearchButton(self):
        row = ["fuck", "fuck", "fuck", "fuck", "fuck"]
        items = [QtGui.QStandardItem(str(name)) for name in row]
        self.model.appendRow(items)

    def onClickParamButton(self):
        row = ["shit", "shit", "shit", "shit", "shit"]
        items = [QtGui.QStandardItem(str(name)) for name in row]
        self.model.appendRow(items)

    def onDblClickTableRow(self, index: QtCore.QModelIndex):
        print(index.row())




