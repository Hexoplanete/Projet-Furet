from PySide6 import QtWidgets
from furet.app.widgets.forms.aspasWidget import AspasInfoWidget
from furet.app.widgets.forms.decreeWidget import DecreeWidget
from furet.app.widgets.forms.raaWidget import RaaWidget

from furet import repository
from furet.app.widgets.textSeparatorWidget import TextSeparatorWidget


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

        self._layout.addWidget(TextSeparatorWidget("Arrêté"))
        self._decree = DecreeWidget(decree)
        self._layout.addWidget(self._decree)

        if not noRaa:
            self._layout.addWidget(TextSeparatorWidget("Recueil"))
            self._raa = RaaWidget(decree.raa)
            self._layout.addWidget(self._raa)

        self._layout.addWidget(TextSeparatorWidget("Informations supplémentaires"))
        self._aspas = AspasInfoWidget(decree.aspasInfo())
        self._layout.addWidget(self._aspas)

        self._buttons = QtWidgets.QDialogButtonBox(standardButtons=QtWidgets.QDialogButtonBox.StandardButton.Save | QtWidgets.QDialogButtonBox.StandardButton.Close)
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)
        self._layout.addWidget(self._buttons)

    def accept(self, /):
        if not self._noRaa:
            raa = self._raa.raa()
            repository.updateRaa(raa.id, raa)
        decree = self._decree.decree()
        decree.setAspasInfo(self._aspas.info())
        repository.updateDecree(decree.id, decree)
        super().accept()
