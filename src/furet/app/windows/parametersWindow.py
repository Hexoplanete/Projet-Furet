from PySide6 import QtWidgets, QtCore


class ParametersWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel("Paramètres")
        layout.addWidget(self.label)
