from PySide6 import QtWidgets

from furet import repository
from furet.app.widgets.imports.finishedImportsWidget import FinishedImportsWidget
from furet.app.widgets.imports.inProgressImportsWidget import InProgressImportsWidget
from furet.app.widgets.imports.pendingImportsWidget import PendingImportsWidget
from furet.app.windows import windowManager
from furet.app.windows.raaDetailsWindow import RaaDetailsWindow
from furet.models.decree import Decree
from furet.models.raa import RAA


class RaaImportWindow(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Import de Recueils")
        self._layout = QtWidgets.QVBoxLayout(self)

        self._pending = PendingImportsWidget()
        self._pending.started.connect(self.startImport)
        self._layout.addWidget(self._pending)
        self._layout.addWidget(QtWidgets.QFrame(frameShape=QtWidgets.QFrame.Shape.HLine))
        self._inProgress = InProgressImportsWidget()
        self._inProgress.finished.connect(self.finishImport)
        self._layout.addWidget(self._inProgress)
        self._layout.addWidget(QtWidgets.QFrame(frameShape=QtWidgets.QFrame.Shape.HLine))
        self._finished = FinishedImportsWidget()
        self._finished.clicked.connect(self.openImport)
        self._layout.addWidget(self._finished)

        self._layout.addStretch()
        self._buttons = QtWidgets.QDialogButtonBox(standardButtons=QtWidgets.QDialogButtonBox.StandardButton.Close)
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)
        self._layout.addWidget(self._buttons)

    def startImport(self, path: str):
        self._pending.remove(path)
        self._inProgress.start(path)

    def finishImport(self, path, raa: RAA, decrees: list[Decree]):
        self._inProgress.remove(path)
        if raa.id == 0:
            repository.addRaa(raa)
            repository.addDecree(decrees)
        else:
            decrees = repository.getDecreesByRaa(raa.id)
        self._finished.add(path, raa, decrees)

    def openImport(self, path: str, raa: RAA, decrees: list[Decree]):
        window, _ = windowManager.showWindow(RaaDetailsWindow, raa, args=(raa, decrees))
        # TODO no visual updates on save + reuses old raa values
