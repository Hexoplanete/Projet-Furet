import enum
import os
from PySide6 import QtWidgets, QtCore

class PickMode(enum.Enum):
    File = enum.auto()
    Folder = enum.auto()
    Files = enum.auto()

class FilePickerWidget(QtWidgets.QWidget):
    def __init__(self, path: str = None, parent: QtWidgets.QWidget = None, /, pickMode: PickMode = PickMode.Files, onDataChange = None):
        super().__init__(parent)

        self._path = path if path is not None and os.path.exists(path) else QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.HomeLocation)
        self._pickMode = pickMode
        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setContentsMargins(0,0,0,0)
        self._fileEditText = QtWidgets.QLineEdit(text=self._path)
        self._fileEditText.textChanged.connect(onDataChange)
        self._layout.addWidget(self._fileEditText)
        self._parcourirButton = QtWidgets.QPushButton("Parcourir")
        self._parcourirButton.setFixedHeight(self._fileEditText.sizeHint().height())
        self._parcourirButton.clicked.connect(self.onClickParcourir)
        self._layout.addWidget(self._parcourirButton)

    def onClickParcourir(self):
        dialog = QtWidgets.QFileDialog()
        match self._pickMode:
            case PickMode.File:
                filePath = dialog.getOpenFileName(None, "Choisir un fichier", QtCore.QDir.homePath())[0]
                if filePath:
                        self._fileEditText.setText(filePath)
            case PickMode.Files:
                filePaths = dialog.getOpenFileNames(None, "Choisir un ou plusieurs fichiers", QtCore.QDir.homePath())
                if len(filePaths) > 0:
                    self._fileEditText.setText("; ".join(filePaths[0]))
            case PickMode.Folder:
                filePath = dialog.getExistingDirectory(None, "Choisir un dossier", self._path)
                if filePath:
                    self._fileEditText.setText(filePath)
    
    def setPath(self, path: str) -> str:
        self._fileEditText.setText(path)
    
    def getPath(self) -> str:
        return self._fileEditText.text()

    def getPaths(self) -> list[str]:
        return self._fileEditText.text().split("; ")
