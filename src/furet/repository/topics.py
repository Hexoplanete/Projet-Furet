from furet.types.decree import *
import os
from furet import settings
from furet.repository import utils

topics: list[Topic] = []
maxId: int = 0

def getFilePath(): 
    return os.path.join(settings.value("repository.csv-root"), 'topics.csv')

def loadAllTopics():
    global topics, maxId
    path = getFilePath()

    if not os.path.isfile(path):
        topics = [
            Topic(id=1, label='chasse'),
            Topic(id=2, label='cynégétique'),
            Topic(id=3, label='gibier'),
            Topic(id=4, label='vénerie'),
            Topic(id=5, label='armes'),
            Topic(id=6, label='tir'),
            Topic(id=7, label='munition'),
            Topic(id=8, label='CDCFS'),
            Topic(id=9, label='SDGC'),
            Topic(id=10, label='blaireau'),
            Topic(id=11, label='déterrage'),
            Topic(id=12, label='tuberculose bovine'),
            Topic(id=13, label='loup'),
            Topic(id=14, label='ours'),
            Topic(id=15, label='lynx'),
            Topic(id=16, label='chacal'),
            Topic(id=17, label='prédation'),
            Topic(id=18, label='prédateur'),
            Topic(id=19, label='tirs de défense'),
            Topic(id=20, label='tir de prélèvement'),
            Topic(id=21, label='effarouchement'),
            Topic(id=22, label='espèce animale protégée'),
            Topic(id=23, label='louveterie'),
            Topic(id=24, label='louvetier'),
            Topic(id=25, label='piège'),
            Topic(id=26, label='piégeage'),
            Topic(id=27, label='destruction'),
            Topic(id=28, label='battue'),
            Topic(id=29, label='ESOD'),
            Topic(id=30, label="espèce susceptible d'occasionner des dégâts"),
            Topic(id=31, label='sanglier'),
            Topic(id=32, label='lapin'),
            Topic(id=33, label='pigeon'),
            Topic(id=34, label='renard'),
            Topic(id=35, label='corvidés'),
            Topic(id=36, label='fouine'),
            Topic(id=37, label='martre'),
            Topic(id=38, label='belette'),
            Topic(id=39, label='putois'),
            Topic(id=40, label='corbeau freux'),
            Topic(id=41, label='corneille noire'),
            Topic(id=42, label='pie bavarde'),
            Topic(id=43, label='geai'),
            Topic(id=44, label='étourneau'),
        ]
        saveTopicsToFile()
    else:
        topics = utils.loadFromCsv(path, Topic)

    maxId = max(maxId, topics[-1].id)


def getTopics():
    l = topics.copy()
    l.sort(key=lambda t: t.label.lower())
    return l



def addTopic(topic: Topic):
    global maxId
    maxId = maxId+1
    topic.id = maxId
    
    topics.append(topic)
    saveTopicsToFile()

def updateTopic(id: int, topic: Topic):
    topic.id = id
    for i in range(len(topics)):
        if topics[i].id == topic.id:
            topics[i] = topic
    saveTopicsToFile()


def saveTopicsToFile():
    utils.saveToCsv(getFilePath(), topics, Topic)
