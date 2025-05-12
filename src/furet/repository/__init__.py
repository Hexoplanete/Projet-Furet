from furet.types.department import *
from furet.types.decree import *

from . import csvdata


def setup():
    csvdata.setup()
    csvdata.load()


def getDecrees() -> list[Decree]:
    return csvdata.allDecreeList

def getDecrees() -> list[Decree]:
    return csvdata.allDecreeList


def getDecreeById(id: int) -> Decree:
    return _findByField(getDecrees(), id)


def updateDecree(id: int, decree: Decree):
    return csvdata.updateDecree(id, decree)


def getDepartments() -> list[Department]:
    return csvdata.departmentList


def getDepartmentById(id: int) -> Department:
    return _findByField(getDepartments(), id)


def getDocumentTypes() -> list[DocumentType]:
    return csvdata.docTypeList


def getDocumentTypeById(id: int) -> DocumentType:
    return _findByField(getDocumentTypes(), id)


def getCampaigns() -> list[Campaign]:
    return csvdata.campaignList


def getCampaignById(id: int) -> Campaign:
    return _findByField(getCampaigns(), id)


def getCampaignIdByLabel(label: str) -> Campaign:
    return _findByField(getCampaigns(), label)


def getTopics() -> list[DecreeTopic]:
    return csvdata.topicList


def getTopicById(id: int) -> DecreeTopic:
    return _findByField(getTopics(), id)


def _findByField(collection, value, field: str = "id"):
    for d in collection:
        if getattr(d, field) == value:
            return d
    return None
