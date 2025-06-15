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
    
    def displayedText(self, /):
        return super().text()

    def setElideMode(self, elidedMode: QtCore.Qt.TextElideMode):
        self._elideMode = elidedMode

    def elideMode(self) -> QtCore.Qt.TextElideMode:
        return self._elideMode

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateDisplayedText()

    def updateDisplayedText(self):
        fm = QtGui.QFontMetrics(self.fontMetrics())
        elidedText = fm.elidedText(self._text, self._elideMode, self.width(), QtCore.Qt.TextFlag.TextShowMnemonic)
        if (len(self._text) > 0):
            showFirstCharacter = self._text[0] + "..."
            self.setMinimumWidth(fm.horizontalAdvance(showFirstCharacter) + 1)
        super().setText(elidedText)


class ElidedUri(ElidedLabel):

    def __init__(self, uri: str, /, parent: QtWidgets.QWidget | None = None, text: str | None = None, elideMode: QtCore.Qt.TextElideMode = QtCore.Qt.TextElideMode.ElideRight):
        self._hasText = text is not None
        self._uri = uri
        super().__init__(text or uri, parent, elideMode)
        self.setOpenExternalLinks(True)

    def setUri(self, uri: str):
        self._uri = uri
        self.setToolTip(uri)
        self.updateDisplayedText()

    def uri(self, /) -> str:
        return self._uri

    def setText(self, text: str | None):
        self._hasText = text is not None
        if text is not None:
            super().setText(text)
        else:
            super().setText(self._uri)

    def text(self, /) -> str | None:  # type: ignore
        return super().text() if self._hasText else None

    def updateDisplayedText(self):
        super().updateDisplayedText()
        QtWidgets.QLabel.setText(
            self, f'<a href="{self._uri}">{self.displayedText()}</a>')


class ElidedPath(ElidedUri):

    def __init__(self, path: str, /, parent: QtWidgets.QWidget | None = None, elideMode: QtCore.Qt.TextElideMode = QtCore.Qt.TextElideMode.ElideMiddle):
        self._path = path
        super().__init__(self.toUri(path), parent, path, elideMode)

    def setPath(self, path: str):
        self._path = path
        self.setUri(self.toUri(path))
        self.setText(path)
    
    def path(self):
        return self._path

    def toUri(self, path: str) -> str:
        return f"file:/{path.removeprefix("/")}"
