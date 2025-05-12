from PySide6 import QtWidgets, QtCore

class FilePickerWidget(QtWidgets.QWidget):
    def __init__(self, parent : QtWidgets.QWidget = None):
        super().__init__(parent)

        self._layout = QtWidgets.QHBoxLayout(self)
        self._fileEditText = QtWidgets.QLineEdit()
        self._layout.addWidget(self._fileEditText)
        self._parcourirButton = QtWidgets.QPushButton("Parcourir")
        self._parcourirButton.clicked.connect(self.onClickParcourir)
        self._layout.addWidget(self._parcourirButton)

    def onClickParcourir(self):
        dialog = QtWidgets.QFileDialog()
        filePath = dialog.getOpenFileName(None, "Choisir un fichier à importer", QtCore.QDir.homePath())[0]
        if filePath:
            self._fileEditText.setText(filePath)
