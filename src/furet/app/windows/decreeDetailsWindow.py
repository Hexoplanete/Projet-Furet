from typing import Any
from dateutil.relativedelta import relativedelta

from PySide6 import QtWidgets, QtCore, QtGui

from furet import repository
from furet.app.utils import addFormRow, buildComboBox, buildDatePicker, buildMultiComboBox
from furet.app.widgets.textSeparatorWidget import TextSeparatorWidget
from furet.app.widgets.elidedLabel import ElidedLabel
from furet.types.decree import Decree


class DecreeDetailsWindow(QtWidgets.QDialog):
    
    def __init__(self, decree: Decree):
        super().__init__()
        self._decree = decree
        self.setWindowTitle(f"Détails de l'arrêté n°{decree.number}")

        self._rootLayout = QtWidgets.QVBoxLayout(self)

        def addSection(label: str):
            if self._rootLayout.count() > 0:
                self._rootLayout.addSpacing(20)
            sep = TextSeparatorWidget(label)
            sep = self._rootLayout.addWidget(sep)
            decreeForm = QtWidgets.QFormLayout()
            self._rootLayout.addLayout(decreeForm)
            return decreeForm

        # Decree
        decreeForm = addSection("Arrêté")

        self._decreeTitle = QtWidgets.QLineEdit(decree.title)
        addFormRow(decreeForm, "Titre", self._decreeTitle)

        self._decreeNumber = QtWidgets.QLineEdit(decree.number)
        addFormRow(decreeForm, "N° de l'arrêté", self._decreeNumber)

        self._docType = QtWidgets.QComboBox()
        self._docType = buildComboBox(repository.getDocumentTypes(), decree.docType)
        addFormRow(decreeForm, "Type de document", self._docType)


        self._signingDate = buildDatePicker(decree.signingDate)
        addFormRow(decreeForm, "Date de signature", self._signingDate)
        
        self._expireDate = buildDatePicker(decree.publicationDate + relativedelta(months=2))
        self._expireDate.setDisabled(True)
        addFormRow(decreeForm, "Date d'expiration", self._expireDate)

        # RAA
        decreeForm = addSection("Recueil")
        self._department = buildComboBox(
            repository.getDepartments(), decree.department)
        self._department.setDisabled(True)
        addFormRow(decreeForm, "Département", self._department)

        self._publicationDate = buildDatePicker(decree.publicationDate)
        self._publicationDate.setDisabled(True)
        addFormRow(decreeForm, "Date de publication", self._publicationDate)
        
        label = ElidedLabel(decree.link)
        label.setMinimumWidth(0)
        label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)
        label.setOpenExternalLinks(True)
        addFormRow(decreeForm, "Lien", label)

        self._raaNumber = QtWidgets.QLineEdit(decree.raaNumber)
        addFormRow(decreeForm, "Numéro RAA", self._raaNumber)

        pagesRange = QtWidgets.QWidget()
        pagesLayout = QtWidgets.QHBoxLayout(pagesRange)
        self._pagesStart = QtWidgets.QLineEdit(str(decree.startPage))
        self._pagesStart.setValidator(QtGui.QIntValidator())
        pagesSep = QtWidgets.QLabel("à")
        self._pagesEnd = QtWidgets.QLineEdit(str(decree.endPage))
        self._pagesEnd.setValidator(QtGui.QIntValidator())
        pagesLayout.addWidget(self._pagesStart)
        pagesLayout.addWidget(pagesSep)
        pagesLayout.addWidget(self._pagesEnd)
        addFormRow(decreeForm, "Pages", pagesRange)
        pagesLayout.setContentsMargins(0, 0, 0, 0)

        # ASPAS specific
        decreeForm = addSection("Informations supplémentaires")

        self._campaign = buildComboBox(
            repository.getCampaigns(), decree.campaign)
        addFormRow(decreeForm, "Campagne", self._campaign)

        topicWidget = QtWidgets.QWidget()
        topicLayout = QtWidgets.QHBoxLayout(topicWidget)
        topicLayout.setContentsMargins(0,0,0,0)
        self._topic = buildMultiComboBox(repository.getTopics(), decree.topic)
        self._topic.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        topicLayout.addWidget(self._topic)

        self._unselectTopic = QtWidgets.QPushButton('X')
        self._unselectTopic.setFixedSize(20,20)
        self._unselectTopic.setContentsMargins(0,0,0,0)
        self._unselectTopic.setToolTip("Bouton qui désélectionne tous les sujets de la liste.")
        self._unselectTopic.clicked.connect(self.onClickUnselectTopic)
        topicLayout.addWidget(self._unselectTopic, alignment=QtCore.Qt.AlignLeft)
        addFormRow(decreeForm, "Sujet", topicWidget)

        self._treated = QtWidgets.QCheckBox("", )
        self._treated.setChecked(decree.treated)
        addFormRow(decreeForm, "Traité", self._treated)

        commentSep = QtWidgets.QLabel("Commentaire")
        self._rootLayout.addWidget(commentSep)
        self._comment = QtWidgets.QTextEdit(self._decree.comment)
        self._rootLayout.addWidget(self._comment)

        # Buttons
        self._buttonLayout = QtWidgets.QHBoxLayout()
        self._returnButton = QtWidgets.QPushButton("Retour")
        self._returnButton.clicked.connect(self.onClickRetourButton)
        self._buttonLayout.addWidget(self._returnButton)
        self._saveAndQuitButton = QtWidgets.QPushButton("Sauvegarder et Quitter")
        self._saveAndQuitButton.clicked.connect(self.onClickSaveQuitButton)
        self._buttonLayout.addWidget(self._saveAndQuitButton)
        self._rootLayout.addLayout(self._buttonLayout)

    def saveDecree(self):
        self._decree = Decree(
            id=self._decree.id,
            number=self._decreeNumber.text(),
            title=self._decreeTitle.text(),
            docType=self._docType.currentData(),
            publicationDate=self._publicationDate.date().toPython(),
            signingDate=self._signingDate.date().toPython(),
            department=self._department.currentData(),
            raaNumber=self._raaNumber.text(),
            link=self._decree.link,
            startPage=int(self._pagesStart.text()),
            endPage=int(self._pagesEnd.text()),
            campaign=self._campaign.currentData(),
            topic=self._topic.currentData(),
            treated=self._treated.isChecked(),
            comment=self._comment.toPlainText(),
        )

    def onClickRetourButton(self):
        self.reject()

    def onClickSaveQuitButton(self):
        self.saveDecree()
        self.accept()

    def decree(self):
        return self._decree

    def onClickUnselectTopic(self):
        self._topic.unselectAllItems()
