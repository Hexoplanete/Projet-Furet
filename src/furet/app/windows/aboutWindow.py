from importlib.metadata import version, metadata
from PySide6 import QtCore, QtWidgets, QtGui
from furet.app.widgets.elidedLabel import ElidedUri
from furet.app.widgets.iconWidget import IconWidget
from furet.app.widgets.sectionHeaderWidget import SectionHeaderWidget

class AboutWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("À propos")

        self._layout = QtWidgets.QVBoxLayout(self)

        self._titleLayout = QtWidgets.QGridLayout()
        self._titleLayout.setColumnStretch(0,1)
        self._titleLayout.setColumnStretch(3,1)
        self._layout.addLayout(self._titleLayout)
        icon = QtGui.QIcon("assets/furet-logo.ico")
        self._icon = IconWidget(icon)
        
        self._titleLayout.addWidget(self._icon, 0,1, -1, 1)
        self._title = QtWidgets.QLabel(f"<h3>FURET - {version('furet')}</h3>")
        self._titleLayout.addWidget(self._title, 0,2)
        self._description = QtWidgets.QLabel(metadata("furet").get("summary"))
        self._description.setWordWrap(True)
        self._titleLayout.addWidget(self._description, 1,2)

        self._layout.addWidget(QtWidgets.QFrame(frameShape=QtWidgets.QFrame.Shape.HLine))

        self._layout.addWidget(SectionHeaderWidget("Copyright"))
        self._copyrightLayout = QtWidgets.QFormLayout(fieldGrowthPolicy=QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self._layout.addLayout(self._copyrightLayout)
        self._copyrightLayout.addRow("Dépôt :", ElidedUri("https://github.com/Hexoplanete/Projet-Furet"))
        self._copyrightLayout.addRow("Licence :", ElidedUri("https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt", text="CC0-1.0"))
        
        self._layout.addWidget(SectionHeaderWidget("Auteurs"))
        self._authorsLabel = QtWidgets.QLabel("Crée l'équipe <a href=\"https://github.com/Hexoplanete\">Hexoplanète</a> de l'INSA de Lyon : ")
        self._authorsLabel.setWordWrap(True)
        self._authorsLabel.setOpenExternalLinks(True)
        self._layout.addWidget(self._authorsLabel)
        self._authorsLayout = QtWidgets.QGridLayout()
        self._authorsLayout.setContentsMargins(0,0,0,0)
        self._authorsLayout.setSpacing(0)
        self._authorsLayout.addWidget(QtWidgets.QLabel("Justine STEPHAN", alignment=QtCore.Qt.AlignmentFlag.AlignCenter), 0, 0)
        self._authorsLayout.addWidget(QtWidgets.QLabel("Marine QUEMENER", alignment=QtCore.Qt.AlignmentFlag.AlignCenter), 1, 0)
        self._authorsLayout.addWidget(QtWidgets.QLabel("Corentin JEANNE", alignment=QtCore.Qt.AlignmentFlag.AlignCenter), 2, 0)
        self._authorsLayout.addWidget(QtWidgets.QLabel("Juliette PIERRE", alignment=QtCore.Qt.AlignmentFlag.AlignCenter), 3, 0)
        self._authorsLayout.addWidget(QtWidgets.QLabel("Joris FELZINES", alignment=QtCore.Qt.AlignmentFlag.AlignCenter), 0, 1)
        self._authorsLayout.addWidget(QtWidgets.QLabel("Harold MARTIN", alignment=QtCore.Qt.AlignmentFlag.AlignCenter), 1, 1)
        self._authorsLayout.addWidget(QtWidgets.QLabel("Thomas LEVRARD", alignment=QtCore.Qt.AlignmentFlag.AlignCenter), 2, 1)
        self._authorsLayout.addWidget(QtWidgets.QLabel("Amadou SOW", alignment=QtCore.Qt.AlignmentFlag.AlignCenter), 3, 1)
        self._layout.addLayout(self._authorsLayout)
        self._layout.addStretch()

        self._buttons = QtWidgets.QDialogButtonBox(standardButtons=QtWidgets.QDialogButtonBox.StandardButton.Close)
        self._buttons.rejected.connect(self.reject)
        self._layout.addWidget(self._buttons)
