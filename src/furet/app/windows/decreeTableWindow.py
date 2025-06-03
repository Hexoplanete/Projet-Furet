from typing import Any, Generic, TypeVar
from PySide6 import QtWidgets, QtCore, QtGui
from furet import repository
from furet.app.utils import formatDate
from furet.app.windows import windowManager
from furet.types.decree import *
from dateutil.relativedelta import relativedelta

from furet.app.widgets.objectTableModel import ObjectTableModel, FieldColumn, ComputedColumn
from furet.app.widgets.decreeFilterWidget import DecreeFilterWidget
from furet.app.windows.decreeDetailsWindow import DecreeDetailsWindow
from furet.app.windows.settingsWindow import SettingsWindow
from furet.app.windows.importFileWindow import ImportFileWindow
from furet.types.department import Department

T = TypeVar('T')
class DecreeFieldColumn(FieldColumn[Decree, T], Generic[T]):
    def data(self, item: Decree, /, role: QtCore.Qt.ItemDataRole):
        if role == QtCore.Qt.ItemDataRole.BackgroundRole:
            if item.isIncomplete():
                return QtGui.QColor(255,0,0,a=50)
        return super().data(item, role=role)


class DecreeBoolColumn(FieldColumn[Decree, bool]):
    def data(self, item: Decree, /, role: QtCore.Qt.ItemDataRole):
        if role == QtCore.Qt.ItemDataRole.BackgroundRole:
            if item.isIncomplete() or not getattr(item, self.name):
                return QtGui.QColor(255,0,0,a=50)
        return super().data(item, role=role)

class DecreeComputedBoolColumn(ComputedColumn[Decree, bool]):
    def data(self, item: Decree, /, role: QtCore.Qt.ItemDataRole) -> Any:
        if role == QtCore.Qt.ItemDataRole.BackgroundRole:
            if item.isIncomplete() or self.value(item):
                return QtGui.QColor(255,0,0,a=50)
        return super().data(item, role=role)


class DecreeTableWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self._content = QtWidgets.QWidget()
        self._layout = QtWidgets.QVBoxLayout(self._content)
        self.setCentralWidget(self._content)

        self._columns = [
            DecreeFieldColumn[date | None]("publicationDate", lambda: "Date de publication", lambda v: "Non définie" if v is None else formatDate(v)),
            DecreeFieldColumn[date | None]("publicationDate", lambda: "Date d'expiration", lambda v: "Non définie" if v is None else formatDate(v + relativedelta(months=2))),
            DecreeFieldColumn[Department | None]("department", lambda: "Département", lambda v : "Non défini" if v is None else str(v), lambda v: 0 if v is None else v.id),
            DecreeFieldColumn[list[Campaign]]("campaigns", lambda: "Campagnes", lambda v: ", ".join(map(str, v))),
            DecreeFieldColumn[list[Topic]]("topics", lambda: "Sujets", lambda v: ", ".join(map(str, v))),
            DecreeFieldColumn[str]("title", lambda: "Titre"),
            DecreeBoolColumn("treated", lambda: "État", lambda v: "Traité" if v else "À traiter"),
            DecreeComputedBoolColumn(lambda v: v.isIncomplete(), lambda: "À compléter", lambda v: "Oui" if v else "Non"), # TODO label not visible
            DecreeFieldColumn[str]("comment", lambda: "Commentaire"),
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