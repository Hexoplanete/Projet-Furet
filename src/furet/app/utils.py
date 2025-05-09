from datetime import date
from typing import Any
from PySide6 import QtWidgets

def buildComboBox(options, choice, none: tuple[str, Any] = None) -> QtWidgets.QComboBox:
    box = QtWidgets.QComboBox()
    box.setEditable(True)
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
    return box

def buildDatePicker(date:date = None) -> QtWidgets.QComboBox:
    picker = QtWidgets.QDateEdit(date=date)
    picker.setCalendarPopup(True)
    picker.setDisplayFormat("dddd d MMMM yy")
    return picker


def formatDate(value: date):
    return value.strftime("%A %d %B %Y")
