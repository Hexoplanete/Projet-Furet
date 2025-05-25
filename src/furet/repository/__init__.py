import os
from furet import settings
from furet.repository import csvdb
from furet.types.department import *
from furet.types.decree import *
from PySide6 import QtCore
from dataclasses import dataclass

def setup():
    settings.setDefaultValue("repository.csv-root", os.path.join(QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.AppDataLocation), 'database'))
    csvdb.connect(settings.value("repository.csv-root"))

# DECREES


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
        if self.after is not None and (decree.publicationDate is None or decree.publicationDate < self.after):
            return False
        if self.before is not None and (decree.publicationDate is None or decree.publicationDate > self.before):
            return False
        if len(self.departments) > 0 and (decree.department is None or not decree.department.id in self.departments):
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


def getDecrees(filters: DecreeFilters | None = None) -> list[Decree]:
    return csvdb.fetch(Decree)


def getDecreeById(id: int) -> Decree | None:
    return csvdb.fetchById(Decree, id)


def updateDecree(id: int, decree: Decree):
    decree.id = id
    return csvdb.update(decree)


def addDecree(decree: Decree):
    csvdb.insert(decree)


def addDecrees(decrees: list[Decree]):
    for d in decrees:
        addDecree(d)

# DEPARTMENTS


def getDepartments() -> list[Department]:
    return csvdb.fetch(Department)


def getDepartmentById(id: int) -> Department | None:
    return csvdb.fetchById(Department, id)


# DOCTYPES


def getDocumentTypes() -> list[DocumentType]:
    return csvdb.fetch(DocumentType)


def getDocumentTypeById(id: int) -> DocumentType | None:
    return csvdb.fetchById(DocumentType, id)

# CAMPAIGNS


def getCampaigns() -> list[Campaign]:
    return csvdb.fetch(Campaign)


def getCampaignById(id: int) -> Campaign | None:
    return csvdb.fetchById(Campaign, id)


def updateCampaign(id: int, campaign: Campaign):
    campaign.id = id
    csvdb.update(campaign)


def addCampaign(campaign: Campaign):
    csvdb.insert(campaign)


def getCampaignFromTopic(topic: Topic) -> list[Campaign]:
    listCampaigns = []
    for c in getCampaigns():
        if topic in c.topicList:
            listCampaigns.append(c)
    return listCampaigns


# TOPICS

def getTopics() -> list[Topic]:
    return csvdb.fetch(Topic)


def getTopicById(id: int) -> Topic | None:
    return csvdb.fetchById(Topic, id)


def updateTopic(id: int, topic: Topic):
    topic.id = id
    csvdb.update(topic)


def addTopic(topic: Topic):
    csvdb.insert(topic)
