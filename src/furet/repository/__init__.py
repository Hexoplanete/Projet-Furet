import datetime
from furet.types.department import *
from furet.types.decree import *


def setup():
    # TODO
    ...


def getDecrees() -> list[Decree]:
    # TODO
    return [
        # Decree(1, getDepartmentById(73), "XXXX", "https://example.com", 1, 2, getDocumentTypeById(1), "XXXX-XX-XX", "Test 1", datetime.datetime.now(), datetime.datetime.now(), getCampaignById(1), getTopicById(1), False, "Will"),
        # Decree(2, getDepartmentById(74), "XXXX", "https://example.com", 1, 2, getDocumentTypeById(1), "XXXX-XX-XX", "Test 2", datetime.datetime.now(), datetime.datetime.now(), getCampaignById(1), getTopicById(1), False, "this"),
        # Decree(3, getDepartmentById(75), "XXXX", "https://example.com", 1, 2, getDocumentTypeById(1), "XXXX-XX-XX", "Test 3", datetime.datetime.now(), datetime.datetime.now(), getCampaignById(1), getTopicById(1), False, "work"),
        # Decree(4, getDepartmentById(76), "XXXX", "https://example.com", 1, 2, getDocumentTypeById(1), "XXXX-XX-XX", "Test 5", datetime.datetime.now(), datetime.datetime.now(), getCampaignById(1), getTopicById(1), False, "?"),
    ]

def getDecreeById(id: int) -> Decree:
    return _findByField(getDecrees(), id)


def getDepartments() -> list[Department]:
    # TODO add to db in setup
    return [
        Department(1, "01", "Ain"),
        Department(2, "02", "Aisne"),
        Department(3, "03", "Allier"),
        Department(4, "04", "Alpes-de-Haute-Provence"),
        Department(5, "05", "Hautes-Alpes"),
        Department(6, "06", "Alpes-Maritimes"),
        Department(7, "07", "Ardèche"),
        Department(8, "08", "Ardennes"),
        Department(9, "09", "Ariège"),
        Department(10, "10", "Aube"),
        Department(11, "11", "Aude"),
        Department(12, "12", "Aveyron"),
        Department(13, "13", "Bouches-du-Rhône"),
        Department(14, "14", "Calvados"),
        Department(15, "15", "Cantal"),
        Department(16, "16", "Charente"),
        Department(17, "17", "Charente-Maritime"),
        Department(18, "18", "Cher"),
        Department(19, "19", "Corrèze"),
        Department(20, "2A", "Corse-du-Sud"),
        Department(200, "2B", "Haute-Corse"),
        Department(21, "21", "Côte-d'Or"),
        Department(22, "22", "Côtes-d'Armor"),
        Department(23, "23", "Creuse"),
        Department(24, "24", "Dordogne"),
        Department(25, "25", "Doubs"),
        Department(26, "26", "Drôme"),
        Department(27, "27", "Eure"),
        Department(28, "28", "Eure-et-Loir"),
        Department(29, "29", "Finistère"),
        Department(30, "30", "Gard"),
        Department(31, "31", "Haute-Garonne"),
        Department(32, "32", "Gers"),
        Department(33, "33", "Gironde"),
        Department(34, "34", "Hérault"),
        Department(35, "35", "Ille-et-Vilaine"),
        Department(36, "36", "Indre"),
        Department(37, "37", "Indre-et-Loire"),
        Department(38, "38", "Isère"),
        Department(39, "39", "Jura"),
        Department(40, "40", "Landes"),
        Department(41, "41", "Loir-et-Cher"),
        Department(42, "42", "Loire"),
        Department(43, "43", "Haute-Loire"),
        Department(44, "44", "Loire-Atlantique"),
        Department(45, "45", "Loiret"),
        Department(46, "46", "Lot"),
        Department(47, "47", "Lot-et-Garonne"),
        Department(48, "48", "Lozère"),
        Department(49, "49", "Maine-et-Loire"),
        Department(50, "50", "Manche"),
        Department(51, "51", "Marne"),
        Department(52, "52", "Haute-Marne"),
        Department(53, "53", "Mayenne"),
        Department(54, "54", "Meurthe-et-Moselle"),
        Department(55, "55", "Meuse"),
        Department(56, "56", "Morbihan"),
        Department(57, "57", "Moselle"),
        Department(58, "58", "Nièvre"),
        Department(59, "59", "Nord"),
        Department(60, "60", "Oise"),
        Department(61, "61", "Orne"),
        Department(62, "62", "Pas-de-Calais"),
        Department(63, "63", "Puy-de-Dôme"),
        Department(64, "64", "Pyrénées-Atlantiques"),
        Department(65, "65", "Hautes-Pyrénées"),
        Department(66, "66", "Pyrénées-Orientales"),
        Department(67, "67", "Bas-Rhin"),
        Department(68, "68", "Haut-Rhin"),
        Department(69, "69", "Rhône"),
        Department(70, "70", "Haute-Saône"),
        Department(71, "71", "Saône-et-Loire"),
        Department(72, "72", "Sarthe"),
        Department(73, "73", "Savoie"),
        Department(74, "74", "Haute-Savoie"),
        Department(75, "75", "Paris"),
        Department(76, "76", "Seine-Maritime"),
        Department(77, "77", "Seine-et-Marne"),
        Department(78, "78", "Yvelines"),
        Department(79, "79", "Deux-Sèvres"),
        Department(80, "80", "Somme"),
        Department(81, "81", "Tarn"),
        Department(82, "82", "Tarn-et-Garonne"),
        Department(83, "83", "Var"),
        Department(84, "84", "Vaucluse"),
        Department(85, "85", "Vendée"),
        Department(86, "86", "Vienne"),
        Department(87, "87", "Haute-Vienne"),
        Department(88, "88", "Vosges"),
        Department(89, "89", "Yonne"),
        Department(90, "90", "Territoire de Belfort"),
        Department(91, "91", "Essonne"),
        Department(92, "92", "Hauts-de-Seine"),
        Department(93, "93", "Seine-Saint-Denis"),
        Department(94, "94", "Val-de-Marne"),
        Department(95, "95", "Val-d'Oise"),
        Department(971, "971", "Guadeloupe"),
        Department(972, "972", "Martinique"),
        Department(973, "973", "Guyane"),
        Department(974, "974", "La Réunion"),
        Department(976, "976", "Mayotte"),
    ]


