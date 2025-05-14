from datetime import date
from typing import Any
from PySide6 import QtWidgets, QtCore

from furet.app.widgets.checkableComboBox import CheckableComboBox
from furet.app.widgets.selectAllComboBox import SelectAllComboBox

from typing import TypeVar

T = TypeVar('T')

def buildComboBox(options: list[T], choice: T, none: tuple[str, Any] = None) -> QtWidgets.QComboBox:
    box = SelectAllComboBox()
    if none is not None:
        box.addItem(none[0], none[1])
        if choice == None: 
            box.setCurrentIndex(0)
    for o in options:
        box.addItem(str(o), o)
    
    if choice is not None:
        for i, o in enumerate(options):
            if o.id == choice.id:
                box.setCurrentIndex(i)

    completer = QtWidgets.QCompleter([str(o) for o in options], box)
    completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
    completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
    completer.setCompletionMode(QtWidgets.QCompleter.CompletionMode.UnfilteredPopupCompletion)
    box.setCompleter(completer)

    return box

def buildMultiComboBox(options: list[T], choices: list[T], none: str = None) -> CheckableComboBox:
    box = CheckableComboBox()
    if none is not None:
        box.setPlaceholderText(none)
    for o in options:
        box.addItem(str(o), o)
    
    for i, o in enumerate(options):
        for j, c in enumerate(choices):
            if o.id == c.id:
                box.setSelectedIndex(i, True)
    return box


def buildDatePicker(date: date = None) -> QtWidgets.QDateEdit:
    picker = QtWidgets.QDateEdit(date=date)
    picker.setCalendarPopup(True)
    picker.setDisplayFormat("dd MMMM yyyy")
    return picker


def formatDate(value: date):
    return value.strftime("%d %B %Y")

def addFormRow(form: QtWidgets.QFormLayout, label: str, widget: QtWidgets.QWidget, tooltip = ""):
    labelWidget = QtWidgets.QLabel(f"{label} :")
    labelWidget.setToolTip(tooltip)
    widget.setToolTip(tooltip)
    form.addRow(labelWidget, widget)