from datetime import date
from typing import Any
from PySide6 import QtWidgets, QtCore, QtGui

from furet.app.widgets.checkableComboBox import CheckableComboBox
from furet.app.widgets.objectTableModel import ObjectTableColumn
from furet.app.widgets.optionalDateEdit import NONE_DATE, OptionalDateEdit
from furet.app.widgets.selectAllTextComboBox import SelectAllTextComboBox

from typing import TypeVar, Generic

from furet.app.widgets.textSeparatorWidget import TextSeparatorWidget
from furet.types.campaign import Campaign, Topic
from furet.types.decree import Decree
from furet.types.department import Department

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

class DecreeColumn(Generic[T], ObjectTableColumn[Decree, T]):
    def data(self, item: Decree, /, role: QtCore.Qt.ItemDataRole):
        if role == QtCore.Qt.ItemDataRole.BackgroundRole:
            if item.missingValues():
                return QtGui.QColor(255, 0, 0, a=50)
        return super().data(item, role=role)


class DecreeStateColumn(DecreeColumn[bool]):
    def data(self, item: Decree, /, role: QtCore.Qt.ItemDataRole):
        if role == QtCore.Qt.ItemDataRole.BackgroundRole:
            if item.missingValues() or not self.value(item):
                return QtGui.QColor(255, 0, 0, a=50)
        return super().data(item, role=role)

DECREE_COLUMNS = [
    DecreeColumn[date|None]("Date de publication", lambda v: v.raa.publicationDate, lambda v: "Non définie" if v is None else formatDate(v), lambda v: v or NONE_DATE),
    DecreeColumn[date|None]("Date d'expiration", lambda v: v.raa.expireDate(), lambda v: "Non définie" if v is None else formatDate(v), lambda v: v or NONE_DATE),
    DecreeColumn[Department|None]("Département", lambda v: v.raa.department, lambda v: "Non défini" if v is None else str(v), lambda v: 0 if v is None else v.id),
    DecreeColumn[list[Campaign]]("Campagnes", lambda v: v.campaigns, lambda v: ", ".join(map(str, v)), lambda v: list(map(lambda i: i.label, v))),
    DecreeColumn[list[Topic]]("Sujets", lambda v: v.topics, lambda v: ", ".join(map(str, v)), lambda v: list(map(lambda i: i.label, v))),
    DecreeColumn[str]("Titre", lambda v: v.title, resizeMode=QtWidgets.QHeaderView.ResizeMode.Stretch),
    DecreeColumn[int]("À compléter", lambda v: v.missingValues(), lambda v: f"{v} champs" if v else ""),  # TODO label not visible
    DecreeStateColumn("État", lambda v: v.treated, lambda v: "Traité" if v else "À traiter"),
    DecreeColumn[str]("Commentaire", lambda v: v.comment, resizeMode=QtWidgets.QHeaderView.ResizeMode.ResizeToContents),
]
