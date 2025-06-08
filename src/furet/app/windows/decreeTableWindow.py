from typing import Generic, TypeVar
from PySide6 import QtWidgets, QtCore, QtGui
from furet import repository
from furet.app.utils import formatDate
from furet.app.widgets.objectTableWidget import ObjectTableWidget
from furet.app.widgets.optionalDateEdit import NONE_DATE
from furet.app.windows import windowManager
from furet.app.windows.ImportRaaWindow import ImportRaaWindow
from furet.types.decree import *

from furet.app.widgets.objectTableModel import ObjectTableColumn
from furet.app.widgets.decreeFilterWidget import DecreeFilterWidget
from furet.app.windows.decreeDetailsWindow import DecreeDetailsWindow
from furet.app.windows.settingsWindow import SettingsWindow
from furet.types.department import Department

T = TypeVar('T')
class DecreeColumn(Generic[T], ObjectTableColumn[Decree, T]):
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

        self._topBar = QtWidgets.QVBoxLayout()
        self._topBar.setContentsMargins(0,0,0,0)
        self._buttonLayer = QtWidgets.QHBoxLayout()
        self._buttonLayer.setContentsMargins(0,0,0,0)
        self._layout.addLayout(self._topBar)
        
        self._fileButton = QtWidgets.QPushButton('Importer un recueil')
        self._fileButton.clicked.connect(self.showImportWindow)
        self._buttonLayer.addWidget(self._fileButton)

        self._buttonLayer.addStretch()

        self._docButton = QtWidgets.QPushButton('Documentation')
        self._docButton.clicked.connect(self.openDocumentation)
        self._buttonLayer.addWidget(self._docButton)           
        
        self._paramButton = QtWidgets.QPushButton('Paramètres')
        self._paramButton.clicked.connect(self.showSettingsWindow)
        self._buttonLayer.addWidget(self._paramButton)
        
        self._topBar.addLayout(self._buttonLayer)

        self._filters = DecreeFilterWidget(self.updateDecrees)
        self._topBar.addWidget(self._filters)

        self._decreeTable = ObjectTableWidget(repository.getDecrees(), [
            DecreeColumn[date|None]("Date de publication", lambda v: v.raa.publicationDate, lambda v: "Non définie" if v is None else formatDate(v), lambda v: v or NONE_DATE),
            DecreeColumn[date|None]("Date d'expiration", lambda v: v.raa.expireDate(), lambda v: "Non définie" if v is None else formatDate(v), lambda v: v or NONE_DATE),
            DecreeColumn[Department|None]("Département", lambda v: v.raa.department, lambda v: "Non défini" if v is None else str(v), lambda v: 0 if v is None else v.id),
            DecreeColumn[list[Campaign]]("Campagnes", lambda v: v.campaigns, lambda v: ", ".join(map(str, v)), lambda v: list(map(lambda i: i.label, v))),
            DecreeColumn[list[Topic]]("Sujets", lambda v: v.topics, lambda v: ", ".join(map(str, v)), lambda v: list(map(lambda i: i.label, v))),
            DecreeColumn[str]("Titre", lambda v: v.title, resizeMode=QtWidgets.QHeaderView.ResizeMode.Stretch),
            DecreeStateColumn("État", lambda v: v.treated, lambda v: "Traité" if v else "À traiter"),
            DecreeColumn[int]("À compléter", lambda v: v.missingValues(), lambda v: f"{v} champs" if v else ""),  # TODO label not visible
            DecreeColumn[str]("Commentaire", lambda v: v.comment, resizeMode=QtWidgets.QHeaderView.ResizeMode.ResizeToContents),
        ], sortingEnabled=True)
        self._decreeTable.doubleClicked.connect(lambda i: self.showDecreeDetailsWindow(self._decreeTable.itemAt(i.row())))
        self._layout.addWidget(self._decreeTable, 1)

    def closeEvent(self, event):
        QtWidgets.QApplication.quit()

    def showSettingsWindow(self):
        windowManager.showWindow(SettingsWindow, args=(self,))

    def showDecreeDetailsWindow(self, decree: Decree):
        window, created = windowManager.showWindow(DecreeDetailsWindow, decree.id, args=(decree,))
        window.accepted.connect(self.updateDecrees, type=QtCore.Qt.ConnectionType.UniqueConnection)

    def showImportWindow(self):
        window, created = windowManager.showWindow(ImportRaaWindow)
        window.accepted.connect(self.updateDecrees, type=QtCore.Qt.ConnectionType.UniqueConnection)

    def openDocumentation(self):
        QtGui.QDesktopServices.openUrl("https://github.com/Hexoplanete/Projet-Furet/wiki")

    def updateDecrees(self):
        self._decreeTable.setItems(repository.getDecrees(self._filters.filters()))

    def updateTopicsComboBox(self):
        self._filters.updateTopicsComboBox()

    def updateCampaignsComboBox(self):
        self._filters.updateCampaignsComboBox()