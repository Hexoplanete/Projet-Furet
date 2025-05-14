from PySide6 import QtWidgets, QtCore, QtGui

class CheckableComboBox(QtWidgets.QComboBox):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        item = QtGui.QStandardItem()
        item.setText("")
        item.setEnabled(False)
        item.setSelectable(False)
        self.view().pressed.connect(self.handleItemPressed)
        self.model().appendRow(item)

        self.model().dataChanged.connect(self.updateText)

    def resizeEvent(self, event):
        super().resizeEvent(event)

    def updateText(self):
        texts = []
        for i in range(1, self.model().rowCount()):
            if self.model().item(i).checkState() == QtCore.Qt.CheckState.Checked:
                texts.append(self.model().item(i).text())

        
        text = ", ".join(texts) if len(texts) > 0 else self.placeholderText()

        # Compute elided text (with "...")
        self.setEditable(True)
        metrics = QtGui.QFontMetrics(self.lineEdit().font())
        elidedText = metrics.elidedText(text, QtCore.Qt.TextElideMode.ElideRight, self.lineEdit().width())
        self.setItemText(0, elidedText)
        self.setEditable(False)

    def addItem(self, text, /, userData = None):
        item = QtGui.QStandardItem()
        item.setText(text)
        if userData is not None:
            item.setData(userData)

        item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
        item.setData(QtCore.Qt.CheckState.Unchecked, QtCore.Qt.ItemDataRole.CheckStateRole.CheckStateRole)
        self.model().appendRow(item)

    def addItems(self, texts, /):
        for i, text in enumerate(texts):
            self.addItem(text)

    def currentData(self):
        res = []
        for i in range(1, self.model().rowCount()):
            if self.model().item(i).checkState() == QtCore.Qt.CheckState.Checked:
                res.append(self.model().item(i).data())
        return res

    def setModel(self, model: QtCore.QAbstractItemModel):
        raise "Not supported"
    
    def model(self) -> QtGui.QStandardItemModel:
        return super().model()

    def setSelectedIndex(self, index, checked=True):
        item = self.model().item(index+1, self.modelColumn())
        item.setCheckState(QtCore.Qt.CheckState.Checked if checked else QtCore.Qt.CheckState.Unchecked)

    def setPlaceholderText(self, placeholderText):
        super().setPlaceholderText(placeholderText)
        self.updateText()

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)
