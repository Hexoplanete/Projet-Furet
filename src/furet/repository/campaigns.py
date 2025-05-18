from furet import repository
from furet.types.decree import *
import os
from furet import settings
from furet.repository import utils

campaigns: list[Campaign] = []
maxId: int = 0


def getFilePath():
    return os.path.join(settings.value("repository.csv-root"), 'campaigns.csv')


def loadAllCampaigns():
    global campaigns, maxId
    path = getFilePath()

    if not os.path.isfile(path):
        campaigns = [
            Campaign(id=1, label='Chasse', topicList=list(map(repository.getTopicById, [1, 2, 3, 4, 5, 6, 7, 8, 9]))),
            Campaign(id=2, label="Espèces protégées - grands prédateurs", topicList=list(map(repository.getTopicById, [13, 14, 15, 16, 17, 18, 19, 20, 21, 22]))),
            Campaign(id=3, label='Blaireau', topicList=list(map(repository.getTopicById, [10, 11, 12, 4]))),
            Campaign(id=4, label='ESOD', topicList=list(map(repository.getTopicById, [23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44]))),
            Campaign(id=5, label='CDCFS', topicList=list(map(repository.getTopicById, [8]))),
        ]
        saveCampaignsToFile()
    else:
        campaigns = utils.loadFromCsv(path, Campaign)

    maxId = max(maxId, campaigns[-1].id)


def getCampaigns():
    l = campaigns.copy()
    l.sort(key=lambda c: c.label.lower())
    return l


def getCampaignFromTopic(topic: DecreeTopic) -> list[Campaign]:
    listCampaigns = []
    for c in campaigns:
        if topic in c.topicList:
            listCampaigns.append(c)

    return listCampaigns


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
    utils.saveToCsv(getFilePath(), campaigns, Campaign)
