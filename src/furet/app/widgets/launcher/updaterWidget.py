import logging
from threading import Lock
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Q_ARG

logger = logging.getLogger("updater")

class UpdaterWidget(QtWidgets.QWidget):
    
    def __init__(self, parent: QtWidgets.QWidget | None = None): 
        super().__init__(parent)
        self._lock = Lock()
        self._lock.acquire()
        self._layout = QtWidgets.QVBoxLayout(self)
        self._doUpgrade: bool = False
        self._label = QtWidgets.QLabel()
        self._layout.addWidget(self._label)

        self._buttons = QtWidgets.QDialogButtonBox(standardButtons=QtWidgets.QDialogButtonBox.StandardButton.Yes | QtWidgets.QDialogButtonBox.StandardButton.No)
        self._buttons.accepted.connect(lambda: self.responded(True))
        self._buttons.rejected.connect(lambda: self.responded(False))
        self._layout.addWidget(self._buttons)
        self.hide()

    def updateModule(self):
        from furet import updater
        currentVersion = updater.currentVersion()
        if currentVersion == None:
            logger.info(f"Not on any tag")
            return

        logger.info(f"Currently on {currentVersion}")
        logger.debug(f"Checking for updates...")
        latestVersion = updater.latestVersion()
        if currentVersion == latestVersion:
            logger.info("Already on latest version")
            return
        logger.info(f"A new version ({latestVersion}) is available")

        QtCore.QMetaObject.invokeMethod(self, "getUpgradeChoice",  QtCore.Qt.ConnectionType.QueuedConnection, Q_ARG(str, currentVersion)) # type: ignore
        self._lock.acquire()

        if not self._doUpgrade:
            logger.info(f"Not upgrading")
            return
        
        logger.info(f"Upgrading to {latestVersion}...")
        updater.updateToVersion(latestVersion)
        logger.info(f"Now on {updater.currentVersion()}. Restart to apply changes")
        QtCore.QMetaObject.invokeMethod(self, "requestRestart",  QtCore.Qt.ConnectionType.QueuedConnection) # type: ignore
        self._lock.acquire()
    
    @QtCore.Slot(str) # type: ignore
    def getUpgradeChoice(self, version: str):
        self._label.setText(f"Une nouvelle version est disponible ({version}).\nVoulez vous l'installer ?")
        self.show()

    def responded(self, response:bool):
        self._doUpgrade = response
        self._label.setText("Installation de la mise à jour...")
        self._lock.release()

    @QtCore.Slot() # type: ignore
    def requestRestart(self):
        self._label.setText("Mise à jour installée avec succès.\nRelancez l'application pour l'appliquer.")
        self._buttons.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self._buttons.accepted.connect(lambda: QtCore.QCoreApplication.quit())
