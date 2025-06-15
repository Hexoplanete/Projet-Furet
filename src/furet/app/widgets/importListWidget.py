from dataclasses import dataclass
import os
from threading import Thread
import time
from PySide6 import QtCore, QtWidgets

from furet import repository
from furet.app.widgets.elidedLabel import ElidedPath
from furet.app.windows import windowManager
from furet.app.windows.raaDetailsWindow import RaaDetailsWindow
from furet.processing.processing import Processing
from PySide6.QtCore import Q_ARG

from furet.repository import csvdb
from furet.models.decree import Decree
from furet.models.raa import RAA

@dataclass
class InProgressImport:
    thread: Thread
    progress: QtWidgets.QProgressBar
    status: QtWidgets.QLabel

class StartClearButtonsWidget(QtWidgets.QWidget):
    started = QtCore.Signal()
    cleared = QtCore.Signal()

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setContentsMargins(0,0,0,0)
        self._layout.setSpacing(0)
        self._startButton = QtWidgets.QPushButton()
        self._startButton.setIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_MediaPlay))
        self._startButton.setContentsMargins(0, 0, 0, 0)
        self._startButton.clicked.connect(lambda: self.started.emit())
        self._layout.addWidget(self._startButton)
        self._clearButton = QtWidgets.QPushButton()
        self._clearButton.setIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_TrashIcon))
        self._clearButton.setContentsMargins(0, 0, 0, 0)
        self._clearButton.clicked.connect(lambda: self.cleared.emit())
        self._layout.addWidget(self._clearButton)

