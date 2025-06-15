import os
from threading import Thread
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Q_ARG
from furet.app.widgets.elidedLabel import ElidedPath
from furet.models.decree import Decree
from furet.models.raa import RAA
from furet.processing.processing import Processing


class InProgressImportWidget(QtWidgets.QWidget):

    finished = QtCore.Signal(RAA, list)

    def __init__(self, path: str, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._progress = QtWidgets.QProgressBar(value=0, minimum=0, maximum=0)
        self._progress.setFormat("%v/%m")
        self._layout.addWidget(self._progress, stretch=3)
        self._status = QtWidgets.QLabel("Initialisation...")
        self._layout.addWidget(self._status, stretch=1)

        self._results: tuple[RAA, list[Decree]]

        def processImport():
            processing = Processing()
            raa, decrees = processing.processingRAA(path, reportProgress=lambda v, m, s: QtCore.QMetaObject.invokeMethod(
                self, "updateStatus",  # type: ignore
                QtCore.Qt.ConnectionType.QueuedConnection,
                Q_ARG(int, v), Q_ARG(int, m), Q_ARG(str, s)))
            self._results = (raa, decrees)
            QtCore.QMetaObject.invokeMethod(self, "finish", QtCore.Qt.ConnectionType.QueuedConnection) # type: ignore

        self._thread = Thread(target=processImport, args=(), daemon=True)

    def start(self):
        self._thread.start()

    @QtCore.Slot()  # type: ignore
    def finish(self):
        self.finished.emit(*self._results)

    @QtCore.Slot(int, int, str)  # type: ignore
    def updateStatus(self, step: int, maximum: int, status: str):
        self._progress.setValue(step)
        self._progress.setMaximum(maximum)
        self._status.setText(status)


class InProgressImportsWidget(QtWidgets.QWidget):

    finished = QtCore.Signal(str, RAA, list)

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.setSpacing(0)

        self._paths: list[str] = []
        self._finished: dict[str, tuple[RAA, list[Decree]]] = {}

        self._startedLabel = QtWidgets.QLabel()
        self._layout.addWidget(self._startedLabel)

        self._importsLayout = QtWidgets.QVBoxLayout()
        self._importsLayout.setSpacing(0)
        self._layout.addLayout(self._importsLayout)
        self.updateStatus()

    def updateStatus(self):
        inProgress = len(self._paths)
        if inProgress == 0: self._startedLabel.setText("Aucun import de recueil en cour")
        else: self._startedLabel.setText(f"Import de {inProgress} recueil(s) en cour...")

    def start(self, path: str):
        path = os.path.realpath(path)
        if path in self._paths: return
        self._paths.append(path)
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        fileLink = ElidedPath(path)
        layout.addWidget(fileLink, stretch=1)
        
        progress = InProgressImportWidget(path)
        progress.finished.connect(lambda raa, decrees: self.finish(path, raa, decrees))
        layout.addWidget(progress, stretch=1)
        self._importsLayout.addWidget(widget)

        progress.start()
        self.updateStatus()

    def finish(self, path: str, raa: RAA, decrees: list[Decree]):
        path = os.path.realpath(path)
        if path not in self._paths: return
        
        self.finished.emit(path, raa, decrees)

    def remove(self, path: str):
        path = os.path.realpath(path)
        if path not in self._paths: return
        index = self._paths.index(path)
        self._paths.pop(index)
        self._importsLayout.takeAt(index).widget().hide()
        self.updateStatus()