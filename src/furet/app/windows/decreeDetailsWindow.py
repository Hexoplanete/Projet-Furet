from typing import Any, Callable
from dateutil.relativedelta import relativedelta
from furet.app.widgets.optionalDateEdit import NONE_DATE
from PySide6 import QtWidgets, QtCore, QtGui

from furet import repository
from furet.app.utils import addFormRow, buildComboBox, buildDatePicker, buildMultiComboBox, addFormSection
from furet.app.widgets.raaDetailsWidget import RaaDetailsWidget
from furet.types.decree import Decree
from furet.types.raa import RAA


class DecreeDetailsWindow(QtWidgets.QDialog):
    
    def __init__(self, decree: Decree, noRaa: bool = False):
        super().__init__()
        self._noRaa = noRaa
        self._decree = decree
        self.setWindowTitle(f"Détails de l'arrêté n°{decree.number}")
        self.setStyleSheet('*[missingValue="true"] { background-color: rgba(255, 0, 0, 0.2) }')
        self._rootLayout = QtWidgets.QVBoxLayout(self)

        # Decree
        decreeForm = addFormSection(self._rootLayout, "Arrêté")
        self._decreeTitle = QtWidgets.QLineEdit(decree.title)
        addFormRow(decreeForm, "Titre", self._decreeTitle)
        self.installMissingBackground(self._decreeTitle, "text", lambda v: len(v) == 0)

        self._decreeNumber = QtWidgets.QLineEdit(decree.number)
        addFormRow(decreeForm, "N° de l'arrêté", self._decreeNumber)
        self.installMissingBackground(self._decreeNumber, "text", lambda v: len(v) == 0)

        self._docType = buildComboBox(repository.getDocumentTypes(), decree.docType, ("Non défini", None))
        addFormRow(decreeForm, "Type de document", self._docType)
        self.installMissingBackground(self._docType, "currentIndex", lambda v: v == 0)

        self._signingDate = buildDatePicker(decree.signingDate)
        addFormRow(decreeForm, "Date de signature", self._signingDate)
        self.installMissingBackground(self._signingDate, "date", lambda v: v is None or v == NONE_DATE)
        
        self._expireDate = buildDatePicker(None if decree.raa.publicationDate is None else decree.raa.publicationDate + relativedelta(months=2))
        self._expireDate.setReadOnly(True)
        self._signingDate.dateChanged.connect(lambda v: self._expireDate.setDate(None if v == NONE_DATE or v is None else v.toPython() + relativedelta(months=2)))  # type: ignore
        addFormRow(decreeForm, "Date d'expiration", self._expireDate)

        pagesRange = QtWidgets.QWidget()
        pagesLayout = QtWidgets.QHBoxLayout(pagesRange)
        self._pagesStart = QtWidgets.QSpinBox(minimum=1, maximum=9999, value=decree.startPage)
        pagesSep = QtWidgets.QLabel("à")
        self._pagesEnd = QtWidgets.QSpinBox(minimum=1, maximum=9999, value=decree.endPage)
        pagesLayout.addWidget(self._pagesStart)
        pagesLayout.addWidget(pagesSep)
        pagesLayout.addWidget(self._pagesEnd)
        pagesLayout.addStretch(1)
        addFormRow(decreeForm, "Pages", pagesRange)
        pagesLayout.setContentsMargins(0, 0, 0, 0)

        # RAA
        if not noRaa:
            decreeForm = addFormSection(self._rootLayout, "Recueil")
            self._raa = RaaDetailsWidget(self._decree.raa)
            self._rootLayout.addWidget(self._raa)


        # ASPAS specific
        decreeForm = addFormSection(self._rootLayout, "Informations supplémentaires")

        self._campaign = buildMultiComboBox(repository.getCampaigns(), decree.campaigns)
        addFormRow(decreeForm, "Campagne", self._campaign)

        topicWidget = QtWidgets.QWidget()
        topicLayout = QtWidgets.QHBoxLayout(topicWidget)
        topicLayout.setContentsMargins(0,0,0,0)
        topicLayout.setSpacing(0)

        self._topic = buildMultiComboBox(repository.getTopics(), decree.topics)
        self._topic.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        topicLayout.addWidget(self._topic)

        self._unselectTopic = QtWidgets.QPushButton()
        self._unselectTopic.setIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_TrashIcon))
        self._unselectTopic.setContentsMargins(0, 0, 0, 0)
        self._unselectTopic.setToolTip("Bouton qui désélectionne tous les sujets de la liste.")
        self._unselectTopic.clicked.connect(self.onClickUnselectTopic)
        topicLayout.addWidget(self._unselectTopic, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        addFormRow(decreeForm, "Sujet", topicWidget)

        self._treated = QtWidgets.QCheckBox("", )
        self._treated.setChecked(decree.treated)
        addFormRow(decreeForm, "Traité", self._treated)
        

        commentSep = QtWidgets.QLabel("Commentaire")
        self._rootLayout.addWidget(commentSep)
        self._comment = QtWidgets.QTextEdit(plainText=self._decree.comment)
        self._rootLayout.addWidget(self._comment)

        # Buttons
        self._buttonLayout = QtWidgets.QHBoxLayout()
        self._returnButton = QtWidgets.QPushButton("Retour")
        self._returnButton.setDefault(True)
        self._returnButton.setAutoDefault(True)
        self._returnButton.clicked.connect(self.onClickRetourButton)
        self._buttonLayout.addWidget(self._returnButton)
        self._saveAndQuitButton = QtWidgets.QPushButton("Sauvegarder et Quitter")
        self._saveAndQuitButton.clicked.connect(self.onClickSaveQuitButton)
        self._buttonLayout.addWidget(self._saveAndQuitButton)
        self._rootLayout.addLayout(self._buttonLayout)
        
    def installMissingBackground(self, widget: QtWidgets.QWidget, fieldName: str, isMissing: Callable[[Any], bool]):
        signal: QtCore.SignalInstance = getattr(widget, f"{fieldName}Changed")
        def updateProp(value: Any):
            widget.setProperty("missingValue", isMissing(value))
            self.style().unpolish(widget)
            self.style().polish(widget)
        signal.connect(updateProp)
        field = getattr(widget, fieldName)
        updateProp(field())

    def saveDecree(self):
        if not self._noRaa:
            raa = self._raa.raa()
            repository.updateRaa(self._decree.raa.id, raa)
        signingDate = self._signingDate.date()
        decree = Decree(
            id=self._decree.id,

            raa=self._decree.raa,
            startPage=self._pagesStart.value(),
            endPage=self._pagesEnd.value(),

            docType=self._docType.currentData(),
            number=self._decreeNumber.text(),
            title=self._decreeTitle.text(),           
            signingDate=None if signingDate is None else signingDate.toPython(),  # type: ignore

            treated=self._treated.isChecked(),
            campaigns=self._campaign.currentData(),
            topics=self._topic.currentData(),
            comment=self._comment.toPlainText(),
        )
        repository.updateDecree(self._decree.id, decree)

    def onClickRetourButton(self):
        self.reject()

    def onClickSaveQuitButton(self):
        self.saveDecree()
        self.accept()

    def onClickUnselectTopic(self):
        self._topic.unselectAllItems()
