from PySide6 import QtWidgets, QtCore, QtGui

class ElidedLabel(QtWidgets.QLabel):
    _text: str = ""
    _elideMode: QtCore.Qt.TextElideMode = QtCore.Qt.TextElideMode.ElideRight

    def __init__(self, text: str, /, parent: QtWidgets.QWidget | None = None, elideMode: QtCore.Qt.TextElideMode = QtCore.Qt.TextElideMode.ElideRight):
        super().__init__("", parent)
        self._text = text
        self._elideMode = elideMode
        self.updateDisplayedText()

    def setText(self, arg__1, /):
        self._text = arg__1
        self.updateDisplayedText()

    def text(self, /):
        return self._text

    def setElideMode(self, elidedMode: QtCore.Qt.TextElideMode):
        self._elideMode = elidedMode

    def elideMode(self) -> QtCore.Qt.TextElideMode:
        return self._elideMode

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateDisplayedText()

    def updateDisplayedText(self):
        fm = QtGui.QFontMetrics(self.fontMetrics())
        elidedText = fm.elidedText(
            self.text(), self._elideMode, self.width(), QtCore.Qt.TextFlag.TextShowMnemonic)
        if (len(self._text) > 0):
            showFirstCharacter = self._text[0] + "..."
            self.setMinimumWidth(fm.horizontalAdvance(showFirstCharacter) + 1)
        if self.textInteractionFlags() == QtCore.Qt.TextInteractionFlag.TextBrowserInteraction:
            elidedText = f'<a href="{self._text}">{elidedText}</a>'
        super().setText(elidedText)
