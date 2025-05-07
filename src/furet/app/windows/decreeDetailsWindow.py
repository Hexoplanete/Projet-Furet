from dateutil.relativedelta import relativedelta

from PySide6 import QtWidgets, QtCore

from furet import repository
from furet.types.decree import Decree


class DecreeDetailsWindow(QtWidgets.QWidget):
    def __init__(self, decree: Decree):
        super().__init__()
        self.setWindowTitle(f"Détails de l'arrêté n°{decree.number}")
        
        self._rootLayout = QtWidgets.QVBoxLayout(self)
        self._decreeForm = QtWidgets.QFormLayout()
        self._rootLayout.addLayout(self._decreeForm)
        # self._layout = QtWidgets.QVBoxLayout()

        # Decree
        decreeTitle = QtWidgets.QLineEdit(decree.title)
        self._decreeForm.addRow("Titre", decreeTitle)

        decreeNumber = QtWidgets.QLineEdit(decree.raaNumber)
        self._decreeForm.addRow("N° de l'arrêté", decreeNumber)

        docType = QtWidgets.QComboBox()
        docTypes = repository.getDocumentTypes()
        for t in docTypes: docType.addItem(t.label, t.id)
        self._decreeForm.addRow("Type de document", docType)
        for i, t in enumerate(docTypes):
            if t.id == decree.doc_type.id:
                docType.setCurrentIndex(i)


        # RAA
        label = QtWidgets.QLabel(f"<a href=\"{decree.link}\">Cliquez ici</a>")
        label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)
        label.setOpenExternalLinks(True)
        self._decreeForm.addRow("Lien vers l'arrêté", label)

        raaNumber = QtWidgets.QLineEdit(decree.raaNumber)
        self._decreeForm.addRow("Numéro RAA", raaNumber)

        docType = QtWidgets.QComboBox()
        docTypes = repository.getDocumentTypes()
        for t in docTypes: docType.addItem(t.label, t.id)
        self._decreeForm.addRow("Type de document", docType)
        for i, t in enumerate(docTypes):
            if t.id == decree.doc_type.id:
                docType.setCurrentIndex(i)

        self._state = QtWidgets.QComboBox()
        self._state.addItems(["Non traité", "Traité"])
        self._decreeForm.addRow("Statut", self._state)

        pubDate = QtWidgets.QLabel(f"{decree.publicationDate}")
        self._decreeForm.addRow("Date de publication", pubDate)

        dateLimit = QtWidgets.QLabel(f"{decree.publicationDate + relativedelta(months=2)}")
        self._decreeForm.addRow("Date limite de recours", dateLimit)

        docType = QtWidgets.QLabel(f"{decree.doc_type}")
        self._decreeForm.addRow("Type de document", docType)

        campaignLabel = QtWidgets.QLabel(str(decree.campaign))
        self._decreeForm.addRow("Campagne ASPAS", campaignLabel)

        topicLabel = QtWidgets.QLabel(str(decree.topic.label))
        self._decreeForm.addRow("Sujet", topicLabel)

        signingDate = QtWidgets.QLabel(str(decree.signingDate))
        self._decreeForm.addRow("Date Signature", signingDate)

        pageRange = QtWidgets.QLabel(f"p.{decree.startPage}->{decree.endPage}")
        self._decreeForm.addRow("Pagination de l'arrêté", pageRange)

        departementLabel = QtWidgets.QLabel(f"{decree.department.label} ({decree.department.id})")
        self._decreeForm.addRow("Département", departementLabel)

        self._comment = QtWidgets.QTextEdit()
        self._decreeForm.addRow("Commentaire", self._comment)


        # # Top Layout
        # self._topLayer = QtWidgets.QHBoxLayout()
        # label = QtWidgets.QLabel(f"Lien vers l'arrêté : <a href=\"{decree.link}\">Cliquez ici</a>")
        # label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)
        # label.setOpenExternalLinks(True)
        # self._topLayer.addWidget(label)
        # self._state = QtWidgets.QComboBox()
        # self._state.addItems(["Statut : Non traité", "Statut : Traité"]) # TODO choix de base
        # self._topLayer.addWidget(self._state)
        # self._decreeForm.addLayout(self._topLayer)

        # # Title Layer
        # label = QtWidgets.QLabel(f"Titre : {decree.title}") # TODO set titre
        # self._decreeForm.addWidget(label)
        
        # # Date Layer
        # self._dateLayer = QtWidgets.QHBoxLayout()
        # label = QtWidgets.QLabel(f"Date de publication : {decree.publication_date}") # TODO set date publication
        # self._dateLayer.addWidget(label)
        # label = QtWidgets.QLabel(f"Date limite de recours : {decree.publication_date + relativedelta(months=2)}") # TODO set date limite max
        # self._dateLayer.addWidget(label)
        # self._decreeForm.addLayout(self._dateLayer)
        

        # self._infoLayer = QtWidgets.QHBoxLayout()
        # decreeFrame = QtWidgets.QGroupBox("Arrêté")
        # # arrete = QtWidgets.QVBoxLayout(decreeFrame)
        # # widget = QtWidgets.QWidget()
        # widgetLayout = QtWidgets.QVBoxLayout(decreeFrame)
        # # widget.setStyleSheet('background-color: LightGray;')
        # form = QtWidgets.QFormLayout()
        # label = QtWidgets.QLabel(decree.doc_type)
        # form.addRow("Type de document", label)
        # label = QtWidgets.QLabel(decree.campaign)
        # form.addRow("Campagne ASPAS", label)
        # label = QtWidgets.QLabel(decree.topic.label)
        # form.addRow("Sujet", label)
        # label = QtWidgets.QLabel(decree.signing_date)
        # form.addRow("Date Signature", label)
        # label = QtWidgets.QLabel(f"p.{decree.start_page}->{decree.end_page}")
        # form.addRow("Pagination de l'arrêté", label)
        # widgetLayout.addLayout(form)
        # self._infoLayer.addWidget(decreeFrame)
        # self._decreeForm.addLayout(self._infoLayer)
        
        # self._commentLayer = QtWidgets.QVBoxLayout()
        # self._decreeForm.addLayout(self._commentLayer)
        
        # self._buttonsLayer = QtWidgets.QHBoxLayout()
        # self._decreeForm.addLayout(self._buttonsLayer)

        # self.label = QtWidgets.QLabel("Détails")
        # self._decreeForm.addWidget(self.label)
        # self.setLayout(self._decreeForm)