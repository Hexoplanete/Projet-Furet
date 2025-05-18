from dataclasses import dataclass, field
from furet.repository import utils
from furet.types.decree import *
import os
from furet import repository, settings
from furet.repository import utils


decreesPerFile: dict[str, list[Decree]] = {}
maxId: int = 0


def getBasePath():
    return os.path.join(settings.value("repository.csv-root"), 'decrees')


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
    decreesPerFile[decreeFile] = utils.loadFromCsv(decreeFile, Decree)


@dataclass
class DecreeFilters:
    after: date | None = None
    before: date | None = None
    departments: list[int] = field(default_factory=list)
    campaigns: list[int] = field(default_factory=list)
    topics: list[int] = field(default_factory=list)
    name: str = ""
    treated: bool | None = None

    def fitFilters(self, decree: Decree) -> bool:
        if self.after is not None and decree.publicationDate < self.after:
            return False
        if self.before is not None and decree.publicationDate > self.before:
            return False
        if len(self.departments) > 0 and not decree.department.id in self.departments:
            return False
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
        if len(self.name) != 0 and self.name.lower() not in decree.title.lower():
            return False
        if self.treated is not None and decree.treated != self.treated:
            return False
        return True


def getDecrees(filters: DecreeFilters | None = None):
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
    utils.saveToCsv(decreeFile, decreesPerFile[decreeFile], Decree)


def getFileName(decree: Decree) -> str:
    filename = f"{decree.department.number}_{decree.publicationDate.strftime("%Y-%m")}_RAA.csv"

    basePath = getBasePath()
    fullPath = os.path.join(basePath, decree.department.number)
    fullPath = os.path.join(fullPath, filename)
    return fullPath
