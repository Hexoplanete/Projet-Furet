from PySide6 import QtWidgets, QtCore
from furet.app.widgets.filePickerWidget import FilePickerWidget
from furet.app.utils import buildDatePicker, buildComboBox
from furet import repository
from datetime import date

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
        fileChoose = QtWidgets.QLabel("Indiquer l'URL du recueil (Ex: https//...) :")
        self._URLLayout.addWidget(fileChoose)
        self._URLRecueil = QtWidgets.QLineEdit()
        self._URLLayout.addWidget(self._URLRecueil)
        self._rootLayout.addLayout(self._URLLayout)

        self._departmentLayout = QtWidgets.QHBoxLayout()
        fileChoose = QtWidgets.QLabel("Indiquer le département :")
        self._departmentLayout.addWidget(fileChoose)
        self._departmentRecueil = buildComboBox(repository.getDepartments(), None, ("Choisir un département", None))
        self._departmentLayout.addWidget(self._departmentRecueil)
        self._rootLayout.addLayout(self._departmentLayout)

        self._dateLayout = QtWidgets.QHBoxLayout()
        fileChoose = QtWidgets.QLabel("Indiquer la date de publication :")
        self._dateLayout.addWidget(fileChoose)
        self._dateRecueil = buildDatePicker(date.today())
        self._dateLayout.addWidget(self._dateRecueil)
        self._rootLayout.addLayout(self._dateLayout)

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