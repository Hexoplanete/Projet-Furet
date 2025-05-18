from furet.repository import utils
from furet.types.decree import *
import os
from furet import settings

departments: list[Department] = []


def getFilePath():
    return os.path.join(settings.value("repository.csv-root"), 'departments.csv')


def loadAllDepartments():
    global departments
    path = getFilePath()

    if not os.path.isfile(path):
        departments = [
            Department(id=1, number='01', label='Ain'),
            Department(id=2, number='02', label='Aisne'),
            Department(id=3, number='03', label='Allier'),
            Department(id=4, number='04', label='Alpes-de-Haute-Provence'),
            Department(id=5, number='05', label='Hautes-Alpes'),
            Department(id=6, number='06', label='Alpes-Maritimes'),
            Department(id=7, number='07', label='Ardèche'),
            Department(id=8, number='08', label='Ardennes'),
            Department(id=9, number='09', label='Ariège'),
            Department(id=10, number='10', label='Aube'),
            Department(id=11, number='11', label='Aude'),
            Department(id=12, number='12', label='Aveyron'),
            Department(id=13, number='13', label='Bouches-du-Rhône'),
            Department(id=14, number='14', label='Calvados'),
            Department(id=15, number='15', label='Cantal'),
            Department(id=16, number='16', label='Charente'),
            Department(id=17, number='17', label='Charente-Maritime'),
            Department(id=18, number='18', label='Cher'),
            Department(id=19, number='19', label='Corrèze'),
            Department(id=200, number='2A', label='Corse-du-Sud'),
            Department(id=201, number='2B', label='Haute-Corse'),
            Department(id=21, number='21', label="Côte-d'Or"),
            Department(id=22, number='22', label="Côtes-d'Armor"),
            Department(id=23, number='23', label='Creuse'),
            Department(id=24, number='24', label='Dordogne'),
            Department(id=25, number='25', label='Doubs'),
            Department(id=26, number='26', label='Drôme'),
            Department(id=27, number='27', label='Eure'),
            Department(id=28, number='28', label='Eure-et-Loir'),
            Department(id=29, number='29', label='Finistère'),
            Department(id=30, number='30', label='Gard'),
            Department(id=31, number='31', label='Haute-Garonne'),
            Department(id=32, number='32', label='Gers'),
            Department(id=33, number='33', label='Gironde'),
            Department(id=34, number='34', label='Hérault'),
            Department(id=35, number='35', label='Ille-et-Vilaine'),
            Department(id=36, number='36', label='Indre'),
            Department(id=37, number='37', label='Indre-et-Loire'),
            Department(id=38, number='38', label='Isère'),
            Department(id=39, number='39', label='Jura'),
            Department(id=40, number='40', label='Landes'),
            Department(id=41, number='41', label='Loir-et-Cher'),
            Department(id=42, number='42', label='Loire'),
            Department(id=43, number='43', label='Haute-Loire'),
            Department(id=44, number='44', label='Loire-Atlantique'),
            Department(id=45, number='45', label='Loiret'),
            Department(id=46, number='46', label='Lot'),
            Department(id=47, number='47', label='Lot-et-Garonne'),
            Department(id=48, number='48', label='Lozère'),
            Department(id=49, number='49', label='Maine-et-Loire'),
            Department(id=50, number='50', label='Manche'),
            Department(id=51, number='51', label='Marne'),
            Department(id=52, number='52', label='Haute-Marne'),
            Department(id=53, number='53', label='Mayenne'),
            Department(id=54, number='54', label='Meurthe-et-Moselle'),
            Department(id=55, number='55', label='Meuse'),
            Department(id=56, number='56', label='Morbihan'),
            Department(id=57, number='57', label='Moselle'),
            Department(id=58, number='58', label='Nièvre'),
            Department(id=59, number='59', label='Nord'),
            Department(id=60, number='60', label='Oise'),
            Department(id=61, number='61', label='Orne'),
            Department(id=62, number='62', label='Pas-de-Calais'),
            Department(id=63, number='63', label='Puy-de-Dôme'),
            Department(id=64, number='64', label='Pyrénées-Atlantiques'),
            Department(id=65, number='65', label='Hautes-Pyrénées'),
            Department(id=66, number='66', label='Pyrénées-Orientales'),
            Department(id=67, number='67', label='Bas-Rhin'),
            Department(id=68, number='68', label='Haut-Rhin'),
            Department(id=69, number='69', label='Rhône'),
            Department(id=70, number='70', label='Haute-Saône'),
            Department(id=71, number='71', label='Saône-et-Loire'),
            Department(id=72, number='72', label='Sarthe'),
            Department(id=73, number='73', label='Savoie'),
            Department(id=74, number='74', label='Haute-Savoie'),
            Department(id=75, number='75', label='Paris'),
            Department(id=76, number='76', label='Seine-Maritime'),
            Department(id=77, number='77', label='Seine-et-Marne'),
            Department(id=78, number='78', label='Yvelines'),
            Department(id=79, number='79', label='Deux-Sèvres'),
            Department(id=80, number='80', label='Somme'),
            Department(id=81, number='81', label='Tarn'),
            Department(id=82, number='82', label='Tarn-et-Garonne'),
            Department(id=83, number='83', label='Var'),
            Department(id=84, number='84', label='Vaucluse'),
            Department(id=85, number='85', label='Vendée'),
            Department(id=86, number='86', label='Vienne'),
            Department(id=87, number='87', label='Haute-Vienne'),
            Department(id=88, number='88', label='Vosges'),
            Department(id=89, number='89', label='Yonne'),
            Department(id=90, number='90', label='Territoire de Belfort'),
            Department(id=91, number='91', label='Essonne'),
            Department(id=92, number='92', label='Hauts-de-Seine'),
            Department(id=93, number='93', label='Seine-Saint-Denis'),
            Department(id=94, number='94', label='Val-de-Marne'),
            Department(id=95, number='95', label="Val-d'Oise"),
            Department(id=971, number='971', label='Guadeloupe'),
            Department(id=972, number='972', label='Martinique'),
            Department(id=973, number='973', label='Guyane'),
            Department(id=974, number='974', label='La Réunion'),
            Department(id=976, number='976', label='Mayotte'),
        ]
        saveDepartmentsToFile()
    else:
        departments = utils.loadFromCsv(path, Department)


def getDepartments():
    return departments


def saveDepartmentsToFile():
    utils.saveToCsv(getFilePath(), departments, Department)
