from PySide6 import QtWidgets, QtCore

class SelectAllComboBox(QtWidgets.QComboBox):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super().__init__(parent)
        self.setEditable(True)
        
        line_edit = self.lineEdit()
        line_edit.installEventFilter(self)
        
    def eventFilter(self, obj, event):
        if obj == self.lineEdit():
            if event.type() == QtCore.QEvent.MouseButtonRelease or event.type() == QtCore.QEvent.FocusIn:
                self.lineEdit().selectAll()
        return super().eventFilter(obj, event)