from furet.repository import utils
from furet.types.decree import *
import os
import csv
from furet import repository, settings

campaigns: list[Campaign] = []
maxId: int = 0
headers = ['id', 'label', 'topicsId']

def getFilePath():
    return os.path.join(settings.value("repository.csv-root"), 'config/campaign.csv')

def loadAllCampaigns():
    global campaigns, maxId
    path = getFilePath()

    if not os.path.isfile(path):
        campaigns += [
            Campaign(id=1, label='Chasse', topicList=list(map(repository.getTopicById,[1,2,3,4,5,6,7,8,9]))),
            Campaign(id=2, label="Espèces protégées - grands prédateurs" , topicList=list(map(repository.getTopicById,[13,14,15,16,17,18,19,20,21,22]))),
            Campaign(id=3, label='Blaireau', topicList=list(map(repository.getTopicById,[10,11,12,4]))),
            Campaign(id=4, label='ESOD', topicList=list(map(repository.getTopicById,[23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44]))),
            Campaign(id=5, label='CDCFS', topicList=list(map(repository.getTopicById,[8]))),
        ]
        maxId = 5
        saveCampaignsToFile()
    
    campaigns.clear()
    try:
        with open(path, encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')

            header = next(reader)
            for row in reader:
                    campaigns.append(Campaign(
                        id=int(row[0]),
                        label=row[1],
                        topicList=list(map(repository.getTopicById, utils.splitIdList(row[2])))
                    ))
                    maxId = max(maxId, campaigns[-1].id)
    except Exception as e:
        if type(e) is not StopIteration:
            print(f"Erreur fichier non trouvé {path}")
            print(f"Erreur : {e}")
    return campaigns

def getCampaigns():
    return campaigns


def addCampaign(campaign: Campaign):
    global maxId
    maxId = maxId+1
    campaign.id = maxId

    campaigns.append(campaign)
    saveCampaignsToFile()

def updateCampaign(id: int, campaign: Campaign):
    campaign.id = id
    for i in range(len(campaigns)):
        if campaigns[i].id == campaign.id:
            campaigns[i] = campaign
    saveCampaignsToFile()


def saveCampaignsToFile():
    try:
        with open(getFilePath(), 'w', encoding='utf-8', newline='') as file:
            writerCsv = csv.writer(file)
            writerCsv.writerow(headers)
            for c in campaigns:
                writerCsv.writerow(c.toCsvLine())

    except Exception as e:
        print(f"Erreur de modification de fichier")
        print(f"Erreur : {e}")


def getCampaignFromTopic(topic: DecreeTopic) -> list[Campaign]:
    listCampaigns = []
    for c in campaigns:
        if topic in c.topicList:
            listCampaigns.append(c)

    return listCampaigns