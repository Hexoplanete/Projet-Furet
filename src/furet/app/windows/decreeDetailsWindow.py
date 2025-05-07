from PySide6 import QtWidgets, QtCore


class DecreeDetailsWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel("Détails")
        layout.addWidget(self.label)
        self.setLayout(layout)