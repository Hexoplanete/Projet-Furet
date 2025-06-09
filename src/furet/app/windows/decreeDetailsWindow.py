from PySide6 import QtWidgets
from furet.app.widgets.models.aspasInfoEdit import AspasInfoEdit
from furet.app.widgets.models.decreeEdit import DecreeEdit
from furet.app.widgets.models.raaEdit import RaaEdit

from furet import repository
from furet.app.widgets.sectionHeaderWidget import SectionHeaderWidget


class DecreeDetailsWindow(QtWidgets.QDialog):

    def __init__(self, decreeId: int, noRaa: bool = False):
        super().__init__()
        self._decreeId = decreeId
        self._noRaa = noRaa

        decree = repository.getDecreeById(decreeId)
        if decree is None:
            raise Exception(f"Decree {decreeId} does not exist")

        self.setWindowTitle(f"Détails de l'arrêté n°{decree.number}")
        self._layout = QtWidgets.QVBoxLayout(self)

        self._layout.addWidget(SectionHeaderWidget("Arrêté"))
        self._decree = DecreeEdit(decree)
        self._layout.addWidget(self._decree)

        if not noRaa:
            self._layout.addWidget(SectionHeaderWidget("Recueil"))
            self._raa = RaaEdit(decree.raa)
            self._layout.addWidget(self._raa)

        self._layout.addWidget(SectionHeaderWidget("Informations supplémentaires"))
        self._aspas = AspasInfoEdit(decree.aspasInfo())
        self._layout.addWidget(self._aspas)

        self._buttons = QtWidgets.QDialogButtonBox(standardButtons=QtWidgets.QDialogButtonBox.StandardButton.Save | QtWidgets.QDialogButtonBox.StandardButton.Close)
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)
        self._layout.addWidget(self._buttons)

    def accept(self, /):
        if not self._noRaa:
            raa = self._raa.value()
            repository.updateRaa(raa.id, raa)
        decree = self._decree.value()
        decree.setAspasInfo(self._aspas.value())
        repository.updateDecree(decree.id, decree)
        super().accept()
