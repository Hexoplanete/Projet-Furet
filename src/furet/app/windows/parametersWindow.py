from PySide6 import QtWidgets, QtCore


class ParametersWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paramètres")
        layout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel("Paramètres\n\nSuch Space\n\tSuch wow")
        layout.addWidget(self.label)
