from threading import Lock
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Q_ARG

class UpdaterWidget(QtWidgets.QWidget):
    
    def __init__(self, parent: QtWidgets.QWidget | None = None): 
        super().__init__(parent)
        self._lock = Lock()
        self._layout = QtWidgets.QVBoxLayout(self)
        self._response: bool = False
        self._label = QtWidgets.QLabel()
        self._layout.addWidget(self._label)

        self._buttons = QtWidgets.QDialogButtonBox(standardButtons=QtWidgets.QDialogButtonBox.StandardButton.Yes | QtWidgets.QDialogButtonBox.StandardButton.No)
        self._buttons.accepted.connect(lambda: self.responded(True))
        self._buttons.rejected.connect(lambda: self.responded(False))
        self._layout.addWidget(self._buttons)
        self.hide()

    def getUpgradeChoice(self, version: str) -> bool:
        self._lock.acquire()
        QtCore.QMetaObject.invokeMethod(self, "_getUpgradeChoice",  QtCore.Qt.ConnectionType.QueuedConnection, Q_ARG(str, version)) # type: ignore
        
        self._lock.acquire()
        return self._response
    
    @QtCore.Slot(str) # type: ignore
    def _getUpgradeChoice(self, version: str):
        self._label.setText(f"Une nouvelle version est disponible ({version})\nVoulez vous l'installer ?")
        self.show()

    def responded(self, response:bool):
        self._response = response
        self._lock.release()