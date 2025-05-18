from furet.types.decree import *
import os
from furet import settings
from furet.repository import utils

docTypes: list[DocumentType] = []


def getFilePath():
    return os.path.join(settings.value("repository.csv-root"), 'documentTypes.csv')


def loadAllDocTypes():
    global docTypes
    path = getFilePath()

    if not os.path.isfile(path):
        docTypes = [
            DocumentType(id=1, label='Arrêté préfectoral'),
            DocumentType(id=2, label='Arrêté municipal'),
            DocumentType(id=3, label='Consultation publique'),
        ]
        saveDocTypesToFile()
    else:
        docTypes = utils.loadFromCsv(path, DocumentType)


def getDocTypes():
    return docTypes


def saveDocTypesToFile():
    utils.saveToCsv(getFilePath(), docTypes, DocumentType)
