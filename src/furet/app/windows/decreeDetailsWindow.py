from dateutil.relativedelta import relativedelta

from PySide6 import QtWidgets, QtCore

from furet.types.decree import Decree


class DecreeDetailsWindow(QtWidgets.QWidget):
    def __init__(self, decree: Decree):
        super().__init__()
        self._layout = QtWidgets.QVBoxLayout()

        # Top Layout
        self._topLayer = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(f"Détails Arrêté {decree.number}")
        self._topLayer.addWidget(label)
        label = QtWidgets.QLabel(f"Lien vers l'arrêté : <a href=\"{decree.link}\">Cliquez ici</a>")
        label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)
        label.setOpenExternalLinks(True)
        self._topLayer.addWidget(label)
        self._state = QtWidgets.QComboBox()
        self._state.addItems(["Statut : Non traité", "Statut : Traité"]) # TODO choix de base
        self._topLayer.addWidget(self._state)
        self._layout.addLayout(self._topLayer)

        # Title Layer
        label = QtWidgets.QLabel(f"Titre : {decree.title}") # TODO set titre
        self._layout.addWidget(label)
        
        # Date Layer
        self._dateLayer = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(f"Date de publication : {decree.publication_date}") # TODO set date publication
        self._dateLayer.addWidget(label)
        label = QtWidgets.QLabel(f"Date limite de recours : {decree.publication_date + relativedelta(months=2)}") # TODO set date limite max
        self._dateLayer.addWidget(label)
        self._layout.addLayout(self._dateLayer)
        

        self._infoLayer = QtWidgets.QHBoxLayout()
        decreeFrame = QtWidgets.QGroupBox("Arrêté")
        # arrete = QtWidgets.QVBoxLayout(decreeFrame)
        # widget = QtWidgets.QWidget()
        widgetLayout = QtWidgets.QVBoxLayout(decreeFrame)
        # widget.setStyleSheet('background-color: LightGray;')
        label = QtWidgets.QLabel(f"Type de document : {decree.doc_type}")
        widgetLayout.addWidget(label)
        label = QtWidgets.QLabel(f"Campagne ASPAS : {decree.campaign}")
        widgetLayout.addWidget(label)
        label = QtWidgets.QLabel(f"Sujet : {decree.topic.label}")
        widgetLayout.addWidget(label)
        label = QtWidgets.QLabel(f"Date Signature : {decree.signing_date}")
        widgetLayout.addWidget(label)
        label = QtWidgets.QLabel(f"Pagination de l'arrêté : p.{decree.start_page}->{decree.end_page}")
        widgetLayout.addWidget(label)
        self._infoLayer.addWidget(decreeFrame)
        self._layout.addLayout(self._infoLayer)
        
        self._commentLayer = QtWidgets.QVBoxLayout()
        self._layout.addLayout(self._commentLayer)
        
        self._buttonsLayer = QtWidgets.QHBoxLayout()
        self._layout.addLayout(self._buttonsLayer)

        self.setWindowTitle("Paramètres")
        self.label = QtWidgets.QLabel("Détails")
        self._layout.addWidget(self.label)
        self.setLayout(self._layout)