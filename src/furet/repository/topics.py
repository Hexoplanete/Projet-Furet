from furet.types.decree import *
import os
import csv
from furet import settings

topics: list[DecreeTopic] = []
maxId: int = 0
headers = ['id', 'label']

def getFilePath(): 
    return os.path.join(settings.value("repository.csv-root"), 'config/topic.csv')

def loadAllTopics():
    global topics, maxId
    path = getFilePath()

    if not os.path.isfile(path):
        topics += [
            DecreeTopic(id=1, label='chasse'),
            DecreeTopic(id=2, label='cynégétique'),
            DecreeTopic(id=3, label='gibier'),
            DecreeTopic(id=4, label='vénerie'),
            DecreeTopic(id=5, label='armes'),
            DecreeTopic(id=6, label='tir'),
            DecreeTopic(id=7, label='munition'),
            DecreeTopic(id=8, label='CDCFS'),
            DecreeTopic(id=9, label='SDGC'),
            DecreeTopic(id=10, label='blaireau'),
            DecreeTopic(id=11, label='déterrage'),
            DecreeTopic(id=12, label='tuberculose bovine'),
            DecreeTopic(id=13, label='loup'),
            DecreeTopic(id=14, label='ours'),
            DecreeTopic(id=15, label='lynx'),
            DecreeTopic(id=16, label='chacal'),
            DecreeTopic(id=17, label='prédation'),
            DecreeTopic(id=18, label='prédateur'),
            DecreeTopic(id=19, label='tirs de défense'),
            DecreeTopic(id=20, label='tir de prélèvement'),
            DecreeTopic(id=21, label='effarouchement'),
            DecreeTopic(id=22, label='espèce animale protégée'),
            DecreeTopic(id=23, label='louveterie'),
            DecreeTopic(id=24, label='louvetier'),
            DecreeTopic(id=25, label='piège'),
            DecreeTopic(id=26, label='piégeage'),
            DecreeTopic(id=27, label='destruction'),
            DecreeTopic(id=28, label='battue'),
            DecreeTopic(id=29, label='ESOD'),
            DecreeTopic(id=30, label="espèce susceptible d'occasionner des dégâts"),
            DecreeTopic(id=31, label='sanglier'),
            DecreeTopic(id=32, label='lapin'),
            DecreeTopic(id=33, label='pigeon'),
            DecreeTopic(id=34, label='renard'),
            DecreeTopic(id=35, label='corvidés'),
            DecreeTopic(id=36, label='fouine'),
            DecreeTopic(id=37, label='martre'),
            DecreeTopic(id=38, label='belette'),
            DecreeTopic(id=39, label='putois'),
            DecreeTopic(id=40, label='corbeau freux'),
            DecreeTopic(id=41, label='corneille noire'),
            DecreeTopic(id=42, label='pie bavarde'),
            DecreeTopic(id=43, label='geai'),
            DecreeTopic(id=44, label='étourneau'),
        ]
        maxId = max(maxId, topics[-1].id)

        saveTopicsToFile()
        return
    
    topics.clear()
    try:
        with open(path, encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')

            header = next(reader)

            for row in reader:
                topics.append(DecreeTopic(id=int(row[0]),label=row[1],))

    except Exception as e:
        if type(e) is not StopIteration:
            print(f"Erreur fichier non trouvé {path}")
            print(f"Erreur : {e}")
    return topics

def getTopics():
    l = topics.copy()
    l.sort(key=lambda t: t.label.lower())
    return l



def addTopic(topic: DecreeTopic):
    global maxId
    maxId = maxId+1
    topic.id = maxId
    
    topics.append(topic)
    saveTopicsToFile()

def updateTopic(id: int, topic: DecreeTopic):
    topic.id = id
    for i in range(len(topics)):
        if topics[i].id == topic.id:
            topics[i] = topic
    saveTopicsToFile()


def saveTopicsToFile():
    try:
        with open(getFilePath(), 'w', encoding='utf-8', newline='') as file:
            writerCsv = csv.writer(file)
            writerCsv.writerow(headers)
            for d in topics:
                writerCsv.writerow(d.toCsvLine())

    except Exception as e:
        print(f"Erreur de modification de fichier")
        print(f"Erreur : {e}")
