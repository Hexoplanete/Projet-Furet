from furet.app.utils import DECREE_COLUMNS
from furet.app.widgets.objectTableWidget import ObjectTableWidget
from PySide6 import QtWidgets, QtCore

from furet import repository
from furet.app.widgets.models.raaEdit import RaaEdit
from furet.app.widgets.sectionHeaderWidget import SectionHeaderWidget
from furet.app.windows import windowManager
from furet.app.windows.decreeDetailsWindow import DecreeDetailsWindow
from furet.models.decree import Decree
from furet.models.raa import RAA


class RaaDetailsWindow(QtWidgets.QDialog):
    
    def __init__(self, raa: RAA, decrees: list[Decree]):
        super().__init__()
        
        self._raa = raa
        self._decrees = decrees
        self._layout = QtWidgets.QVBoxLayout(self)

        self._layout.addWidget(SectionHeaderWidget("Recueil"))
        self._raaWidget = RaaEdit(raa)
        self._layout.addWidget(self._raaWidget)

        self._layout.addWidget(SectionHeaderWidget("Arrêtés"))
        self._decreesTable = ObjectTableWidget(self._decrees, DECREE_COLUMNS[3:7])
        self._decreesTable.doubleClicked.connect(lambda i: self.showDecreeDetailsWindow(self._decreesTable.itemAt(i.row())))
        self._layout.addWidget(self._decreesTable)

        self._buttons = QtWidgets.QDialogButtonBox(standardButtons=QtWidgets.QDialogButtonBox.StandardButton.Save | QtWidgets.QDialogButtonBox.StandardButton.Close)
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)
        self._layout.addWidget(self._buttons)

    def showDecreeDetailsWindow(self, decree: Decree):
        window, created = windowManager.showWindow(DecreeDetailsWindow, decree.id, args=(decree.id,), kwargs={ "noRaa":True })
        window.accepted.connect(self.updateDecrees, type=QtCore.Qt.ConnectionType.UniqueConnection)

    def accept(self, /) -> None:
        raa = self._raaWidget.value()
        repository.updateRaa(raa.id, raa)

        # TODO find a way to remove this, currently, the decree does not know that tha raa was changed and fetching returns an old versions as the decrees file is not changed
        for d in self._decrees:
            repository.updateDecree(d.id, d)
        super().accept()

    def updateDecrees(self):
        self._decreesTable.setItems([repository.getDecreeById(d.id) for d in self._decrees])

