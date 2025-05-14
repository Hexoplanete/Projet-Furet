from furet.types.decree import *
import datetime
import os
import csv
from datetime import datetime
from furet import repository, settings

decreesPerFile: dict[str, list[Decree]] = {}
maxId: int = 0

def getBasePath():
    return os.path.join(settings.value("repository.csv-root"), 'prefectures')


def loadAllDecrees():
   # Separate function from setup because setup must be called before processing (information required for processing is retrieved during setup) and processing adds new decrees!
    basePath = getBasePath()
    for root, dirs, files in os.walk(basePath + '/prefectures/'):
        for filename in files:
            if filename.endswith(".csv"):
                filepath = os.path.join(root, filename)
                loadDecreeFromFiles(filepath)


def loadDecreeFromFiles(decreeFile: str):
    global maxId
    try:
        with open(decreeFile, encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')

            header = next(reader)

            decrees: list[Decree] = []
            for row in reader:
                try:
                    decrees.append[Decree(
                        id=int(row[0]),

                        raaNumber=row[6],
                        department=repository.getDepartmentById(int(row[1])),
                        link=row[8],
                        startPage=int(row[9]), endPage=int(row[10]),
                        publicationDate=datetime.strptime(
                            row[7], format).date(),

                        docType=repository.getDocumentTypeById(int(row[2])),
                        number=row[3],
                        title=row[4],
                        signingDate=datetime.strptime(row[5], format).date(),

                        campaigns=list(
                            map(repository.getCampaignById, map(int, row[11].split("-")))),
                        topics=list(map(repository.getTopicById,
                                    map(int, row[12].split("-")))),
                        treated=bool(int(row[13])),
                        missingData=row[14],
                        comment=row[15],
                    )]
                    maxId = max(maxId, decrees[-1].id)


                except Exception as e:
                    print(f"Erreur de parsing arrêtés, ligne ignorée : {row}")
                    print(f"Erreur : {e}")
            decreesPerFile[decreeFile] = decrees

    except Exception as e:
        if type(e) is not StopIteration:
            print(f"Erreur fichier non trouvé : {decreeFile}")
            print(f"Erreur : {e}")


def getDecrees():
    l = []
    for ds in decreesPerFile.values():
        l += ds
    return l


def addDecree(decree: Decree):
    global maxId
    maxId = maxId+1
    decree.id = maxId
    decreeFile = getFileName(decree)
    decreesPerFile[decreeFile].append(decree)
    saveDecreesToFile(decreeFile)


def updateDecree(id: int, decree: Decree):
    decree.id = id
    decreeFile = getFileName(decree)
    for i in range(len(decreesPerFile[decreeFile])):
        if decreesPerFile[decreeFile][i].id == decree.id:
            decreesPerFile[decreeFile][i] = decree
    saveDecreesToFile(decree)


def saveDecreesToFile(decreeFile: str):
    headers = ['id', 'Département', "Type de document", "Numéro de l'arrêté", "Titre de l'arrêté",
               "Date de signature de l'arrêté", "Numéro du RAA", "Date de publication du RAA", 'URL du RAA',
               "Page début", "Page fin", "Campagne Aspas concernée", "Sujet", "Statut de traitement", 'Commentaire', "Données Manquantes"]

    try:
        os.makedirs(decreeFile, exist_ok=True)
        with open(decreeFile, 'w', encoding='utf-8', newline='') as file:
            writerCsv = csv.writer(file)
            writerCsv.writerow(headers)
            for decree in decreesPerFile[decreeFile]:
                writerCsv.writerow(decree.toCsvLine())
    except Exception as e:
        print(f"Erreur de lecture de fichier {decreeFile}")
        print(f"Erreur : {e}")


def getFileName(arrete: Decree) -> str:
    dYear = arrete.publicationDate.year
    dMonth = arrete.publicationDate.month
    filename = arrete.department.number + "_" + \
        str(dYear) + "_" + str(dMonth) + "_RAA.csv"

    basePath = getBasePath()
    fullPath = basePath + "/prefectures/" + \
        arrete.department.number + '/' + filename
    return fullPath
