import csv
from datetime import datetime
from datetime import date

path = "./Database/57/"

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

    def __str__(self):
        return f"Arrêté n°: {self.numArrete}, pages: {self.pages}"

if __name__ == "__main__":

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
