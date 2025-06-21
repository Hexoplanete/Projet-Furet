from datetime import date
from PySide6 import QtWidgets, QtCore, QtGui
from typing import TypeVar, Generic
from furet.app.widgets.objectTableWidget import ObjectTableColumn
from furet.models.campaign import Campaign, Topic
from furet.models.decree import Decree
from furet.models.raa import Department


T = TypeVar('T')


def formatDate(value: date):
    return value.strftime("%d %B %Y")


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


NONE_QDATE = date(1900, 1, 1)
DECREE_COLUMNS = [
    DecreeColumn[date|None]("Date de publication", lambda v: v.raa.publicationDate, lambda v: "Non définie" if v is None else formatDate(v), lambda v: v or NONE_QDATE),
    DecreeColumn[date|None]("Date d'expiration", lambda v: v.raa.expireDate(), lambda v: "Non définie" if v is None else formatDate(v), lambda v: v or NONE_QDATE),
    DecreeColumn[Department|None]("Département", lambda v: v.raa.department, lambda v: "Non défini" if v is None else str(v), lambda v: 0 if v is None else v.id),
    DecreeColumn[list[Campaign]]("Campagnes", lambda v: v.campaigns, lambda v: ", ".join(map(str, v)), lambda v: list(map(lambda i: i.label, v))),
    DecreeColumn[list[Topic]]("Sujets", lambda v: v.topics, lambda v: ", ".join(map(str, v)), lambda v: list(map(lambda i: i.label, v))),
    DecreeColumn[str]("Titre", lambda v: v.title, resizeMode=QtWidgets.QHeaderView.ResizeMode.Stretch),
    DecreeColumn[int]("À compléter", lambda v: v.missingValues(), lambda v: f"{v} champs" if v else ""),
    DecreeStateColumn("État", lambda v: v.treated, lambda v: "Traité" if v else "À traiter"),
    DecreeColumn[str]("Commentaire", lambda v: v.comment, resizeMode=QtWidgets.QHeaderView.ResizeMode.ResizeToContents),
]
