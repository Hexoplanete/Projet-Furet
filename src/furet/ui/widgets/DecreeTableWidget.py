from PySide6 import QtWidgets, QtGui, QtCore

from furet.ui.fakedata import Decree


class DecreeTableModel(QtWidgets.QAbstractTableModel):
    def __init__(self, data: list[Decree]):
        super().__init__()
        self._data = data
        self.s

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data)


class DecreeTableWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self._content = QtWidgets.QWidget()
        self.setCentralWidget(self._content)

        self._tableView = QtWidgets.QTableView()
        self._tableView.doubleClicked.connect(self.onDblClickTableRow)

        # Modèle
        cols = ["department", "topic", "name", "publication_date", "state"]
        self._model = DecreeTableModel(getFakeData())
        self._tableView.setModel(self._model)
        # self.model.setHorizontalHeaderLabels(cols)

        # Données (ajoutées ligne par ligne)
        # data = getFakeData()

        # for row in data:
        #     items = [QtGui.QStandardItem(
        #         str(getattr(row, name))) for name in cols]
        #     self.model.appendRow(items)

        # Lier le modèle à la table
        self._tableView.setEditTriggers(QtWidgets.QTableView.EditTrigger.NoEditTriggers)
        self._tableView.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)
        self._tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self._tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        # self._tableView.horizontalHeader().setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)


    def onDblClickTableRow(self, index: QtCore.QModelIndex):
        print(index.row())
