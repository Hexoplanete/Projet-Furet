from furet.types.decree import *
import os
import csv
from furet import settings

docTypes: list[DocumentType] = []

headers = ['id', 'label']

def getFilePath(): 
    return os.path.join(settings.value("repository.csv-root"), 'config/docType.csv')

def loadAllDocTypes():
    global docTypes
    path = getFilePath()

    if not os.path.isfile(path):
        docTypes += [
            DocumentType(id=1, label='Arrêté préfectoral'),
            DocumentType(id=2, label='Arrêté municipal'),
            DocumentType(id=3, label='Consultation publique'),
        ]
        saveDocTypesToFile()
        return
    
    docTypes.clear()
    try:
        with open(path, encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')

            header = next(reader)

            for row in reader:
                docTypes.append(DocumentType(id=int(row[0]),label=row[1],))

    except Exception as e:
        if type(e) is not StopIteration:
            print(f"Erreur fichier non trouvé {path}")
            print(f"Erreur : {e}")
    return docTypes

def getDocTypes():
    return docTypes

def saveDocTypesToFile():
    try:
        with open(getFilePath(), 'w', encoding='utf-8', newline='') as file:
            writerCsv = csv.writer(file)
            writerCsv.writerow(headers)
            for t in docTypes:
                writerCsv.writerow(t.toCsvLine())

    except Exception as e:
        print(f"Erreur de modification de fichier")
        print(f"Erreur : {e}")