def getDepartmentById(id: int) -> Department:
    return _findByField(getDepartments(), id)


def getDocumentTypes() -> list[DocumentType]:
    # TODO add to db in setup
    return [
        DocumentType(1, "Arrêté préfectoral"),
    ]


def getDocumentTypeById(id: int) -> DocumentType:
    return _findByField(getDocumentTypes(), id)


def getCampaign() -> list[DecreeTopic]:
    # TODO add to db in setup
    return [
        DecreeTopic(1, "Chasse"),
        DecreeTopic(2, "Espèces protégées - grands prédateurs"),
        DecreeTopic(3, "Blaireau"),
        DecreeTopic(4, "ESOD"),
    ]


def getCampaignById(id: int) -> DecreeTopic:
    return _findByField(getCampaign(), id)


def getTopics() -> list[DecreeTopic]:
    # TODO add to db in setup
    return [
        DecreeTopic(1, "chasse"),
        DecreeTopic(2, "cynégétique"),
        DecreeTopic(3, "gibier"),
        DecreeTopic(4, "vénerie"),
        DecreeTopic(5, "armes"),
        DecreeTopic(6, "tir"),
        DecreeTopic(7, "munition"),
        DecreeTopic(8, "CDCFS"),
        DecreeTopic(9, "SDG"),
        DecreeTopic(10, "blaireau"),
        DecreeTopic(11, "vénerie"),
        DecreeTopic(12, "déterrage"),
        DecreeTopic(13, "tuberculose bovine"),
        DecreeTopic(14, "loup"),
        DecreeTopic(15, "ours"),
        DecreeTopic(16, "lynx"),
        DecreeTopic(17, "chacal"),
        DecreeTopic(18, "prédation"),
        DecreeTopic(19, "prédateur"),
        DecreeTopic(20, "tirs de défense"),
        DecreeTopic(21, "tir de prélèvement"),
        DecreeTopic(22, "effarouchement"),
        DecreeTopic(23, "espèce animale protégée"),
        DecreeTopic(24, "blaireau"),
        DecreeTopic(25, "vénerie"),
        DecreeTopic(26, "déterrage"),
        DecreeTopic(27, "tuberculose bovine"),
        DecreeTopic(28, "louveterie"),
        DecreeTopic(29, "louvetier"),
        DecreeTopic(30, "piège"),
        DecreeTopic(31, "piégeage"),
        DecreeTopic(32, "destruction"),
        DecreeTopic(33, "battue"),
        DecreeTopic(34, "ESOD"),
        DecreeTopic(35, "espèce susceptible d'occasionner des dégâts"),
        DecreeTopic(36, "sanglier"),
        DecreeTopic(37, "lapin"),
        DecreeTopic(38, "pigeon"),
        DecreeTopic(39, "renard"),
        DecreeTopic(40, "corvidés"),
        DecreeTopic(41, "fouine"),
        DecreeTopic(42, "martre"),
        DecreeTopic(43, "belette"),
        DecreeTopic(44, "putois"),
        DecreeTopic(45, "corbeau freux"),
        DecreeTopic(46, "corneille noire"),
        DecreeTopic(47, "pie bavarde"),
        DecreeTopic(48, "geai"),
        DecreeTopic(49, "étourneau"),
    ]


def getTopicById(id: int) -> DecreeTopic:
    return _findByField(getTopics(), id)


def _findByField(collection, value, field: str = "id"):
    for d in collection:
        if getattr(d, field) == value:
            return d
    return None
