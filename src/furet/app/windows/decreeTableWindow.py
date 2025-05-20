from PySide6 import QtWidgets, QtCore, QtGui
from furet import repository
from furet.app.utils import formatDate
from furet.app.windows import windowManager
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
            TableColumn[date | None]("publicationDate", lambda: "Date de publication", lambda v: "Non définie" if v is None else formatDate(v)), # 0
            TableColumn[date | None]("publicationDate", lambda: "Date d'expiration", lambda v: "Non définie" if v is None else formatDate(v + relativedelta(months=2))), # 1
            TableColumn[Department | None]("department", lambda: "Département", lambda v : "Non défini" if v is None else str(v)), # 2
            TableColumn[list[Campaign]]("campaigns", lambda: "Campagnes", lambda v: ", ".join(map(str, v))),                      # 3
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

        self._filters = DecreeFilterWidget(self.onClickResearchButton)
        self._topBar.addWidget(self._filters)

        self._table = QtWidgets.QTableView()
        self._table.setModel(self._decrees)
        self._layout.addWidget(self._table, 1)
        self._table.doubleClicked.connect(self.onDblClickTableRow)

        self._table.setEditTriggers(QtWidgets.QTableView.EditTrigger.NoEditTriggers)
        self._table.setSelectionMode(QtWidgets.QTableView.SelectionMode.SingleSelection)
        self._table.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)
        self._table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self._table.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self._table.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self._table.horizontalHeader().setSectionResizeMode(8, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self._table.setSortingEnabled(True)
        self._table.sortByColumn(1, QtCore.Qt.SortOrder.DescendingOrder)

    def closeEvent(self, event):
        super().closeEvent(event)
        QtWidgets.QApplication.quit()

    def onClickParamButton(self):
        windowManager.showWindow(SettingsWindow)

    def onClickResearchButton(self):
        self._decrees.resetData(repository.getDecrees(self._filters.filters()))


    def onDblClickTableRow(self, index: QtCore.QModelIndex):
        decree = self._decrees.itemAt(index.row())
        window, created = windowManager.showWindow(DecreeDetailsWindow, (decree,))
        if created:
            def onDecreeSaved():
                self._decrees.resetData(repository.getDecrees())
            window.accepted.connect(onDecreeSaved)

    def onClickImportButton(self):
        window, created = windowManager.showWindow(ImportFileWindow)
        if created:
            def onImportDone():
                self._decrees.resetData(repository.getDecrees())
            window.accepted.connect(onImportDone)
    def onClickDocButton(self):
        QtGui.QDesktopServices.openUrl("https://github.com/Hexoplanete/Projet-Furet/wiki")

    def updateTopicsComboBox(self):
        self._filters.updateTopicsComboBox()

    def updateCampaignsComboBox(self):
        self._filters.updateCampaignsComboBox()