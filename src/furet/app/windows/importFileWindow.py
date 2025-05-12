from PySide6 import QtWidgets, QtCore
from furet.app.widgets.filePickerWidget import FilePickerWidget

class ImportFileWindow(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Import Recueil")

        self._rootLayout = QtWidgets.QVBoxLayout(self)
        self._fileLayout = QtWidgets.QHBoxLayout()

        fileChoose = QtWidgets.QLabel("Choisir un fichier :")
        self._fileLayout.addWidget(fileChoose)
        self._filePicker = FilePickerWidget()
        self._fileLayout.addWidget(self._filePicker)
        self._rootLayout.addLayout(self._fileLayout)

        self._URLLayout = QtWidgets.QHBoxLayout()

        fileChoose = QtWidgets.QLabel("Indiquer l'URL du receuil :")
        self._URLLayout.addWidget(fileChoose)
        self._URLReceuil = QtWidgets.QLineEdit()
        self._URLLayout.addWidget(self._URLReceuil)
        self._rootLayout.addLayout(self._URLLayout)

        self._rootLayout.addSpacing(25)
        self._buttonLayout = QtWidgets.QHBoxLayout()
        self._cancelButton = QtWidgets.QPushButton("Annuler")
        self._cancelButton.clicked.connect(self.onClickAnnulerButton)
        self._buttonLayout.addWidget(self._cancelButton)
        self._saveConfirmerButton = QtWidgets.QPushButton("Confirmer")
        self._saveConfirmerButton.clicked.connect(self.onClickConfirmerButton)
        self._buttonLayout.addWidget(self._saveConfirmerButton)
        self._rootLayout.addLayout(self._buttonLayout)

    def onClickAnnulerButton(self):
        self.reject()

    def onClickConfirmerButton(self):
        self.accept()