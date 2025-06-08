from typing import Any, Callable
from PySide6 import QtCore, QtWidgets


class FormWidget(QtWidgets.QWidget):

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self.setStyleSheet('*[missingValue="true"] { background-color: rgba(255, 0, 0, 0.2) }')
        self._layout = QtWidgets.QFormLayout(self)
        self._layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self._layout.setContentsMargins(0, 0, 0, 0)

    def installMissingBackground(self, widget: QtWidgets.QWidget, fieldName: str, isMissing: Callable[[Any], bool]):
        signal: QtCore.SignalInstance = getattr(widget, f"{fieldName}Changed")

        def updateProp(value: Any):
            widget.setProperty("missingValue", isMissing(value))
            self.style().unpolish(widget)
            self.style().polish(widget)
        signal.connect(updateProp)
        field = getattr(widget, fieldName)
        updateProp(field())

    def addRow(self, label: str, widget: QtWidgets.QWidget, tooltip=None):
        labelWidget = QtWidgets.QLabel(f"{label} :")
        if tooltip is not None:
            labelWidget.setToolTip(tooltip)
            widget.setToolTip(tooltip)
        self._layout.addRow(labelWidget, widget)