class ImportListWidget(QtWidgets.QWidget):
    
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.setContentsMargins(0,0,0,0)

        self._buildPendingSection()
        self._separator = QtWidgets.QFrame(frameShape=QtWidgets.QFrame.Shape.HLine)
        self._layout.addWidget(self._separator)
        self._buildStartedSection()
        self._separator2 = QtWidgets.QFrame(frameShape=QtWidgets.QFrame.Shape.HLine)
        self._layout.addWidget(self._separator2)
        self._buildFinishedSection()


    def _buildPendingSection(self):
        self._pendingImports: list[str] = []

        def onPendingAddClicked():
            files, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Ajouter des recueils", QtCore.QDir.homePath(), "Documents (*.pdf)")
            for f in files:
                self.addImport(f)
        
        def onPendingStartClicked():
            paths = self._pendingImports.copy()
            for path in paths:
                self.startImport(path)
        
        def onPendingClearClicked():
            paths = self._pendingImports.copy()
            for path in paths:
                self.clearImport(path)

        self._pendingStatusLayout = QtWidgets.QHBoxLayout()
        self._pendingStatusLayout.setContentsMargins(0,0,0,0)
        self._pendingStatusLayout.setSpacing(0)
        self._layout.addLayout(self._pendingStatusLayout)
        self._pendingLabel = QtWidgets.QLabel()
        self._pendingStatusLayout.addWidget(self._pendingLabel, stretch=1)
        self._pendingAddButton = QtWidgets.QPushButton("Parcourir")
        self._pendingAddButton.clicked.connect(onPendingAddClicked)
        self._pendingStatusLayout.addWidget(self._pendingAddButton)
        self._pendingControls = StartClearButtonsWidget()
        self._pendingControls.started.connect(onPendingStartClicked)
        self._pendingControls.cleared.connect(onPendingClearClicked)
        self._pendingStatusLayout.addWidget(self._pendingControls)

        self._pendingImportsLayout = QtWidgets.QVBoxLayout()
        self._pendingImportsLayout.setSpacing(0)
        self._layout.addLayout(self._pendingImportsLayout)

        self.updatePendingStatus()

    def _buildStartedSection(self):
        self._inProgressImports: list[str] = []
        self._inProgressStates: list[InProgressImport] = []

        self._processing = Processing()

        self._startedLabel = QtWidgets.QLabel()
        self._layout.addWidget(self._startedLabel)

        self._inProgressImportsLayout = QtWidgets.QVBoxLayout()
        self._inProgressImportsLayout.setSpacing(0)
        self._layout.addLayout(self._inProgressImportsLayout)

        self.updateInProgressStatus()
        
    def _buildFinishedSection(self):
        self._finishedImports: list[str] = []

        self._finishedLabel = QtWidgets.QLabel()
        self._layout.addWidget(self._finishedLabel)

        self._finishedImportsLayout = QtWidgets.QVBoxLayout()
        self._finishedImportsLayout.setSpacing(0)
        self._layout.addLayout(self._finishedImportsLayout)

        self.updateFinishedStatus()
    
    def updatePendingStatus(self):
        pendingCount = len(self._pendingImports)
        if pendingCount == 0:
            self._pendingLabel.setText("Aucun recueil à importer")
        else:
            self._pendingLabel.setText(f"{pendingCount} recueil(s) à importer")

        self._pendingControls.setDisabled(pendingCount == 0)

    def updateInProgressStatus(self):
        inProgress = len(self._inProgressImports)
        if inProgress == 0:
            self._startedLabel.setText("Aucun import de recueil en cour")
        else:
            self._startedLabel.setText(f"Import de {inProgress} recueil(s) en cour...")

    @QtCore.Slot(str, int, int, str)
    def updateInProgressImportStatus(self, path: str, step: int, maximum: int, status: str):
        path = os.path.realpath(path)
        if not path in self._inProgressImports: return
        index = self._inProgressImports.index(path)
        state = self._inProgressStates[index]
        state.progress.setValue(step)
        state.progress.setMaximum(maximum)
        state.status.setText(status)

    def updateFinishedStatus(self):
        finished = len(self._finishedImports)
        if finished == 0:
            self._finishedLabel.setText("Aucun recueil importé")
        else:
            self._finishedLabel.setText(f"{finished} recueil(s) importé(s)")

    def addImport(self, path: str):
        path = os.path.realpath(path)
        if path in self._pendingImports or path in self._inProgressImports or path in self._finishedImports: return
        self._pendingImports.append(path)
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(0,0,0,0)
        fileLink = ElidedPath(path)
        layout.addWidget(fileLink, stretch=1)
        pending = StartClearButtonsWidget()
        pending.started.connect(lambda: self.startImport(path))
        pending.cleared.connect(lambda: self.clearImport(path))
        layout.addWidget(pending)
        self._pendingImportsLayout.addWidget(widget)
        self.updatePendingStatus()

    def clearImport(self, path: str):
        index = self._pendingImports.index(path)
        if index == -1: return
        self._pendingImports.pop(index)
        self._pendingImportsLayout.takeAt(index).widget().hide()
        self.updatePendingStatus()

    def startImport(self, path: str):
        path = os.path.realpath(path)
        self.clearImport(path)
        if path in self._inProgressImports: return
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        fileLink = ElidedPath(path)
        layout.addWidget(fileLink, stretch=3)
        progress = QtWidgets.QProgressBar(value=0, minimum=0, maximum=0)
        progress.setFormat("%v/%m")
        layout.addWidget(progress, stretch=3)
        status = QtWidgets.QLabel("Initialisation...")
        layout.addWidget(status, stretch=1)
        self._inProgressImportsLayout.addWidget(widget)

        def processImport(path: str):
            raa, decrees = self._processing.processingRAA(path,reportProgress=lambda v, m, s: QtCore.QMetaObject.invokeMethod(
                self, "updateInProgressImportStatus",  # type: ignore
                QtCore.Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, path), Q_ARG(int, v), Q_ARG(int, m), Q_ARG(str, s)))
            if raa.id == 0:
                repository.addRaa(raa)
                repository.addDecree(decrees)
            else:
                decrees = repository.getDecreesByRaa(raa.id)
            time.sleep(1)
            QtCore.QMetaObject.invokeMethod(
                self, "finishImport",  # type: ignore
                QtCore.Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, path), Q_ARG(int, raa.id), Q_ARG(str, csvdb.serialize(decrees)))

        thread = Thread(target=processImport, args=(path,), daemon=True)
        self._inProgressImports.append(path)
        self._inProgressStates.append(InProgressImport(thread, progress, status))
        thread.start()
        self.updateInProgressStatus()

    @QtCore.Slot(str, int, str)
    def finishImport(self, path: str, raaId: int, decreesStr: str):
        path = os.path.realpath(path)
        if path not in self._inProgressImports: return
        index = self._inProgressImports.index(path)
        self._inProgressImports.pop(index)
        self._inProgressStates.pop(index)
        self._inProgressImportsLayout.takeAt(index).widget().hide()
        self.updateInProgressStatus()

        if path in self._finishedImports: return

        raa: RAA = repository.getRaaById(raaId)  # type: ignore

        def onOpenButtonClicked():
            window, _ = windowManager.showWindow(RaaDetailsWindow, raa.id, args=(raa.id, decrees))
            # TODO no visual updates on save + reuses old raa values
   

        decrees = csvdb.deserialize(decreesStr, list[Decree])
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        fileLink = ElidedPath(path)
        layout.addWidget(fileLink, stretch=1)
        button = QtWidgets.QPushButton()
        button.setText(f"{len(decrees)}/{raa.decreeCount} arrêté(s), {raa.missingValues() + sum(map(lambda d: d.missingValues(False), decrees))} champ(s) manquant(s)")
        button.clicked.connect(onOpenButtonClicked)
        layout.addWidget(button, stretch=1)
        self._finishedImportsLayout.addWidget(widget)
        self._finishedImports.append(path)
        self.updateFinishedStatus()
