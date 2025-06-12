from PySide6 import QtCore, QtWidgets, QtGui


class UrlEdit(QtWidgets.QWidget):

    urlChanged = QtCore.Signal(str)

    def __init__(self, link: str | None = None, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._urlEdit = QtWidgets.QLineEdit(link if link is not None else "")
        self._urlEdit.textChanged.connect(self.urlChanged.emit)
        self._layout.addWidget(self._urlEdit, stretch=1)
        self._openButton = QtWidgets.QPushButton()
        self._openButton.setIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowRight))
        self._openButton.clicked.connect(self.openUrl)
        self._layout.addWidget(self._openButton)

    def openUrl(self):
        QtGui.QDesktopServices.openUrl(self._urlEdit.text())

    def setUrl(self, url: str):
        self._urlEdit.setText(url)

    def url(self) -> str:
        return self._urlEdit.text()
