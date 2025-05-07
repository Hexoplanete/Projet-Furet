from PySide6 import QtWidgets, QtCore
from furet import repository
from furet.types.decree import *

from furet.app.widgets.objectTableModel import ObjectTableModel, TableColumn
from furet.app.widgets.decreeFilterWidget import DecreeFilterWidget
from furet.app.windows.decreeDetailsWindow import DecreeDetailsWindow
from furet.app.windows.parametersWindow import ParametersWindow
from furet.types.department import Department

class DecreeTableWindow(QtWidgets.QMainWindow):


    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fouille Universelle de Recueils pour Entreposage et Traitement")
        self._content = QtWidgets.QWidget()
        self._layout = QtWidgets.QVBoxLayout(self._content)
        self.setCentralWidget(self._content)

        columns = [
            TableColumn[Department]("department", lambda: "Département"),
            TableColumn[DecreeTopic]("topic", lambda: "Sujet"),
            TableColumn[str]("title", lambda: "Titre"),
            TableColumn[date]("publicationDate", lambda: "Date de publication"),
            TableColumn[bool]("treated", lambda: "État", lambda v: "Traité" if v else "À traiter"),
            TableColumn[str]("comment", lambda: "Commentaire"),
        ]
        self._decrees = ObjectTableModel(repository.getDecrees(), columns)

        self._topBar = QtWidgets.QHBoxLayout()
        self._layout.addLayout(self._topBar)

        self._filters = DecreeFilterWidget()
        self._filters.setModel(self._decrees)
        self._topBar.addWidget(self._filters)
        
        self._paramButton = QtWidgets.QPushButton('Paramètres')
        self._paramButton.clicked.connect(self.onClickParamButton)
        self._topBar.addWidget(self._paramButton)
        
        self._table = QtWidgets.QTableView()
        self._table.sortByColumn(0, QtCore.Qt.SortOrder.AscendingOrder)
        self._table.setModel(self._filters.proxyModel())
        self._layout.addWidget(self._table, 1)
        self._table.doubleClicked.connect(self.onDblClickTableRow)

        self._table.setEditTriggers(QtWidgets.QTableView.EditTrigger.NoEditTriggers)
        self._table.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)
        self._table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self._table.horizontalHeader().setSectionResizeMode(len(columns)-1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self._table.setSortingEnabled(True)

        self._paramWindow: ParametersWindow = None
        self._decreeDetailWindows: dict[int, DecreeDetailsWindow] = {}

    def closeEvent(self, event):
        QtWidgets.QApplication.quit()

    def onClickParamButton(self):
        if self._paramWindow == None or not(self._paramWindow.isVisible()):
            self._paramWindow = ParametersWindow()
            self._paramWindow.show()
        else:
            self._paramWindow.activateWindow()

    def onDblClickTableRow(self, index: QtCore.QModelIndex):
        source_index = self._filters.proxyModel().mapToSource(index)
        decree = self._decrees.itemAt(source_index.row())
        if id not in self._decreeDetailWindows or not(self._decreeDetailWindows[id].isVisible()):
            self._decreeDetailWindows[decree.id] = DecreeDetailsWindow(decree)
            self._decreeDetailWindows[decree.id].show()
        else:
            self._decreeDetailWindows[decree.id].activateWindow()
