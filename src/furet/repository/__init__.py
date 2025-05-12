import datetime
from furet.types.department import *
from furet.types.decree import *
import os
import csv
from datetime import datetime

#gérer les id
# gérer la modif d'un arrete: add arrete to file (enregistrer l'id et pas tout l'objet campagne)

basePath = "./database/"
format = '%d/%m/%Y'
allDecreeList = []
campaignList = []
topicList = []
departmentList = []
docTypeList = []
def setup():
    #load config data
    loadCampaignsFromFile(basePath + '/config/campaign.csv', campaignList)
    loadDepartmentsFromFile(basePath + '/config/departments.csv', departmentList)
    loadTopicsFromFile(basePath + '/config/decreeTopics.csv', topicList)
    loadDocTypesFromFile(basePath + '/config/documentType.csv', docTypeList)
    #print(campaignList)
    # get all csvfiles from os
    for root, dirs, files in os.walk(basePath + '/prefectures/'):
        for filename in files:
            if filename.endswith(".csv"):
                filepath = os.path.join(root, filename)
                #mod_time = os.path.getmtime(filepath)  # timestamp de modification
                loadArretesFromFile(filepath,allDecreeList)
    #print(len(allDecreeList))

def getDecrees() -> list[Decree]:
    return allDecreeList
    """
    # TODO
    return [
        Decree(1, getDepartmentById(73), "XXXX", "https://example.com", 1, 2, getDocumentTypeById(1), "XXXX-XX-XX", "Test 1", datetime.datetime.now(), datetime.datetime.now(), getCampaignById(1), getTopicById(1), False, "Will"),
        Decree(2, getDepartmentById(74), "XXXX", "https://example.com", 1, 2, getDocumentTypeById(1), "XXXX-XX-XX", "Test 2", datetime.datetime.now(), datetime.datetime.now(), getCampaignById(1), getTopicById(1), False, "this"),
        Decree(3, getDepartmentById(75), "XXXX", "https://example.com", 1, 2, getDocumentTypeById(1), "XXXX-XX-XX", "Test 3", datetime.datetime.now(), datetime.datetime.now(), getCampaignById(1), getTopicById(1), False, "work"),
        Decree(4, getDepartmentById(76), "XXXX", "https://example.com", 1, 2, getDocumentTypeById(1), "XXXX-XX-XX", "Test 5", datetime.datetime.now(), datetime.datetime.now(), getCampaignById(1), getTopicById(1), False, "?"),
    ]
    """

def getDecreeById(id: int) -> Decree:
    return _findByField(getDecrees(), id)




def getDepartments() -> list[Department]:
    return departmentList


def getDepartmentById(id: int) -> Department:
    return _findByField(getDepartments(), id)


def getDocumentTypes() -> list[DocumentType]:
    return docTypeList


def getDocumentTypeById(id: int) -> DocumentType:
    return _findByField(getDocumentTypes(), id)


def getCampaign() -> list[Campaign]:
    return campaignList
    """
    # TODO add to db in setup
    return [
        Campaign(1, "Chasse"),
        Campaign(2, "Espèces protégées - grands prédateurs"),
        Campaign(3, "Blaireau"),
        Campaign(4, "ESOD"),
    ]
    """

def getCampaignById(id: int) -> Campaign:
    return _findByField(getCampaign(), id)

def getCampaignIdByLabel(label: str) -> Campaign:
    return _findByField(getCampaign(), label)

def getTopics() -> list[DecreeTopic]:
    return topicList

def getTopicById(id: int) -> DecreeTopic:
    return _findByField(getTopics(), id)


def _findByField(collection, value, field: str = "id"):
    for d in collection:
        if getattr(d, field) == value:
            return d
    return None


def addArreteToFile(arrete :Decree):
    #get the year and month
    fullPath = getFileName(arrete)
    headers = ['id', 'Département', "Type de document", "Numéro de l'arrêté", "Titre de l'arrêté", 
               "Date de signature de l'arrêté", "Numéro du RAA", "Date de publication du RAA", 'URL du RAA', 
               "Page début", "Page fin", "Campagne Aspas concernée", "Sujet", "Statut de traitement", 'Commentaire']
    row = arrete.toCsvLine()
    file_exists = os.path.isfile(fullPath) #bool

    with open(fullPath, 'a', encoding='utf-8', newline='') as file:
        writerCsv = csv.writer(file)
        # if the file is freshly created, we need to insert the column names at the beginning
        if not file_exists:
            writerCsv.writerow(headers) 
        # insert the line with the arrete
        writerCsv.writerow(row)  

