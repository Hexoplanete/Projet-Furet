from PySide6 import QtWidgets, QtCore, QtGui

class AboutUsWindow(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("About Us")

        self._rootLayout = QtWidgets.QVBoxLayout(self)

        title = QtWidgets.QLabel("<h2>About Us</h2>")
        self._rootLayout.addWidget(title)

        texte = QtWidgets.QLabel("C'est la merde")
        self._rootLayout.addWidget(texte)
