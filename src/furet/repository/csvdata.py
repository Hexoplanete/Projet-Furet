from furet.types.decree import *
import datetime
import os
import csv
from datetime import datetime
from furet import repository, settings

format = '%d/%m/%Y'
allDecreeList = []
campaignList = []
topicList = []
departmentList = []
docTypeList = []

ROOT_KEY = "repository.csv.root"
def setup():
    settings.setDefaultValue(ROOT_KEY,  "database")

def load():
    # load config data
    basePath = settings.value(ROOT_KEY)
    loadTopicsFromFile(os.path.join(basePath, 'config/decreeTopics.csv'), topicList)
    loadCampaignsFromFile(os.path.join(basePath, 'config/campaign.csv'), campaignList)
    loadDepartmentsFromFile(os.path.join(basePath, 'config/departments.csv'), departmentList)
    loadDocTypesFromFile(os.path.join(basePath, 'config/documentType.csv'), docTypeList)

    # get all csvfiles from os
    for root, dirs, files in os.walk(os.path.join(basePath, 'prefectures')):
        for filename in files:
            if filename.endswith(".csv"):
                filepath = os.path.join(root, filename)
                # mod_time = os.path.getmtime(filepath)  # timestamp de modification
                loadArretesFromFile(filepath, allDecreeList)
    # print(len(allDecreeList))

def addArreteToFile(arrete: Decree):
    # get the year and month
    fullPath = getFileName(arrete)
    headers = ['id', 'Département', "Type de document", "Numéro de l'arrêté", "Titre de l'arrêté",
               "Date de signature de l'arrêté", "Numéro du RAA", "Date de publication du RAA", 'URL du RAA',
               "Page début", "Page fin", "Campagne Aspas concernée", "Sujet", "Statut de traitement", 'Commentaire']
    row = arrete.toCsvLine()
    file_exists = os.path.isfile(fullPath)  # bool

    with open(fullPath, 'a', encoding='utf-8', newline='') as file:
        writerCsv = csv.writer(file)
        # if the file is freshly created, we need to insert the column names at the beginning
        if not file_exists:
            writerCsv.writerow(headers)
        # insert the line with the arrete
        writerCsv.writerow(row)


