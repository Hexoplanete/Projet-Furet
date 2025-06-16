from PySide6 import QtCore, QtWidgets

class SectionHeaderWidget(QtWidgets.QWidget):
    def __init__(self, label: str = ""):
        super().__init__()
        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setContentsMargins(0,20,0,5)
        self._text = QtWidgets.QLabel(f"<h3>{label}</h3>", alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self._text)

    def text(self):
        return self._text.text()
    
    def setText(self, text: str):
        self._text.setText(text)
