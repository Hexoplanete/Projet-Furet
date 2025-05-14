from PySide6 import QtWidgets, QtCore, QtGui

class ElidedLabel(QtWidgets.QLabel):
    _txt: str = ""
    _elideMode: QtCore.Qt.TextElideMode = QtCore.Qt.TextElideMode.ElideRight

    def __init__(self, text: str, elideMode: QtCore.Qt.TextElideMode = QtCore.Qt.TextElideMode.ElideRight, parent: QtWidgets.QWidget = None):
        if parent is None:
            super().__init__("")
        else:
            super().__init__(parent, "")
        self._txt = text
        self._elideMode = elideMode
        self.updateDisplayedText()

    def setText(self, arg__1):
        self._txt = arg__1
        self.updateDisplayedText()

    def text(self):
        return self._txt

    def setElideMode(self, elidedMode: QtCore.Qt.TextElideMode):
        self._elideMode = elidedMode

    def elideMode(self):
        return self._elideMode

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateDisplayedText()

    def updateDisplayedText(self):
        fm = QtGui.QFontMetrics(self.fontMetrics())
        elidedText = fm.elidedText(
            self.text(), self._elideMode, self.width(), QtCore.Qt.TextFlag.TextShowMnemonic)
        if (len(self._txt) > 0):
            showFirstCharacter = self._txt[0] + "..."
            self.setMinimumWidth(fm.horizontalAdvance(showFirstCharacter) + 1)
        if self.textInteractionFlags() == QtCore.Qt.TextInteractionFlag.TextBrowserInteraction:
            elidedText = f'<a href="{self._txt}">{elidedText}</a>'
        super().setText(elidedText)
