from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QMetaObject

import os
from datetime import date
from furet.app.utils import addFormRow, buildComboBox, buildDatePicker
from furet.app.widgets.filePickerWidget import FilePickerWidget
from furet import repository
from furet.types.raa import RAA
import threading

class ImportFileWindow(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Import Recueil")

        self._rootLayout = QtWidgets.QVBoxLayout(self)

        self._formWidget = QtWidgets.QWidget()
        decreeForm = QtWidgets.QFormLayout(self._formWidget)
        
        self._filePicker = FilePickerWidget(onDataChange=self.onValueChange)
        addFormRow(decreeForm, "Choisir un fichier", self._filePicker)

        # self._URLRecueil = QtWidgets.QLineEdit()
        # self._URLRecueil.textChanged.connect(self.onValueChange)
        # addFormRow(decreeForm, "Indiquer l'URL du recueil (Ex: https//...)", self._URLRecueil)

        # self._department = buildComboBox(repository.getDepartments(), None, ("Choisir un département", None))
        # self._department.editTextChanged.connect(self.onValueChange)
        # addFormRow(decreeForm, "Indiquer le département", self._department)
        
        # self._pubDate = buildDatePicker(date.today())
        # self._pubDate.dateChanged.connect(self.onValueChange)
        # addFormRow(decreeForm, "Indiquer la date de publication", self._pubDate)

        self._rootLayout.addWidget(self._formWidget, stretch=1)

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

        self._threads = []
        self._progressBar = QtWidgets.QProgressBar(self)
        self._progressBar.setFixedWidth(500)  # Increase the width of the progress bar
        self._progressBar.setStyleSheet("""
            QProgressBar {
            border: 2px solid #4CAF50;
            border-radius: 5px;
            text-align: center;
            background: #E0E0E0;
            }
            QProgressBar::chunk {
            background-color: #4CAF50;
            width: 20px;
            margin: 1px;
            }
        """)  # Add styling for a more polished look
        self._progressBar.hide()

    @QtCore.Slot()
    def finalProcess(self):
        self.accept()
    

    def onClickAnnulerButton(self):
        self.reject()

    def onClickConfirmerButton(self):

        from furet.processing.processing import Processing

        paramPdfStorageDirectory_path = os.path.join(os.getcwd(), "database", "pdfDirectory") # A recupérer dans le frontend ? Donc pas ici mais dans "importFileWindow.py"
        paramOutputProcessingSteps_path = os.path.join(os.getcwd(), "database", "debug", "processingSteps") # A recupérer dans le frontend ? Donc pas ici mais dans "importFileWindow.py"

        os.makedirs(paramPdfStorageDirectory_path, exist_ok=True) # Si on récupère ça du front alors logiquement, le dossier doit déjà existé 
        os.makedirs(paramOutputProcessingSteps_path, exist_ok=True) # Si on récupère ça du front alors logiquement, le dossier doit déjà existé 

        traitement = Processing(pdfDirectory_path=paramPdfStorageDirectory_path, outputProcessingSteps_path=paramOutputProcessingSteps_path)
        listeFichiers = self._filePicker.getPaths()
        self._progressBar.show()
        self._progressBar.setRange(0, len(listeFichiers))
        self._progressBar.setFormat("%v/%m")  # Display as fraction (current/total)
        self._progressBar.setValue(0)
        self._rootLayout.insertWidget(0, self._progressBar)
        self._rootLayout.removeWidget(self._formWidget)
        self._cancelButton.hide()
        self._saveConfirmerButton.hide()
        self._formWidget.hide()

        def runRAAProcessing(fichier):
            traitement.processingRAA(fichier)
            self._progressBar.setValue(self._progressBar.value() + 1)

            if self._progressBar.value() == len(self._threads):
                # Remove the progress bar after completion
                self._rootLayout.removeWidget(self._progressBar)
                QMetaObject.invokeMethod(self, "finalProcess", QtCore.Qt.QueuedConnection)


        for fichier in listeFichiers:
            thread = threading.Thread(target=runRAAProcessing, args=(fichier,))
            self._threads.append(thread)
            thread.start()

    def onValueChange(self):
        self._saveConfirmerButton.setEnabled(False)
        for fichier in self._filePicker.getPaths():
            if not(os.path.isfile(fichier)): return
        # if not(os.path.isfile(self._filePicker.getPath())): return
        # if not(self._URLRecueil.text()): return
        # if not(self._department.currentIndex()): return
        # if not(self._pubDate.date()): return
        self._saveConfirmerButton.setEnabled(True)