def updateDecree(id: int, decree: Decree):
    # update decree data in csv file
    fileContent = []
    try: 
        # 1. get the file name
        fullPath = getFileName(decree)
        # 2. read file and it content
        with open(fullPath, encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')
            # Get the header separately from the rest, to avoid cast error
            header = next(reader)

            for row in reader:
                if int(row[0]) == id:
                    fileContent.append(decree.toCsvLine())
                else:
                    fileContent.append(row)

        # 3. re-write the file content (updated)
        with open(fullPath, 'w', encoding='utf-8', newline='') as file:  # w clears all the file content
            writerCsv = csv.writer(file)
            # write the header
            writerCsv.writerow(header)
            writerCsv.writerows(fileContent)
    
    except Exception as e:
                print(f"Erreur de lecture de fichier {fullPath}")
                print(f"Erreur : {e}")


def loadArretesFromFile(path: str, listArretes: list[Decree]) -> list[Decree]:
    try:
        with open(path, encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')

            # Separate header from the other data of the csv
            header = next(reader)
            for row in reader:
                try:
                    aa = Decree(
                        id=int(row[0]), department=repository.getDepartmentById(int(row[1])), docType=repository.getDocumentTypeById(int(row[2])),
                        number=row[3], title=row[4], signingDate=datetime.strptime(row[5], format).date(), raaNumber=row[6],
                        publicationDate=datetime.strptime(row[7], format).date(), link=row[8], startPage=int(row[9]),
                        endPage=int(row[10]), campaign=repository.getCampaignById(int(row[11])),
                        topic=list(
                            map(repository.getTopicById, map(int, row[12].split("-")))),
                        treated=bool(int(row[13])), comment=row[14]
                    )
                    listArretes.append(aa)

                except Exception as e:
                    print(f"Erreur de parsing arrêtés, ligne ignorée : {row}")
                    print(f"Erreur : {e}")
    except Exception as e:
        print(f"Erreur fichier non trouvé : {path}")
        print(f"Erreur : {e}")
    return listArretes


def loadCampaignsFromFile(path: str, listCampaigns: list[Campaign]) -> list[Campaign]:
    try: 
        with open(path, encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')

            # Separate header from the other data of the csv
            header = next(reader)
            for row in reader:
                try:
                    cc = Campaign(
                                  id=int(row[0]), 
                                  label=row[1], 
                                  topicList = list(map(repository.getTopicById, map(int, row[2].split("-"))))
                                  )
                    listCampaigns.append(cc)

                except Exception as e:
                    print(f"Erreur de parsing campagnes, ligne ignorée : {row}")
                    print(f"Erreur : {e}")
    except Exception as e:
                print(f"Erreur fichier non trouvé {path}")
                print(f"Erreur : {e}")
    return listCampaigns


def loadDepartmentsFromFile(path: str, listDepartments: list[Department]) -> list[Department]:
    try: 
        with open(path, encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')
            # Separate header from the other data of the csv
            header = next(reader)
            for row in reader:
                try:
                    dd = Department(id=int(row[0]), number=row[1], label=row[2])
                    listDepartments.append(dd)

                except Exception as e:
                    print(f"Erreur de parsing départements, ligne ignorée : {row}")
                    print(f"Erreur : {e}")
    except Exception as e:
            print(f"Erreur fichier non trouvé {path}")
            print(f"Erreur : {e}")
    return listDepartments


def loadTopicsFromFile(path: str, listTopics: list[DecreeTopic]) -> list[DecreeTopic]:
    try: 
        with open(path, encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')
            # Separate header from the other data of the csv
            header = next(reader)
            for row in reader:
                try:
                    tt = DecreeTopic(id=int(row[0]), label=row[1])
                    listTopics.append(tt)

                except Exception as e:
                    print(f"Erreur de parsing sujets, ligne ignorée : {row}")
                    print(f"Erreur : {e}")
    except Exception as e:
            print(f"Erreur fichier non trouvé {path}")
            print(f"Erreur : {e}")
    return listTopics


def loadDocTypesFromFile(path: str, listDocTypes: list[DocumentType]) -> list[DocumentType]:
    try: 
        with open(path, encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')
            # Separate header from the other data of the csv
            header = next(reader)
            for row in reader:
                try:
                    tt = DocumentType(id=int(row[0]), label=row[1])
                    listDocTypes.append(tt)

                except Exception as e:
                    print(
                        f"Erreur de parsing types de docs, ligne ignorée : {row}")
                    print(f"Erreur : {e}")
    except Exception as e:
            print(f"Erreur fichier non trouvé {path}")
            print(f"Erreur : {e}")
    return listDocTypes

def addTopic(top :DecreeTopic):
    basePath = settings.value(ROOT_KEY)
    fullPath = basePath + '/config/decreeTopics.csv'
    nId = updateIdFile('topic')
    top.id = nId
    try:
        with open(fullPath, 'a', encoding='utf-8', newline='') as file:
            writerCsv = csv.writer(file)
            writerCsv.writerow(top.toCsvLine())

    except Exception as e:
        print(f"Erreur de modification de fichier")
        print(f"Erreur : {e}")

def addCampaign(camp :Campaign): 
    basePath = settings.value(ROOT_KEY)
    fullPath = basePath + '/config/campaign.csv'
    try:
        nId = updateIdFile('campaign')
        camp.id = nId

        with open(fullPath, 'a', encoding='utf-8', newline='') as file:
            writerCsv = csv.writer(file)
            writerCsv.writerow(camp.toCsvLine())

    except Exception as e:
        print(f"Erreur de modification de fichier")
        print(f"Erreur : {e}")

def addTopicToCampaign(top: DecreeTopic, camp : Campaign):
    basePath = settings.value(ROOT_KEY)
    fullPath = basePath + '/config/campaign.csv'
    fileContent = []

    try:
        # read file and it content
        with open(fullPath, encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')
            # Get the header separately from the rest, to avoid cast error
            header = next(reader)
            for row in reader:
                # find the row corresponding to the campaign in the file
                if int(row[0]) == camp.id:
                    topList = list(map(int, row[2].split("-")))
                    # if the topic is not already in the list, add it
                    if top.id not in topList:
                        camp.topicList.append(top)
                    fileContent.append(camp.toCsvLine())
                else:
                    fileContent.append(row)

        # re-write the file content (updated)
        with open(fullPath, 'w', encoding='utf-8', newline='') as file:  # w clears all the file content
            writerCsv = csv.writer(file)
            # write the header
            writerCsv.writerow(header)
            writerCsv.writerows(fileContent)
    
    except Exception as e:
                print(f"Erreur de lecture de fichier {fullPath}")
                print(f"Erreur : {e}")

def updateIdFile(attr: str) -> int:
    # update decree data in csv file
    basePath = settings.value(ROOT_KEY)
    fullPath = basePath + '/config/lastId.csv'
    fileContent = []

    try: 
        # read file and its content
        with open(fullPath, encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')
            header = next(reader)
            for row in reader:
                if row[0] == attr:
                    nextId = int(row[1]) + 1
                    fileContent.append([attr, nextId])
                else:
                    fileContent.append(row)

        # re-write the file content (updated)
        with open(fullPath, 'w', encoding='utf-8', newline='') as file:  # w clears all the file content
            writerCsv = csv.writer(file)
            writerCsv.writerow(header)
            writerCsv.writerows(fileContent)

    except Exception as e:
                print(f"Erreur de lecture de fichier {fullPath}")
                print(f"Erreur : {e}")
    return nextId


def getFileName(arrete: Decree) -> str:
    dYear = arrete.publicationDate.year
    dMonth = arrete.publicationDate.month
    filename = arrete.department.number + "_" + \
        str(dYear) + "_" + str(dMonth) + "_RAA.csv"

    basePath = settings.value(ROOT_KEY)
    fullPath = basePath + "/prefectures/" + arrete.department.number + '/' + filename
    return fullPath

def getCampaignFromTopic(topic : DecreeTopic) -> list[Campaign]:
    listCampaigns = []
    try:
            basePath = settings.value(ROOT_KEY)
            fullPath = os.path.join(basePath, 'config/campaign.csv')
            # open file and read it
            with open(fullPath, encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=',')

                # Separate header from the other data of the csv
                header = next(reader)
                for row in reader:
                    decreeTopicIdList = list(map(int, row[2].split("-")))
                    # for each campaign, check if the searched topic matches
                    if topic.id in decreeTopicIdList : 
                        try:
                            cc = Campaign(
                                        id=int(row[0]), 
                                        label=row[1], 
                                        topicList = list(map(repository.getTopicById, map(int, row[2].split("-"))))
                                        )
                            listCampaigns.append(cc)

                        except Exception as e:
                            print(f"Erreur de parsing campagnes, ligne ignorée : {row}")
                            print(f"Erreur : {e}")

    except Exception as e:
            print(f"Erreur de lecture de fichier {fullPath}")
            print(f"Erreur : {e}")
            
    return listCampaigns