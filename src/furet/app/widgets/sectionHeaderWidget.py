from PySide6 import QtWidgets

class SectionHeaderWidget(QtWidgets.QWidget):
    def __init__(self, label: str = ""):
        super().__init__()
        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setContentsMargins(0,0,0,0)
        self._line = QtWidgets.QFrame(frameShape=QtWidgets.QFrame.Shape.HLine)
        self._line.setFixedWidth(30)
        self._layout.addWidget(self._line)
        self._text = QtWidgets.QLabel(label)
        self._layout.addWidget(self._text)
        self._line2 = QtWidgets.QFrame(frameShape=QtWidgets.QFrame.Shape.HLine)
        self._layout.addWidget(self._line2, 1)


    def text(self):
        return self._text.text()
    
    def setText(self, text: str):
        self._text.setText(text)
