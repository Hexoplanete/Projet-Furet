from PySide6 import QtWidgets, QtCore, QtGui
from furet import repository
from furet.app.utils import DECREE_COLUMNS
from furet.app.widgets.objectTableWidget import ObjectTableWidget
from furet.app.windows import windowManager
from furet.app.windows.ImportRaaWindow import ImportRaaWindow
from furet.types.decree import Decree

from furet.app.widgets.decreeFilterWidget import DecreeFilterWidget
from furet.app.windows.decreeDetailsWindow import DecreeDetailsWindow
from furet.app.windows.settingsWindow import SettingsWindow

class DecreeTableWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._content = QtWidgets.QWidget()
        self._layout = QtWidgets.QVBoxLayout(self._content)
        self.setCentralWidget(self._content)
    
        self._buttonLayer = QtWidgets.QHBoxLayout()
        self._buttonLayer.setContentsMargins(0,0,0,0)
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
        self._layout.addLayout(self._buttonLayer)

        self._filters = DecreeFilterWidget(self.updateDecrees)
        self._layout.addWidget(self._filters)

        self._decreeTable = ObjectTableWidget(repository.getDecrees(self._filters.filters()), DECREE_COLUMNS, sortingEnabled=True)
        self._decreeTable.doubleClicked.connect(lambda i: self.showDecreeDetailsWindow(self._decreeTable.itemAt(i.row())))
        self._layout.addWidget(self._decreeTable, 1)

    def closeEvent(self, event):
        QtWidgets.QApplication.quit()

    def showSettingsWindow(self):
        windowManager.showWindow(SettingsWindow, args=(self,))

    def showDecreeDetailsWindow(self, decree: Decree):
        window, created = windowManager.showWindow(DecreeDetailsWindow, decree.id, args=(decree.id,))
        window.accepted.connect(self.updateDecrees, type=QtCore.Qt.ConnectionType.UniqueConnection)

    def showImportWindow(self):
        window, created = windowManager.showWindow(ImportRaaWindow)
        window.finished.connect(self.updateDecrees, type=QtCore.Qt.ConnectionType.UniqueConnection)

    def openDocumentation(self):
        QtGui.QDesktopServices.openUrl("https://github.com/Hexoplanete/Projet-Furet/wiki")

    def updateDecrees(self):
        self._decreeTable.setItems(repository.getDecrees(self._filters.filters()))

    def updateTopicsComboBox(self):
        self._filters.updateTopicsComboBox()

    def updateCampaignsComboBox(self):
        self._filters.updateCampaignsComboBox()