def updateDecree(id: int, decree: Decree):
    #update decree data in csv file
    fileContent = []

    # 1. get the file name
    fullPath = getFileName(decree)
    
    #2. read file and it content
    with open(fullPath, encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        # On recupere le header separément du reste des lignes sinon ca pose probleme pour le cast
        header = next(reader)

        for row in reader:
            if int(row[0]) == id:
                fileContent.append(decree.toCsvLine())
            else:
                fileContent.append(row)

    #3. re-write the file content (updated)
    with open(fullPath, 'w', encoding='utf-8', newline='') as file: #w clears all the file content
        writerCsv = csv.writer(file)
        #write the header
        writerCsv.writerow(header)
        writerCsv.writerows(fileContent)

def loadArretesFromFile(path :str, listArretes : list[Decree]) -> list[Decree]:
    with open(path, encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')

        # Separate header from the other data of the csv
        header = next(reader)
        for row in reader:
            try: 
                aa = Decree(
                    id = int(row[0]), department = getDepartmentById(int(row[1])), docType = getDocumentTypeById(int(row[2])), 
                    number = row[3], title = row[4], signingDate = datetime.strptime(row[5], format).date(), raaNumber = row[6], 
                    publicationDate = datetime.strptime(row[7], format).date(), link = row[8], startPage = int(row[9]), 
                    endPage = int(row[10]), campaign = getCampaignById(int(row[11])), 
                    topic = map(getTopicById, map(int, row[12].split("-"))), 
                    treated = bool(int(row[13])), comment = row[14]
                )
                listArretes.append(aa)

            except Exception as e:
                print(f"Erreur de parsing arrêtés, ligne ignorée : {row}")
                print(f"Erreur : {e}")
    return listArretes

def loadCampaignsFromFile(path :str, listCampaigns : list[Campaign]) -> list[Campaign]:
    with open(path, encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')

        # Separate header from the other data of the csv
        header = next(reader)
        for row in reader:
            try: 
                cc = Campaign(id = int(row[0]), label = row[1])
                listCampaigns.append(cc)

            except Exception as e:
                print(f"Erreur de parsing campagnes, ligne ignorée : {row}")
                print(f"Erreur : {e}")
    return listCampaigns

def loadDepartmentsFromFile(path :str, listDepartments : list[Department]) -> list[Department]:
    with open(path, encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        # Separate header from the other data of the csv
        header = next(reader)
        for row in reader:
            try: 
                dd = Department(id = int(row[0]), number= row[1], label = row[2])
                listDepartments.append(dd)

            except Exception as e:
                print(f"Erreur de parsing départements, ligne ignorée : {row}")
                print(f"Erreur : {e}")
    return listDepartments

def loadTopicsFromFile(path :str, listTopics : list[DecreeTopic]) -> list[DecreeTopic]:
    with open(path, encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        # Separate header from the other data of the csv
        header = next(reader)
        for row in reader:
            try: 
                tt = DecreeTopic(id = int(row[0]), label = row[1])
                listTopics.append(tt)

            except Exception as e:
                print(f"Erreur de parsing sujets, ligne ignorée : {row}")
                print(f"Erreur : {e}")
    return listTopics

def loadDocTypesFromFile(path :str, listDocTypes : list[DocumentType]) -> list[DocumentType]:
    with open(path, encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        # Separate header from the other data of the csv
        header = next(reader)
        for row in reader:
            try: 
                tt = DocumentType(id = int(row[0]), label = row[1])
                listDocTypes.append(tt)

            except Exception as e:
                print(f"Erreur de parsing types de docs, ligne ignorée : {row}")
                print(f"Erreur : {e}")
    return listDocTypes

def addCampaign(label: str):
    fullPath = basePath + 'config/campaign.csv'
    try: 
        nId = updateIdFile('campaign')

        with open(fullPath, 'a', encoding='utf-8', newline='') as file:
            writerCsv = csv.writer(file)
            writerCsv.writerow([nId, label])  

    except Exception as e:
        print(f"Erreur de modification de fichier")
        print(f"Erreur : {e}")

def addTopic(label: str):
    fullPath = basePath + 'config/decreeTopics.csv'
    nId = updateIdFile('topic')

    try: 
        with open(fullPath, 'a', encoding='utf-8', newline='') as file:
            writerCsv = csv.writer(file)
            writerCsv.writerow([nId, label])  

    except Exception as e:
        print(f"Erreur de modification de fichier")
        print(f"Erreur : {e}")

def updateIdFile(attr : str) -> int:
    #update decree data in csv file
    fullPath = basePath + 'config/lastId.csv'
    fileContent = []
    
    #2. read file and its content
    with open(fullPath, encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        header = next(reader)
        for row in reader:
            if row[0] == attr:
                nextId = int(row[1]) + 1
                fileContent.append([attr, nextId])
            else:
                fileContent.append(row)

    #3. re-write the file content (updated)
    with open(fullPath, 'w', encoding='utf-8', newline='') as file: #w clears all the file content
        writerCsv = csv.writer(file)
        writerCsv.writerow(header)
        writerCsv.writerows(fileContent)
    
    return nextId


def getFileName(arrete : Decree) -> str:
    dYear = arrete.publicationDate.year
    dMonth = arrete.publicationDate.month
    filename = str(arrete.department) + "_" + str(dYear) + "_" + str(dMonth) + "_RAA.csv"
    
    fullPath = basePath + str(arrete.department) + '/' + filename
    return fullPath