from PySide6 import QtWidgets

from furet.app.widgets.importListWidget import ImportListWidget


class ImportRaaWindow(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Import de Recueils")
        self._rootLayout = QtWidgets.QVBoxLayout(self)
        self._importsList = ImportListWidget()
        self._rootLayout.addWidget(self._importsList)
        self._rootLayout.addStretch()