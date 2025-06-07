from datetime import date
from typing import Any
from PySide6 import QtWidgets, QtCore

from furet.app.widgets.checkableComboBox import CheckableComboBox
from furet.app.widgets.optionalDateEdit import OptionalDateEdit
from furet.app.widgets.selectAllTextComboBox import SelectAllTextComboBox

from typing import TypeVar

from furet.app.widgets.textSeparatorWidget import TextSeparatorWidget

T = TypeVar('T')

# TODO turn into a custom widget
def buildComboBox(options: list[T], choice: T | None, none: tuple[str, Any] | None = None) -> QtWidgets.QComboBox:
    box = SelectAllTextComboBox()
    if none is not None:
        box.addItem(none[0], none[1])
        if choice is None: 
            box.setCurrentIndex(0)
    for o in options:
        box.addItem(str(o), o)
    
    if choice is not None:
        for i, o in enumerate(options):
            if o == choice:
                box.setCurrentIndex(i if none is None else (i+1))

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
            if o == c:
                box.setSelectedIndex(i, True)
    return box


def buildDatePicker(date: date | None) -> OptionalDateEdit:
    picker = OptionalDateEdit(date)  # type: ignore
    picker.setCalendarPopup(True)
    picker.setDisplayFormat("dd MMMM yyyy")
    return picker


def formatDate(value: date):
    return value.strftime("%d %B %Y")

def addFormSection(layout: QtWidgets.QBoxLayout, label: str):
    if layout.count() > 0:
        layout.addSpacing(20)
    sep = TextSeparatorWidget(label)
    sep = layout.addWidget(sep)
    decreeForm = QtWidgets.QFormLayout()
    layout.addLayout(decreeForm)
    return decreeForm

def addFormRow(form: QtWidgets.QFormLayout, label: str, widget: QtWidgets.QWidget, tooltip = None):
    labelWidget = QtWidgets.QLabel(f"{label} :")
    if tooltip is not None:
        labelWidget.setToolTip(tooltip)
        widget.setToolTip(tooltip)
    form.addRow(labelWidget, widget)