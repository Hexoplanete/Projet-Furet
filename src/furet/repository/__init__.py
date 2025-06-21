from datetime import date
import logging
from furet import settings
from furet.configs import RepositoryConfig
from furet.repository import csvdb
from furet.models.raa import Department
from furet.models.decree import DocumentType, Decree
from furet.models.campaign import Campaign, Topic
from furet.models.raa import RAA
from dataclasses import dataclass, field

logger = logging.getLogger("repository")

def setup():
    logger.info("Connecting to DB...")
    settings.setDefaultConfig(RepositoryConfig)
    csvdb.connect(settings.config(RepositoryConfig).csvRoot)


# RAAS


def getRaas() -> list[RAA]:
    return sorted(csvdb.fetch(RAA), key=lambda r: r.publicationDate or date(1900,1,1))


def getRaaById(id: int) -> RAA | None:
    return csvdb.fetchById(RAA, id)


def updateRaa(id: int, raa: RAA):
    raa.id = id
    return csvdb.update(raa)


def addRaa(raa: RAA):
    csvdb.insert(raa)


def addRaas(raas: list[RAA]):
    for d in raas:
        addRaa(d)

def alreadyImported(fileHash: str) -> bool:
    for raa in csvdb.fetch(RAA):
        if raa.fileHash == fileHash:
            return True
    return False

def getRaaByHash(fileHash: str) -> RAA | None:
    for raa in csvdb.fetch(RAA):
        if raa.fileHash == fileHash:
            return raa
    return None

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
        if self.after is not None and (decree.raa.publicationDate is None or decree.raa.publicationDate < self.after):
            return False
        if self.before is not None and (decree.raa.publicationDate is None or decree.raa.publicationDate > self.before):
            return False
        if len(self.departments) > 0 and (decree.raa.department is None or not decree.raa.department.id in self.departments):
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
    decrees = csvdb.fetch(Decree)
    return decrees if filters is None else list(filter(lambda d: filters.fitFilters(d), decrees))


def getDecreeById(id: int) -> Decree | None:
    return csvdb.fetchById(Decree, id)

def getDecreesByRaa(raaId: int) -> list[Decree]:
    return [d for d in csvdb.fetch(Decree) if d.raa.id == raaId]

def updateDecree(id: int, decree: Decree):
    decree.id = id
    return csvdb.update(decree)


def addDecree(decree: Decree | list[Decree]):
    csvdb.insert(decree)


# DEPARTMENTS


def getDepartments() -> list[Department]:
    return sorted(csvdb.fetch(Department), key=lambda i: i.id)


def getDepartmentById(id: int) -> Department | None:
    return csvdb.fetchById(Department, id)


# DOCTYPES


def getDocumentTypes() -> list[DocumentType]:
    return sorted(csvdb.fetch(DocumentType), key=lambda i: i.label)


def getDocumentTypeById(id: int) -> DocumentType | None:
    return csvdb.fetchById(DocumentType, id)

# CAMPAIGNS


def getCampaigns() -> list[Campaign]:
    return sorted(csvdb.fetch(Campaign), key=lambda i: i.label)


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
        if topic in c.topics:
            listCampaigns.append(c)
    return listCampaigns


# TOPICS

def getTopics() -> list[Topic]:
    return sorted(csvdb.fetch(Topic), key=lambda i:i.label)


def getTopicById(id: int) -> Topic | None:
    return csvdb.fetchById(Topic, id)


def updateTopic(id: int, topic: Topic):
    topic.id = id
    csvdb.update(topic)


def addTopic(topic: Topic):
    csvdb.insert(topic)
