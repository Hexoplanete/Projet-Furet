from typing import Any, Callable
from PySide6 import QtWidgets, QtCore, Qt

from furet.types.Decree import *
from furet.ui.widgets.ObjectTableModel import ObjectTableModel


class DecreeFilterProxy(QtCore.QSortFilterProxyModel):

    def __init__(self, filterer: Callable[[int, QtCore.QModelIndex | QtCore.QPersistentModelIndex], bool], parent=None):
        super().__init__(parent)
        self._filterer = filterer

    def setSourceModel(self, model: ObjectTableModel[Decree]):
        super().setSourceModel(model)

    def sourceModel(self) -> ObjectTableModel[Decree]:
        return super().sourceModel()

    def filterAcceptsRow(self, source_row, source_parent, /):
        return self._filterer(self.sourceModel().itemAt(source_row))


class DecreeFilterWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._layout = QtWidgets.QHBoxLayout(self)

        self._proxy = DecreeFilterProxy(filterer=self.filterDecrees)
        
        self._department = QtWidgets.QComboBox()
        self._department.addItems([
                "Aucun",
                "01 : Ain",
                "02 : Aisne",
                "03 : Allier",
                "04 : Alpes-de-Haute-Provence",
                "05 : Hautes-Alpes",
                "06 : Alpes-Maritimes",
                "07 : Ardèche",
                "08 : Ardennes",
                "09 : Ariège",
                "10 : Aube",
                "11 : Aude",
                "12 : Aveyron",
                "13 : Bouches-du-Rhône",
                "14 : Calvados",
                "15 : Cantal",
                "16 : Charente",
                "17 : Charente-Maritime",
                "18 : Cher",
                "19 : Corrèze",
                "2A : Corse-du-Sud",
                "2B : Haute-Corse",
                "21 : Côte-d'Or",
                "22 : Côtes-d'Armor",
                "23 : Creuse",
                "24 : Dordogne",
                "25 : Doubs",
                "26 : Drôme",
                "27 : Eure",
                "28 : Eure-et-Loir",
                "29 : Finistère",
                "30 : Gard",
                "31 : Haute-Garonne",
                "32 : Gers",
                "33 : Gironde",
                "34 : Hérault",
                "35 : Ille-et-Vilaine",
                "36 : Indre",
                "37 : Indre-et-Loire",
                "38 : Isère",
                "39 : Jura",
                "40 : Landes",
                "41 : Loir-et-Cher",
                "42 : Loire",
                "43 : Haute-Loire",
                "44 : Loire-Atlantique",
                "45 : Loiret",
                "46 : Lot",
                "47 : Lot-et-Garonne",
                "48 : Lozère",
                "49 : Maine-et-Loire",
                "50 : Manche",
                "51 : Marne",
                "52 : Haute-Marne",
                "53 : Mayenne",
                "54 : Meurthe-et-Moselle",
                "55 : Meuse",
                "56 : Morbihan",
                "57 : Moselle",
                "58 : Nièvre",
                "59 : Nord",
                "60 : Oise",
                "61 : Orne",
                "62 : Pas-de-Calais",
                "63 : Puy-de-Dôme",
                "64 : Pyrénées-Atlantiques",
                "65 : Hautes-Pyrénées",
                "66 : Pyrénées-Orientales",
                "67 : Bas-Rhin",
                "68 : Haut-Rhin",
                "69 : Rhône",
                "70 : Haute-Saône",
                "71 : Saône-et-Loire",
                "72 : Sarthe",
                "73 : Savoie",
                "74 : Haute-Savoie",
                "75 : Paris",
                "76 : Seine-Maritime",
                "77 : Seine-et-Marne",
                "78 : Yvelines",
                "79 : Deux-Sèvres",
                "80 : Somme",
                "81 : Tarn",
                "82 : Tarn-et-Garonne",
                "83 : Var",
                "84 : Vaucluse",
                "85 : Vendée",
                "86 : Vienne",
                "87 : Haute-Vienne",
                "88 : Vosges",
                "89 : Yonne",
                "90 : Territoire de Belfort",
                "91 : Essonne",
                "92 : Hauts-de-Seine",
                "93 : Seine-Saint-Denis",
                "94 : Val-de-Marne",
                "95 : Val-d'Oise",
                "971 : Guadeloupe",
                "972 : Martinique",
                "973 : Guyane",
                "974 : La Réunion",
                "976 : Mayotte"
            ])
        self._department.setPlaceholderText("Département")
        self._department.setEditText("Département")
        self._department.setEditable(True)
        self._layout.addWidget(self._department)

        
        self._topic = QtWidgets.QComboBox()
        self._topic.addItems(["TODO1", "TODO2", "TODO3"])
        self._layout.addWidget(self._topic)

        self._name = QtWidgets.QLineEdit()
        self._layout.addWidget(self._name)

        self._date = QtWidgets.QDateEdit()
        self._layout.addWidget(self._date)

        self._state = QtWidgets.QCheckBox()
        self._layout.addWidget(self._state)

        
        self._researchButton = QtWidgets.QPushButton('Rechercher')
        self._researchButton.clicked.connect(self.onClickResearchButton)
        self._layout.addWidget(self._researchButton)


    def data(self, index, /, role = ...):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return getattr(self._data[index.row()], self._fields[index.column()])

    def rowCount(self, /, parent = ...):
        return len(self._data)
    
    def setModel(self, model: ObjectTableModel):
        self._model = model
        self._proxy.setSourceModel(model)

    def proxyModel(self) -> DecreeFilterProxy:
        return self._proxy
    
    def onClickResearchButton(self):
        firstText = self._department.currentText().split(" ")[0]
        self._departementValue = int(firstText) if firstText.isnumeric() else 0 # Donne le numéro du département (0 si aucun)

        """
        # self._model.
        proxy = QtCore.QSortFilterProxyModel()
        proxy.setSourceModel(self._model)  # mon_model est ton QAbstractTableModel

        # Exemple : filtrer par une chaîne de caractères dans une colonne
        proxy.setFilterKeyColumn(1)  # Colonne 1 par exemple
        proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
        proxy.setFilterFixedString("exemple")  # Ou utiliser setFilterRegExp()
        proxy.filterAcceptsRow
        """

        self._topicValue = self._topic.currentText()
        self._nameValue = self._name.text()
        self._dateValue = self._date.date()
        self._stateValue = self._state.checkState()

        self._proxy.invalidateFilter()

        return
    
    def filterDecrees(self, decree: Decree):
        # TODO will be broken later
        if self._departementValue != 0 and decree.department != self._departementValue: return False
        return True

    # def rowCount(self, index):

    # def columnCount(self, index):
    #     return len(self._fields)

