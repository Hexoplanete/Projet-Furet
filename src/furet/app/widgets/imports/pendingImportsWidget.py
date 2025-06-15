import os
from PySide6 import QtCore, QtWidgets

from furet.app.widgets.elidedLabel import ElidedPath
from furet.app.widgets.fileDialog import FileDialog


class StartRemoveButtonsWidget(QtWidgets.QWidget):
    started = QtCore.Signal()
    removed = QtCore.Signal()

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._startButton = QtWidgets.QPushButton()
        self._startButton.setIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_MediaPlay))
        self._startButton.setContentsMargins(0, 0, 0, 0)
        self._startButton.clicked.connect(lambda: self.started.emit())
        self._layout.addWidget(self._startButton)
        self._removeButton = QtWidgets.QPushButton()
        self._removeButton.setIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_TrashIcon))
        self._removeButton.setContentsMargins(0, 0, 0, 0)
        self._removeButton.clicked.connect(lambda: self.removed.emit())
        self._layout.addWidget(self._removeButton)


class PendingImportsWidget(QtWidgets.QWidget):

    started = QtCore.Signal(str)

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.setSpacing(0)

        self._paths: list[str] = []

        self._statusLayout = QtWidgets.QHBoxLayout()
        self._statusLayout.setContentsMargins(0, 0, 0, 0)
        self._statusLayout.setSpacing(0)
        self._layout.addLayout(self._statusLayout)
        self._label = QtWidgets.QLabel()
        self._statusLayout.addWidget(self._label, stretch=1)
        self._addButton = QtWidgets.QPushButton("Parcourir")
        self._addButton.clicked.connect(self.browse)
        self._statusLayout.addWidget(self._addButton)
        self._controls = StartRemoveButtonsWidget()
        self._controls.started.connect(self.startAll)
        self._controls.removed.connect(self.removeAll)
        self._statusLayout.addWidget(self._controls)

        self._importsLayout = QtWidgets.QVBoxLayout()
        self._importsLayout.setSpacing(0)
        self._layout.addLayout(self._importsLayout)
        self.updateStatus()

    def browse(self):
        files, _ = FileDialog.getOpenFileNames(self, "Ajouter des recueils", "raa", QtCore.QDir.homePath(), "Documents (*.pdf)")
        [self.add(f) for f in files]

    def add(self, path: str):
        path = os.path.realpath(path)
        if path in self._paths:return
        self._paths.append(path)
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        fileLink = ElidedPath(path)
        layout.addWidget(fileLink, stretch=1)
        controls = StartRemoveButtonsWidget()
        controls.started.connect(lambda: self.start(path))
        controls.removed.connect(lambda: self.remove(path))
        layout.addWidget(controls)
        self._importsLayout.addWidget(widget)
        self.updateStatus()

    def remove(self, path: str):
        if not path in self._paths: return
        index = self._paths.index(path)
        self._paths.pop(index)
        self._importsLayout.takeAt(index).widget().hide()
        self.updateStatus()

    def removeAll(self):
        [self.remove(path) for path in self._paths.copy()]

    def start(self, path: str):
        self.started.emit(path)

    def startAll(self):
        [self.start(path) for path in self._paths.copy()]

    def updateStatus(self):
        count = len(self._paths)
        if count == 0: self._label.setText("Aucun recueil à importer")
        else: self._label.setText(f"{count} recueil(s) à importer")
        self._controls.setDisabled(count == 0)
