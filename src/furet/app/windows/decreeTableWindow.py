from PySide6 import QtWidgets, QtCore, QtGui
from furet import repository
from furet.app.utils import formatDate
from furet.types.decree import *
from dateutil.relativedelta import relativedelta

from furet.app.widgets.objectTableModel import ObjectTableModel, TableColumn
from furet.app.widgets.decreeFilterWidget import DecreeFilterWidget
from furet.app.windows.decreeDetailsWindow import DecreeDetailsWindow
from furet.app.windows.settingsWindow import SettingsWindow
from furet.app.windows.importFileWindow import ImportFileWindow
from furet.types.department import Department


class DecreeTableWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self._content = QtWidgets.QWidget()
        self._layout = QtWidgets.QVBoxLayout(self._content)
        self.setCentralWidget(self._content)

        self._columns = [
            TableColumn[date]("publicationDate", lambda: "Date de publication", lambda v: formatDate(v)),                         # 0
            TableColumn[date]("publicationDate", lambda: "Date d'expiration", lambda v: formatDate(v + relativedelta(months=2))), # 1
            TableColumn[Department]("department", lambda: "Département"),                                                         # 2
            TableColumn[Campaign]("campaigns", lambda: "Campagnes", lambda v: ", ".join(map(str, v))),                                                              # 3
            TableColumn[list[DecreeTopic]]("topics", lambda: "Sujets", lambda v: ", ".join(map(str, v))),                         # 4
            TableColumn[str]("title", lambda: "Titre"),                                                                           # 5
            TableColumn[bool]("treated", lambda: "État", lambda v: "Traité" if v else "À traiter"),                               # 6
            TableColumn[bool]("missingData", lambda: "À compléter", lambda v: "Oui" if v else "Non"),                             # 7
            TableColumn[str]("comment", lambda: "Commentaire"),                                                                   # 8
        ]
        self._decrees = ObjectTableModel(repository.getDecrees(), self._columns)

        self._topBar = QtWidgets.QVBoxLayout()
        self._topBar.setContentsMargins(0,0,0,0)
        self._buttonLayer = QtWidgets.QHBoxLayout()
        self._buttonLayer.setContentsMargins(0,0,0,0)
        self._layout.addLayout(self._topBar)
        
        self._fileButton = QtWidgets.QPushButton('Importer un recueil')
        self._fileButton.clicked.connect(self.onClickImportButton)
        self._buttonLayer.addWidget(self._fileButton)

        self._buttonLayer.addStretch()

        self._docButton = QtWidgets.QPushButton('Documentation')
        self._docButton.clicked.connect(self.onClickDocButton)
        self._buttonLayer.addWidget(self._docButton)           
        
        self._paramButton = QtWidgets.QPushButton('Paramètres')
        self._paramButton.clicked.connect(self.onClickParamButton)
        self._buttonLayer.addWidget(self._paramButton)
        
        self._topBar.addLayout(self._buttonLayer)

        self._filters = DecreeFilterWidget()
        self._filters.setModel(self._decrees)
        self._topBar.addWidget(self._filters)

        self._table = QtWidgets.QTableView()
        self._table.setModel(self._filters.proxyModel())
        self._layout.addWidget(self._table, 1)
        self._table.doubleClicked.connect(self.onDblClickTableRow)

        self._table.setEditTriggers(QtWidgets.QTableView.EditTrigger.NoEditTriggers)
        self._table.setSelectionMode(QtWidgets.QTableView.SelectionMode.SingleSelection)
        self._table.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)
        self._table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self._table.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self._table.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self._table.horizontalHeader().setSectionResizeMode(8, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self._table.setSortingEnabled(False) # YA UN BUG AVEC TRUE
        # self._table.sortByColumn(1, QtCore.Qt.SortOrder.DescendingOrder)

        self._paramWindow: SettingsWindow = None
        self._importFileWindow: ImportFileWindow = None
        self._decreeDetailWindows: dict[int, DecreeDetailsWindow] = {}

    def closeEvent(self, event):
        QtWidgets.QApplication.quit()

    def onClickParamButton(self):
        if self._paramWindow == None or not(self._paramWindow.isVisible()):
            self._paramWindow = SettingsWindow(self)
            self._paramWindow.show()
        else:
            self._paramWindow.activateWindow()

    def onDblClickTableRow(self, index: QtCore.QModelIndex):
        source_index = self._filters.proxyModel().mapToSource(index)
        decree = self._decrees.itemAt(source_index.row())
        id = decree.id
        def onDecreeSaved():
            repository.updateDecree(id, self._decreeDetailWindows[decree.id].decree())
            self._decrees.resetData(repository.getDecrees())

        if decree.id not in self._decreeDetailWindows or not(self._decreeDetailWindows[decree.id].isVisible()):
            self._decreeDetailWindows[decree.id] = DecreeDetailsWindow(decree)
            self._decreeDetailWindows[decree.id].show()
            self._decreeDetailWindows[decree.id]._returnButton.setFocus()
            self._decreeDetailWindows[decree.id].accepted.connect(onDecreeSaved)
        else:
            self._decreeDetailWindows[decree.id].activateWindow()

    def onClickImportButton(self):
        def onImportDone():
            self._decrees.resetData(repository.getDecrees())

        if self._importFileWindow == None or not(self._importFileWindow.isVisible()):
            self._importFileWindow = ImportFileWindow()
            self._importFileWindow.show()
            self._importFileWindow.accepted.connect(onImportDone)
        else:
            self._importFileWindow.activateWindow()

    def onClickDocButton(self):
        QtGui.QDesktopServices.openUrl("https://github.com/Hexoplanete/Projet-Furet/wiki")

    def updateTopicsComboBox(self):
        self._filters.updateTopicsComboBox()

    def updateCampaignsComboBox(self):
        self._filters.updateCampaignsComboBox()
