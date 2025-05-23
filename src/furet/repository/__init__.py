import os
from furet import settings
from furet.types.department import *
from furet.types.decree import *
from PySide6 import QtCore

from . import campaigns, decrees, departments, docTypes, topics, utils


def setup():
    settings.setDefaultValue("repository.csv-root", os.path.join(QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.AppDataLocation), 'database'))

    utils.addSerializer(Campaign, lambda c: utils.serialize(c.id), lambda s, t: getCampaignById(utils.deserialize(s, int)))
    utils.addSerializer(Decree, lambda c: utils.serialize(c.id), lambda s, t: getDecreeById(utils.deserialize(s, int)))
    utils.addSerializer(Department, lambda c: utils.serialize(c.id), lambda s, t: getDepartmentById(utils.deserialize(s, int)))
    utils.addSerializer(DocumentType, lambda c: utils.serialize(c.id), lambda s, t: getDocumentTypeById(utils.deserialize(s, int)))
    utils.addSerializer(DecreeTopic, lambda c: utils.serialize(c.id), lambda s, t: getTopicById(utils.deserialize(s, int)))

    topics.loadAllTopics()
    departments.loadAllDepartments()
    docTypes.loadAllDocTypes()
    campaigns.loadAllCampaigns()
    decrees.loadAllDecrees()


# DECREES
def getDecrees(filters: decrees.DecreeFilters | None = None) -> list[Decree]:
    return decrees.getDecrees(filters)


def getDecreeById(id: int) -> Decree:
    return _findByField(decrees.getDecrees(), id)

def updateDecree(id: int, decree: Decree):
    return decrees.updateDecree(id, decree)

def addDecree(decree: Decree):
    return decrees.addDecree(decree)

def addDecrees(decreesList: list[Decree]):
    return decrees.addDecrees(decreesList)

# DEPARTMENTS

def getDepartments() -> list[Department]:
    return departments.getDepartments()


def getDepartmentById(id: int) -> Department:
    return _findByField(getDepartments(), id)

# DOCTYPES

def getDocumentTypes() -> list[DocumentType]:
    return docTypes.getDocTypes()


def getDocumentTypeById(id: int) -> DocumentType:
    return _findByField(getDocumentTypes(), id)

# CAMPAIGNS

def getCampaigns() -> list[Campaign]:
    return campaigns.getCampaigns()


def getCampaignById(id: int) -> Campaign:
    return _findByField(campaigns.getCampaigns(), id)


def getCampaignIdByLabel(label: str) -> Campaign:
    return _findByField(campaigns.getCampaigns(), label)


def updateCampaign(id: int, campaign: Campaign):
    return campaigns.updateCampaign(id, campaign)


def addCampaign(campaign: Campaign):
    return campaigns.addCampaign(campaign)

def getCampaignFromTopic(topic: DecreeTopic) -> list[Campaign]:
    return campaigns.getCampaignFromTopic(topic)


# TOPICS

def getTopics() -> list[DecreeTopic]:
    return topics.getTopics()


def getTopicById(id: int) -> DecreeTopic:
    return _findByField(getTopics(), id)


def updateTopic(id: int, topic: DecreeTopic):
    return topics.updateTopic(id, topic)


def addTopic(topic: DecreeTopic):
    return topics.addTopic(topic)


def _findByField(collection, value, field: str = "id"):
    for d in collection:
        if getattr(d, field) == value:
            return d
    return None

def getDecreesWithEmptyLink() -> list[Decree]:
    return [
        decree for decree in getDecrees()
        if decree.link == ""
    ]