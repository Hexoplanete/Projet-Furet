from PySide6 import QtWidgets, QtCore, QtGui
from furet import repository
from furet.app.utils import DECREE_COLUMNS
from furet.app.widgets.objectTableWidget import ObjectTableWidget
from furet.app.windows import windowManager
from furet.app.windows.raaImportWindow import RaaImportWindow
from furet.models.decree import Decree

from furet.app.widgets.decreeFilterWidget import DecreeFilterWidget
from furet.app.windows.decreeDetailsWindow import DecreeDetailsWindow
from furet.app.windows.settingsWindow import SettingsWindow

class DecreeTableWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self._toolbar = self.addToolBar("a toolbar")
        self._toolbar.setMovable(False)
        self._importAction = self._toolbar.addAction("Importer un recueil")
        self._importAction.triggered.connect(self.showImportWindow)
        self._importAction = self._toolbar.addAction("Campagnes et Sujets")
        self._importAction.triggered.connect(self.showImportWindow)
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        self._toolbar.addWidget(spacer)
        self._docAction = self._toolbar.addAction("Documentation")
        self._docAction.triggered.connect(self.openDocumentation)
        self._settingsAction = self._toolbar.addAction("Paramètres")
        self._settingsAction.triggered.connect(self.showSettingsWindow)

        self._content = QtWidgets.QWidget()
        self._layout = QtWidgets.QVBoxLayout(self._content)
        self.setCentralWidget(self._content)


        self._filters = DecreeFilterWidget(self.updateDecrees)
        self._layout.addWidget(self._filters)

        self._decreeTable = ObjectTableWidget(repository.getDecrees(self._filters.filters()), DECREE_COLUMNS, sortingEnabled=True)
        self._decreeTable.doubleClicked.connect(lambda i: self.showDecreeDetailsWindow(self._decreeTable.itemAt(i.row())))
        self._layout.addWidget(self._decreeTable, 1)

    def closeEvent(self, event):
        QtWidgets.QApplication.quit()

    def showSettingsWindow(self):
        window, _ = windowManager.showWindow(SettingsWindow)
        window.accepted.connect(self.updateDecrees, type=QtCore.Qt.ConnectionType.UniqueConnection)

    def showDecreeDetailsWindow(self, decree: Decree):
        window, _ = windowManager.showWindow(DecreeDetailsWindow, decree.id, args=(decree.id,))
        window.accepted.connect(self.updateTopicsAndCampaigns, type=QtCore.Qt.ConnectionType.UniqueConnection)

    def showImportWindow(self):
        window, _ = windowManager.showWindow(RaaImportWindow)
        window.finished.connect(self.updateDecrees, type=QtCore.Qt.ConnectionType.UniqueConnection)

    def openDocumentation(self):
        QtGui.QDesktopServices.openUrl("https://github.com/Hexoplanete/Projet-Furet/wiki")

    def updateDecrees(self):
        self._decreeTable.setItems(repository.getDecrees(self._filters.filters()))

    def updateTopicsAndCampaigns(self):
        self._filters.updateCampaignsComboBox()
        self._filters.updateTopicsComboBox()
