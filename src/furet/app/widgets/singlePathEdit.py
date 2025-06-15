import os
from typing import Any
from PySide6 import QtWidgets, QtCore

from furet.app.widgets.elidedLabel import ElidedPath
from furet.app.widgets.fileDialog import FileDialog

class SinglePathEdit(QtWidgets.QWidget):

    pathChanged = QtCore.Signal(str)

    def __init__(self, path: str | None = None, /, parent: QtWidgets.QWidget | None = None, id: str | Any | None = None, folder: bool = False):
        super().__init__(parent)
        self._id = id
        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setContentsMargins(0,0,0,0)

        self._folder = folder
        self._uri = ElidedPath(path or "", elideMode=QtCore.Qt.TextElideMode.ElideMiddle)
        self._layout.addWidget(self._uri, stretch=1)

        self._selectButton = QtWidgets.QPushButton("Parcourir")
        # self._browseButton.setFixedHeight(self._fileEditText.sizeHint().height())
        self._selectButton.clicked.connect(self.queryPath)
        self._layout.addWidget(self._selectButton)

    def queryPath(self):
        if self._folder:
            filePath = FileDialog.getExistingDirectory(self, dir=os.path.dirname(self._uri.path()), id=self._id)
            if filePath:
                self.setPath(filePath)
        else:
            filePath = FileDialog.getOpenFileName(self, dir=os.path.dirname(self._uri.path()), id=self._id)[0]
            if filePath:
                    self.setPath(filePath)

    def setPath(self, path: str):
        self._uri.setPath(path)
        self.pathChanged.emit(path)
    
    def path(self) -> str:
        return self._uri.path()
