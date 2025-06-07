from furet.app.widgets.objectTableModel import ObjectTableColumn
from furet.app.widgets.objectTableWidget import ObjectTableWidget
from furet.app.widgets.optionalDateEdit import NONE_DATE
from PySide6 import QtWidgets, QtCore

from furet import repository
from furet.app.widgets.raaDetailsWidget import RaaDetailsWidget
from furet.app.widgets.textSeparatorWidget import TextSeparatorWidget
from furet.app.windows import windowManager
from furet.app.windows.decreeDetailsWindow import DecreeDetailsWindow
from furet.types.decree import Decree
from furet.types.raa import RAA


class RaaDetailsWindow(QtWidgets.QDialog):
    
    def __init__(self, raa: RAA, decrees: list[Decree]):
        super().__init__()
        
        self._raa = raa
        self._decrees = decrees
        self._layout = QtWidgets.QVBoxLayout(self)

        self._raaWidget = RaaDetailsWidget(raa)
        self._layout.addWidget(self._raaWidget)

        self._separator = TextSeparatorWidget("Arrêtés")
        self._layout.addWidget(self._separator)
        self._decreeLabel = TextSeparatorWidget(f"{len(decrees)} arrêté(s) pertinent(s) sur {raa.decreeCount}")
        self._layout.addWidget(self._separator)

        self._decreesTable = ObjectTableWidget(self._decrees, [
            ObjectTableColumn("Campagnes", lambda v: v.campaigns, lambda v: ", ".join(map(str, v))),
            ObjectTableColumn("Sujets", lambda v: v.topics, lambda v: ", ".join(map(str, v))),
            ObjectTableColumn("Titre", lambda v: v.title),
            ObjectTableColumn("À compléter", lambda v: v.missingValues(False), lambda v: f"{v} champs" if v else ""), # TODO label not visible
        ])
        self._decreesTable.doubleClicked.connect(self.onDblClickTableRow)
        self._layout.addWidget(self._decreesTable)
        self._buttons = QtWidgets.QDialogButtonBox(standardButtons=QtWidgets.QDialogButtonBox.StandardButton.Save | QtWidgets.QDialogButtonBox.StandardButton.Close)
        self._buttons.accepted.connect(self.save)
        self._buttons.rejected.connect(self.reject)
        self._layout.addWidget(self._buttons)

    def onDblClickTableRow(self, index: QtCore.QModelIndex):
        decree = self._decreesTable.itemAt(index.row())
        window, created = windowManager.showWindow(DecreeDetailsWindow, decree.id, args=(decree,), kwargs={ "noRaa":True}) # TODO handle RAA info edit / disable it
        window.accepted.connect(self.onDecreeSaved, type=QtCore.Qt.ConnectionType.UniqueConnection)

    def save(self):
        raa = self._raaWidget.raa()
        repository.updateRaa(raa.id, raa)

        # TODO find a way to remove this, currently, the decree does not know that tha raa was changed and fetching returns an old versions as the decrees file is not changed
        for d in self._decrees:
            repository.updateDecree(d.id, d)
        self.accept()
    
    def onDecreeSaved(self):
        self._decreesTable.setItems([repository.getDecreeById(d.id) for d in self._decrees])

