from PySide6 import QtWidgets

from furet.app.widgets.importListWidget import ImportListWidget


class RaaImportWindow(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Import de Recueils")
        self._layout = QtWidgets.QVBoxLayout(self)
        self._importsList = ImportListWidget()
        self._layout.addWidget(self._importsList)
        self._layout.addStretch()

        self._buttons = QtWidgets.QDialogButtonBox(standardButtons=QtWidgets.QDialogButtonBox.StandardButton.Close)
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)
        self._layout.addWidget(self._buttons)
