# https://wiki.qt.io/Elided_Label

from PySide6 import QtWidgets, QtCore, QtGui

class ElidedLabel(QtWidgets.QLabel):

    _elideMode: QtCore.Qt.TextElideMode = QtCore.Qt.TextElideMode.ElideRight
    _cachedElidedText: str = ""
    _cachedText: str = ""

    def setElideMode(self, elidedMode: QtCore.Qt.TextElideMode):
        self._elideMode = elidedMode

    def elideMode(self):
        return self._elideMode


    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._cachedText = ""
    
    def paintEvent(self, event, /):
        if (self._elideMode == QtCore.Qt.TextElideMode.ElideNone):
            return super().paintEvent(event)

        self.updateCachedTexts()
        super().setText(self._cachedElidedText)
        super().paintEvent(event)
        super().setText(self._cachedText)

    def updateCachedTexts(self): 
        txt = self.text()
        if (self._cachedText == txt):
            return 
        self._cachedText = txt
        fm = QtGui.QFontMetrics(self.fontMetrics())
        self._cachedElidedText = fm.elidedText(self.text(), self._elideMode, self.width(), QtCore.Qt.TextFlag.TextShowMnemonic)
        if (len(self._cachedText) > 0):
            showFirstCharacter = self._cachedText[0] + "..."
            self.setMinimumWidth(fm.horizontalAdvance(showFirstCharacter) + 1)
class ElidedLabel(QtWidgets.QLabel):

    _elideMode: QtCore.Qt.TextElideMode = QtCore.Qt.TextElideMode.ElideRight
    _cachedElidedText: str = ""
    _cachedText: str = ""

    def setElideMode(self, elidedMode: QtCore.Qt.TextElideMode):
        self._elideMode = elidedMode

    def elideMode(self):
        return self._elideMode


    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._cachedText = ""
    
    def paintEvent(self, event, /):
        if (self._elideMode == QtCore.Qt.TextElideMode.ElideNone):
            return super().paintEvent(event)

        self.updateCachedTexts()
        super().setText(self._cachedElidedText)
        super().paintEvent(event)
        super().setText(self._cachedText)

    def updateCachedTexts(self): 
        txt = self.text()
        if (self._cachedText == txt):
            return 
        self._cachedText = txt
        fm = QtGui.QFontMetrics(self.fontMetrics())
        self._cachedElidedText = fm.elidedText(self.text(), self._elideMode, self.width(), QtCore.Qt.TextFlag.TextShowMnemonic)
        if (len(self._cachedText) > 0):
            showFirstCharacter = self._cachedText[0] + "..."
            self.setMinimumWidth(fm.horizontalAdvance(showFirstCharacter) + 1)

class ElidedHyperlink(QtWidgets.QLabel):

    _elideMode: QtCore.Qt.TextElideMode = QtCore.Qt.TextElideMode.ElideRight
    _cachedElidedText: str = ""
    _cachedText: str = ""

    def setElideMode(self, elidedMode: QtCore.Qt.TextElideMode):
        self._elideMode = elidedMode

    def elideMode(self):
        return self._elideMode


    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._cachedText = ""
    
    def paintEvent(self, event, /):
        if (self._elideMode == QtCore.Qt.TextElideMode.ElideNone):
            return super().paintEvent(event)

        self.updateCachedTexts()
        super().setText(f"<a href=\"{self.text()}\">{self._cachedElidedText}</a>")
        super().paintEvent(event)
        super().setText(self._cachedText)

    def updateCachedTexts(self): 
        txt = self.text()
        if (self._cachedText == txt):
            return 
        self._cachedText = txt
        fm = QtGui.QFontMetrics(self.fontMetrics())
        self._cachedElidedText = fm.elidedText(self.text(), self._elideMode, self.width(), QtCore.Qt.TextFlag.TextShowMnemonic)
        if (len(self._cachedText) > 0):
            showFirstCharacter = self._cachedText[0] + "..."
            self.setMinimumWidth(fm.horizontalAdvance(showFirstCharacter) + 1)
