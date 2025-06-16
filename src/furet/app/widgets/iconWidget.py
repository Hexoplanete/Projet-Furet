from PySide6 import QtWidgets, QtGui


class IconWidget(QtWidgets.QWidget):
    def __init__(self, icon: QtGui.QIcon, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._icon = icon
        policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        policy.setWidthForHeight(True)
        self.setSizePolicy(policy)

    def setIcon(self, icon: QtGui.QIcon):
        self._icon = icon
    
    def icon(self):
        return self._icon
    
    def paintEvent(self, event, /):
        painter = QtGui.QPainter(self)
        self._icon.paint(painter, self.rect())
        painter.end()

    def resizeEvent(self, event, /) -> None:
        self.setMinimumWidth(event.size().height())