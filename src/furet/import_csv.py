import csv
import os

from datetime import datetime
from datetime import date

format = '%d/%m/%Y'
path = "./database/"

"""
"""

class Arrete:
    def __init__(self, typeDocument, campagneAspas, departement, numArrete, titreArrete, dateSignatureArrete, numRaa, datePubliRaa, url, pages, statutTraitement, commentaire):
        self.typeDocument = typeDocument
        self.campagneAspas = campagneAspas
        self.departement = departement
        self.numArrete = numArrete
        self.titreArrete = titreArrete
        self.dateSignatureArrete = datetime.strptime(dateSignatureArrete, format).date()
        self.numRaa = numRaa
        self.datePubliRaa = datetime.strptime(datePubliRaa, format).date()
        self.url = url
        self.pages = pages
        self.statutTraitement = statutTraitement
        self.commentaire = commentaire

    def __str__(self):  #for debug
        return f"Arrêté n°: {self.numArrete}, pages: {self.pages}"
    
    def toCsvLine(self):
        return [self.typeDocument, self.campagneAspas, self.departement, self.numArrete,self.titreArrete, self.dateSignatureArrete, self.numRaa, self.datePubliRaa, self.url, self.pages, self.statutTraitement, self.commentaire]


def addArreteToFile(arrete):
    #recuperer l'annee et le mois
    annee = arrete.datePubliRaa.year
    mois = arrete.datePubliRaa.month
    nom = arrete.departement + "_" + str(annee) + "_" + str(mois) + "_RAA.csv"
    
    full_path = path + arrete.departement + '/' + nom
    headers = ['Type de document', 'Campagne Aspas concernée', 'Département', "Numéro de l'arrêté", "Titre de l'arrêté", "Date de signature de l'arrêté", 'Numéro du RAA', 'Date de publication du RAA', 'URL du RAA', 'Pages concernées ', 'Statut de traitement', 'Commentaire']
    row = arrete.toCsvLine()
    file_exists = os.path.isfile(full_path) #bool

    with open(full_path, 'a', encoding='utf-8', newline='') as file:
        writerCsv = csv.writer(file)
        # if the file is freshly created, we need to insert the column names at the beginning
        if not file_exists:
            writerCsv.writerow(headers) 
        # insert the line with the arrete
        writerCsv.writerow(row)  

if __name__ == "__main__":

    # -----------------save Arretes into database-------------------------------------------------------------
    # example
    mockA = Arrete("Arrêté préfectoral", "chasse", "57", "2025-DDT-SERAF-UFC n°17", "Titre vreeument long", "07/05/2025", "38-2023-010", "10/05/2025", "http://url/blablabla.com", "14-16", "à traiter", "")
    #print(mockA)
    addArreteToFile(mockA)





#lecture d'un fichier 
    with open(path + '57_2025_04_RAA.csv', encoding='utf-8') as file:

        reader = csv.reader(file, delimiter=',')

        # On recupere le header separément du reste des lignes sinon ca pose probleme pour le cast
        header = next(reader)

        l = []
        for row in reader:
            try: 
                aa = Arrete(
                    row[0], row[1], row[2], row[3], row[4], row[5], 
                    row[6], row[7], row[8], row[9], row[10], row[11]
                )
                
                l.append(aa)
    
            except Exception as e:
                print(f"Erreur de parsing, ligne ignorée : {row}")
                print(f"Erreur : {e}")
