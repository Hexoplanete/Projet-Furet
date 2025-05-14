from furet.types.decree import *
import datetime
import os
import csv
from datetime import datetime
from furet import repository, settings

from PySide6 import QtCore

format = '%d/%m/%Y'
allDecreeList = []
campaignList = []
topicList = []
departmentList = []
docTypeList = []

ROOT_KEY = "repository.csv-root"
def setup():
    settings.setDefaultValue(ROOT_KEY, os.path.join(QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.AppDataLocation), 'database'))

    basePath = settings.value(ROOT_KEY)    
    # create folder 'prefectures' if the database doesn't exists
    if not os.path.exists(basePath):
        settings.setValue(ROOT_KEY, os.path.join(QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.AppDataLocation), 'database'))
        basePath = settings.value(ROOT_KEY)    
        os.makedirs(basePath, exist_ok=True)

    if not os.path.exists(os.path.join(basePath, 'prefectures')):
        os.makedirs(os.path.join(basePath, 'prefectures'))
    # create folder 'config' if the database doesn't exists
    if not os.path.exists(os.path.join(basePath, 'config')):
        os.makedirs(os.path.join(basePath, 'config'))

    # create departments csv file
    if not os.path.isfile(os.path.join(basePath, 'config/departments.csv')): 
        fileContent = [
            ['id','number','label'],
            [1,'01','Ain'],
            [2,'02','Aisne'],
            [3,'03','Allier'],
            [4,'04','Alpes-de-Haute-Provence'],
            [5,'05','Hautes-Alpes'],
            [6,'06','Alpes-Maritimes'],
            [7,'07','Ardèche'],
            [8,'08','Ardennes'],
            [9,'09','Ariège'],
            [10,'10','Aube'],
            [11,'11','Aude'],
            [12,'12','Aveyron'],
            [13,'13','Bouches-du-Rhône'],
            [14,'14','Calvados'],
            [15,'15','Cantal'],
            [16,'16','Charente'],
            [17,'17','Charente-Maritime'],
            [18,'18','Cher'],
            [19,'19','Corrèze'],
            [200,'2A','Corse-du-Sud'],
            [201,'2B','Haute-Corse'],
            [21,'21',"Côte-d'Or"],
            [22,'22',"Côtes-d'Armor"],
            [23,'23','Creuse'],
            [24,'24','Dordogne'],
            [25,'25','Doubs'],
            [26,'26','Drôme'],
            [27,'27','Eure'],
            [28,'28','Eure-et-Loir'],
            [29,'29','Finistère'],
            [30,'30','Gard'],
            [31,'31','Haute-Garonne'],
            [32,'32','Gers'],
            [33,'33','Gironde'],
            [34,'34','Hérault'],
            [35,'35','Ille-et-Vilaine'],
            [36,'36','Indre'],
            [37,'37','Indre-et-Loire'],
            [38,'38','Isère'],
            [39,'39','Jura'],
            [40,'40','Landes'],
            [41,'41','Loir-et-Cher'],
            [42,'42','Loire'],
            [43,'43','Haute-Loire'],
            [44,'44','Loire-Atlantique'],
            [45,'45','Loiret'],
            [46,'46','Lot'],
            [47,'47','Lot-et-Garonne'],
            [48,'48','Lozère'],
            [49,'49','Maine-et-Loire'],
            [50,'50','Manche'],
            [51,'51','Marne'],
            [52,'52','Haute-Marne'],
            [53,'53','Mayenne'],
            [54,'54','Meurthe-et-Moselle'],
            [55,'55','Meuse'],
            [56,'56','Morbihan'],
            [57,'57','Moselle'],
            [58,'58','Nièvre'],
            [59,'59','Nord'],
            [60,'60','Oise'],
            [61,'61','Orne'],
            [62,'62','Pas-de-Calais'],
            [63,'63','Puy-de-Dôme'],
            [64,'64','Pyrénées-Atlantiques'],
            [65,'65','Hautes-Pyrénées'],
            [66,'66','Pyrénées-Orientales'],
            [67,'67','Bas-Rhin'],
            [68,'68','Haut-Rhin'],
            [69,'69','Rhône'],
            [70,'70','Haute-Saône'],
            [71,'71','Saône-et-Loire'],
            [72,'72','Sarthe'],
            [73,'73','Savoie'],
            [74,'74','Haute-Savoie'],
            [75,'75','Paris'],
            [76,'76','Seine-Maritime'],
            [77,'77','Seine-et-Marne'],
            [78,'78','Yvelines'],
            [79,'79','Deux-Sèvres'],
            [80,'80','Somme'],
            [81,'81','Tarn'],
            [82,'82','Tarn-et-Garonne'],
            [83,'83','Var'],
            [84,'84','Vaucluse'],
            [85,'85','Vendée'],
            [86,'86','Vienne'],
            [87,'87','Haute-Vienne'],
            [88,'88','Vosges'],
            [89,'89','Yonne'],
            [90,'90','Territoire de Belfort'],
            [91,'91','Essonne'],
            [92,'92','Hauts-de-Seine'],
            [93,'93','Seine-Saint-Denis'],
            [94,'94','Val-de-Marne'],
            [95,95,"Val-d'Oise"],
            [971,'971','Guadeloupe'],
            [972,'972','Martinique'],
            [973,'973','Guyane'],
            [974,'974','La Réunion'],
            [976,'976','Mayotte']
        ]

        with open(os.path.join(basePath, 'config/departments.csv'), 'w', encoding='utf-8', newline='') as file:
            writerCsv = csv.writer(file)
            writerCsv.writerows(fileContent)

    # create document types csv file
    if not os.path.isfile(os.path.join(basePath, 'config/documentType.csv')):   
        fileContent = [
                    ['id', 'label'],
                    [1, 'Arrêté préfectoral'],
                    [2, 'Arrêté municipal'],
                    [3, 'Consultation publique']
                ]
        with open(os.path.join(basePath, 'config/documentType.csv'), 'w', encoding='utf-8', newline='') as file:
            writerCsv = csv.writer(file)
            writerCsv.writerows(fileContent)

    # créer les campagnes

    # create campaign csv file
    if not os.path.isfile(os.path.join(basePath, 'config/campaign.csv')):   
        fileContent = [
                        ['id','label','topicsId'],
                        [1,'Chasse',"1-2-3-4-5-6-7-8-9"],
                        [2,"Espèces protégées - grands prédateurs","13-14-15-16-17-18-19-20-21-22"],
                        [3,'Blaireau',"10-11-12-4"],
                        [4,'ESOD',"23-24-25-26-27-28-29-30-31-32-33-34-35-36-37-38-39-40-41-42-43-44"],
                        [5,'CDCFS',"8"]
                    ]
        with open(os.path.join(basePath, 'config/campaign.csv'), 'w', encoding='utf-8', newline='') as file:
            writerCsv = csv.writer(file)
            writerCsv.writerows(fileContent)

    # create decreeTopics csv file
    if not os.path.isfile(os.path.join(basePath, 'config/decreeTopics.csv')):  
        fileContent = [
                        ['id','label'],
                        [1,'chasse'],
                        [2,'cynégétique'],
                        [3,'gibier'],
                        [4,'vénerie'],
                        [5,'armes'],
                        [6,'tir'],
                        [7,'munition'],
                        [8,'CDCFS'],
                        [9,'SDGC'],
                        [10,'blaireau'],
                        [11,'déterrage'],
                        [12,'tuberculose bovine'],
                        [13,'loup'],
                        [14,'ours'],
                        [15,'lynx'],
                        [16,'chacal'],
                        [17,'prédation'],
                        [18,'prédateur'],
                        [29,'tirs de défense'],
                        [20,'tir de prélèvement'],
                        [21,'effarouchement'],
                        [22,'espèce animale protégée'],
                        [23,'louveterie'],
                        [24,'louvetier'],
                        [25,'piège'],
                        [26,'piégeage'],
                        [27,'destruction'],
                        [28,'battue'],
                        [29,'ESOD'],
                        [30,"espèce susceptible d'occasionner des dégâts"],
                        [31,'sanglier'],
                        [32,'lapin'],
                        [33,'pigeon'],
                        [34,'renard'],
                        [35,'corvidés'],
                        [36,'fouine'],
                        [37,'martre'],
                        [38,'belette'],
                        [39,'putois'],
                        [40,'corbeau freux'],
                        [41,'corneille noire'],
                        [42,'pie bavarde'],
                        [43,'geai'],
                        [44,'étourneau']
                    ]
        with open(os.path.join(basePath, 'config/decreeTopics.csv'), 'w', encoding='utf-8', newline='') as file:
            writerCsv = csv.writer(file)
            writerCsv.writerows(fileContent)

    # create last id csv file
    if not os.path.isfile(os.path.join(basePath, 'config/lastId.csv')):     
        fileContent = [
                        ['label', 'value'],
                        ['decree', 1],
                        ['campaigns',5],
                        ['topics',44]
                    ]
        with open(os.path.join(basePath, 'config/lastId.csv'), 'w', encoding='utf-8', newline='') as file:
            writerCsv = csv.writer(file)
            writerCsv.writerows(fileContent)

def readAllArretesFromFiles():
   #Separate function from setup because setup must be called before processing (information required for processing is retrieved during setup) and processing adds new decrees!
    allDecreeList.clear()
    basePath = settings.value(ROOT_KEY)
    for root, dirs, files in os.walk(basePath + '/prefectures/'):
        for filename in files:
            if filename.endswith(".csv"):
                filepath = os.path.join(root, filename)
                #mod_time = os.path.getmtime(filepath)  # timestamp de modification
                loadArretesFromFile(filepath,allDecreeList)

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
    
    nId = updateIdFile('decree')
    arrete.id = nId
    row = arrete.toCsvLine()
    file_exists = os.path.isfile(fullPath)  # bool

    directory = os.path.dirname(fullPath)
    os.makedirs(directory, exist_ok=True)

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
    readAllArretesFromFiles()


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
                        endPage=int(row[10]),
                        campaigns=list(map(repository.getCampaignById, map(int, row[11].split("-")))),
                        topics=list(map(repository.getTopicById, map(int, row[12].split("-")))),
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
    listCampaigns.clear()
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
    listTopics.clear()
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
    loadTopicsFromFile()

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
    loadCampaignsFromFile()

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
    loadCampaignsFromFile()

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