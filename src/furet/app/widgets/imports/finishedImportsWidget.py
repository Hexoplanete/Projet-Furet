import os
from PySide6 import QtCore, QtWidgets

from furet.app.widgets.elidedLabel import ElidedPath
from furet.models.decree import Decree
from furet.models.raa import RAA


class FinishedImportsWidget(QtWidgets.QWidget):

    clicked = QtCore.Signal(str, RAA, list)

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.setSpacing(0)

        self._paths: list[str] = []

        self._label = QtWidgets.QLabel()
        self._layout.addWidget(self._label)

        self._importsLayout = QtWidgets.QVBoxLayout()
        self._importsLayout.setSpacing(0)
        self._layout.addLayout(self._importsLayout)
        self.updateStatus()

    def add(self, path: str, raa: RAA, decrees:list[Decree]):
        path = os.path.abspath(path)
        if path in self._paths: return

        self._paths.append(path)
        # raa: RAA = repository.getRaaById(raaId)  # type: ignore
        # decrees = csvdb.deserialize(decreesStr, list[Decree])

        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        fileLink = ElidedPath(path)
        layout.addWidget(fileLink, stretch=1)
        button = QtWidgets.QPushButton()
        button.setText(f"{len(decrees)}/{raa.decreeCount} arrêté(s), {raa.missingValues() + sum(map(lambda d: d.missingValues(False), decrees))} champ(s) manquant(s)")
        button.clicked.connect(lambda: self.clicked.emit(path, raa, decrees))
        layout.addWidget(button, stretch=1)
        self._importsLayout.addWidget(widget)
        self.updateStatus()

    def updateStatus(self):
        count = len(self._paths)
        if count == 0: self._label.setText("Aucun recueil importé")
        else: self._label.setText(f"{count} recueil(s) importé(s)")