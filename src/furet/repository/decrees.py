from dataclasses import dataclass, field
from furet.repository import utils
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
    for root, dirs, files in os.walk(basePath):
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
                    decrees.append(Decree(
                        id=int(row[0]),

                        raaNumber=row[6],
                        department=repository.getDepartmentById(int(row[1])),
                        link=row[8],
                        startPage=int(row[9]), endPage=int(row[10]),
                        publicationDate=datetime.strptime(
                            row[7], "%d/%m/%Y").date(),

                        docType=repository.getDocumentTypeById(int(row[2])),
                        number=row[3],
                        title=row[4],
                        signingDate=datetime.strptime(row[5], "%d/%m/%Y").date(),

                        campaigns=list(map(repository.getCampaignById, utils.splitIdList(row[11]))),
                        topics=list(map(repository.getTopicById, utils.splitIdList(row[12]))),
                        treated=bool(int(row[13])),
                        missingData=bool(int(row[14])),
                        comment=row[15],
                    ))
                    maxId = max(maxId, decrees[-1].id)

                except Exception as e:
                    print(f"Erreur de parsing arrêtés, ligne ignorée : {row}")
                    print(f"Erreur : {e}")
            decreesPerFile[decreeFile] = decrees

    except Exception as e:
        if type(e) is not StopIteration:
            print(f"Erreur fichier non trouvé : {decreeFile}")
            print(f"Erreur : {e}")


@dataclass
class DecreeFilters:
    after: Optional[date] = None
    before: Optional[date] = None
    departments: list[int] = field(default_factory=list)
    campaigns: list[int] = field(default_factory=list)
    topics: list[int] = field(default_factory=list)
    name: str = ""
    treated: Optional[bool] = None

    def fitFilters(self, decree: Decree) -> bool:
        if self.after is not None and decree.publicationDate < self.after: return False
        if self.before is not None and decree.publicationDate > self.before: return False
        if len(self.departments) > 0 and not decree.department.id in self.departments: return False
        if len(self.campaigns) > 0:
            for c in decree.campaigns:
                if c.id in self.campaigns:
                    break
            else:
                return False
            
        if len(self.topics) > 0:
            dTopics = set(map(lambda t: t.id, decree.topics))
            for id in self.topics:
                if id not in dTopics:
                    return False
        if len(self.name) != 0 and self.name.lower() not in decree.title.lower(): return False
        if self.treated is not None and decree.treated != self.treated: return False
        return True


def getDecrees(filters: Optional[DecreeFilters] = None):
    l = []
    for ds in decreesPerFile.values():
        if filters is None:
            l += ds
        else:
            l += filter(filters.fitFilters, ds)
    return l


def _addDecree(decree: Decree):
    global maxId
    maxId = maxId+1
    decree.id = maxId
    decreeFile = getFileName(decree)
    if not decreeFile in decreesPerFile:
        decreesPerFile[decreeFile] = []
    decreesPerFile[decreeFile].append(decree)
def addDecree(decree: Decree):
    _addDecree(decree)
    saveDecreesToFile(getFileName(decree))

def addDecrees(decrees: list[Decree]):
    files = set()
    for d in decrees:
        files.add(getFileName(d))
        _addDecree(d)
    for f in files:
        saveDecreesToFile(f)


def updateDecree(id: int, decree: Decree):
    oldDecreeFile = getFileName(repository.getDecreeById(id))
    decree.id = id
    decreeFile = getFileName(decree)
    
    if not decreeFile in decreesPerFile:
        decreesPerFile[decreeFile] = []
    
    if oldDecreeFile != decreeFile:
        decreesPerFile[oldDecreeFile].remove(decree)
        decreesPerFile[decreeFile].append(decree)
        saveDecreesToFile(oldDecreeFile)
        saveDecreesToFile(decreeFile)
        return

    i = decreesPerFile[decreeFile].index(decree)
    decreesPerFile[decreeFile][i] = decree
    saveDecreesToFile(decreeFile)


def saveDecreesToFile(decreeFile: str):
    headers = ['id', 'Département', "Type de document", "Numéro de l'arrêté", "Titre de l'arrêté",
               "Date de signature de l'arrêté", "Numéro du RAA", "Date de publication du RAA", 'URL du RAA',
               "Page début", "Page fin", "Campagne Aspas concernée", "Sujet", "Statut de traitement", 'Commentaire', "Données Manquantes"]

    try:
        os.makedirs(os.path.dirname(decreeFile), exist_ok=True)
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
    filename = arrete.department.number + "_" + str(dYear) + "_" + str(dMonth) + "_RAA.csv"

    basePath = getBasePath()
    fullPath = os.path.join(basePath, arrete.department.number)
    fullPath = os.path.join(fullPath, filename)
    return fullPath
