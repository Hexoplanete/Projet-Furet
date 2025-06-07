from typing import Generic, TypeVar
from PySide6 import QtWidgets, QtCore, QtGui
from furet import repository
from furet.app.utils import formatDate
from furet.app.widgets.optionalDateEdit import NONE_DATE
from furet.app.windows import windowManager
from furet.app.windows.ImportRaaWindow import ImportRaaWindow
from furet.types.decree import *
from dateutil.relativedelta import relativedelta

from furet.app.widgets.objectTableModel import ObjectTableModel, ObjectTableColumn
from furet.app.widgets.decreeFilterWidget import DecreeFilterWidget
from furet.app.windows.decreeDetailsWindow import DecreeDetailsWindow
from furet.app.windows.settingsWindow import SettingsWindow

T = TypeVar('T')
class DecreeColumn(ObjectTableColumn[Decree, T], Generic[T]):
    def data(self, item: Decree, /, role: QtCore.Qt.ItemDataRole):
        if role == QtCore.Qt.ItemDataRole.BackgroundRole:
            if item.missingValues():
                return QtGui.QColor(255,0,0,a=50)
        return super().data(item, role=role)


class DecreeStateColumn(DecreeColumn[bool]):
    def data(self, item: Decree, /, role: QtCore.Qt.ItemDataRole):
        if role == QtCore.Qt.ItemDataRole.BackgroundRole:
            if item.missingValues() or not self.value(item):
                return QtGui.QColor(255,0,0,a=50)
        return super().data(item, role=role)

class DecreeTableWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self._content = QtWidgets.QWidget()
        self._layout = QtWidgets.QVBoxLayout(self._content)
        self.setCentralWidget(self._content)

        self._columns = [
            DecreeColumn("Date de publication", lambda v: v.raa.publicationDate, lambda v: "Non définie" if v is None else formatDate(v), lambda v: v or NONE_DATE),
            DecreeColumn("Date d'expiration", lambda v: v.raa.publicationDate, lambda v: "Non définie" if v is None else formatDate(v + relativedelta(months=2)), lambda v: v or NONE_DATE),
            DecreeColumn("Département", lambda v: v.raa.department, lambda v : "Non défini" if v is None else str(v), lambda v: 0 if v is None else v.id),
            DecreeColumn("Campagnes", lambda v: v.campaigns, lambda v: ", ".join(map(str, v))),
            DecreeColumn("Sujets", lambda v: v.topics, lambda v: ", ".join(map(str, v))),
            DecreeColumn("Titre", lambda v: v.title),
            DecreeStateColumn("État", lambda v: v.treated, lambda v: "Traité" if v else "À traiter"),
            DecreeColumn("À compléter", lambda v: v.missingValues(), lambda v: f"{v} champs" if v else ""), # TODO label not visible
            DecreeColumn("Commentaire", lambda v: v.comment),
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
        QtWidgets.QApplication.quit()

    def onClickParamButton(self):
        windowManager.showWindow(SettingsWindow)

    def onClickResearchButton(self):
        self._decrees.setItems(repository.getDecrees(self._filters.filters()))

    def onDecreeSaved(self):
        print("isuet")
        self._decrees.setItems(repository.getDecrees())

    def onDblClickTableRow(self, index: QtCore.QModelIndex):
        decree = self._decrees.itemAt(index.row())
        window, created = windowManager.showWindow(DecreeDetailsWindow, decree.id, args=(decree,))
        window.accepted.connect(self.onDecreeSaved, type=QtCore.Qt.ConnectionType.UniqueConnection)

    def onImportDone(self):
        self._decrees.setItems(repository.getDecrees())
    
    def onClickImportButton(self):
        window, created = windowManager.showWindow(ImportRaaWindow)
        window.accepted.connect(self.onImportDone, type=QtCore.Qt.ConnectionType.UniqueConnection)

    def onClickDocButton(self):
        QtGui.QDesktopServices.openUrl("https://github.com/Hexoplanete/Projet-Furet/wiki")

    def updateTopicsComboBox(self):
        self._filters.updateTopicsComboBox()

    def updateCampaignsComboBox(self):
        self._filters.updateCampaignsComboBox()