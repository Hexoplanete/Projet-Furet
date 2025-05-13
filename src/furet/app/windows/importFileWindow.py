from PySide6 import QtWidgets, QtCore

import os
from datetime import date
from furet.app.utils import buildComboBox, buildDatePicker
from furet.app.widgets.filePickerWidget import FilePickerWidget
from furet import repository
from furet.traitement.processing import Traitement
from furet.types.raa import RAA

class ImportFileWindow(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Import Recueil")

        self._rootLayout = QtWidgets.QVBoxLayout(self)
        decreeForm = QtWidgets.QFormLayout()
        
        self._filePicker = FilePickerWidget(onDataChange=self.onValueChange)
        decreeForm.addRow("Choisir un fichier :", self._filePicker)

        self._URLRecueil = QtWidgets.QLineEdit()
        self._URLRecueil.textChanged.connect(self.onValueChange)
        decreeForm.addRow("Indiquer l'URL du recueil (Ex: https//...) :", self._URLRecueil)

        self._department = buildComboBox(repository.getDepartments(), None, ("Choisir un département", None))
        self._department.editTextChanged.connect(self.onValueChange)
        decreeForm.addRow("Indiquer le département :", self._department)
        
        self._pubDate = buildDatePicker(date.today())
        self._pubDate.dateChanged.connect(self.onValueChange)
        decreeForm.addRow("Indiquer la date de publication :", self._pubDate)

        self._rootLayout.addLayout(decreeForm)

        self._rootLayout.addSpacing(25)
        self._buttonLayout = QtWidgets.QHBoxLayout()
        self._cancelButton = QtWidgets.QPushButton("Annuler")
        self._cancelButton.clicked.connect(self.onClickAnnulerButton)
        self._buttonLayout.addWidget(self._cancelButton)
        self._saveConfirmerButton = QtWidgets.QPushButton("Confirmer")
        self._saveConfirmerButton.setEnabled(False)
        self._saveConfirmerButton.clicked.connect(self.onClickConfirmerButton)
        self._buttonLayout.addWidget(self._saveConfirmerButton)
        self._rootLayout.addLayout(self._buttonLayout)

    def onClickAnnulerButton(self):
        self.reject()

    def onClickConfirmerButton(self):
        traitement = Traitement()
        traitement.traitementRAA(self._filePicker.getPath(), RAA(department=self._department.currentData(),
                                                                 number="ND",
                                                                 link=self._URLRecueil.text(),
                                                                 publicationDate=self._pubDate.date().toPython()))
        self.accept()

    def onValueChange(self):
        self._saveConfirmerButton.setEnabled(False)
        if not(os.path.isfile(self._filePicker.getPath())): return
        if not(self._URLRecueil.text()): return
        if not(self._department.currentIndex()): return
        if not(self._pubDate.date()): return
        self._saveConfirmerButton.setEnabled(True)