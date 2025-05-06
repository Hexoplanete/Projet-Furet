import csv
path = "./Database/57/"

"""
"""

class Arrete:
    def __init__(self, typeDocument, campagneAspas, departement, numArrete, titreArrete, dateSignatureArrete, numRaa, datePubliRaa, pages, statutTraitement, commentaire):
        self.typeDocument = typeDocument
        self.campagneAspas = campagneAspas
        self.departement = departement
        self.numArrete = numArrete
        self.titreArrete = titreArrete
        self.dateSignatureArrete = dateSignatureArrete
        self.numRaa = numRaa
        self.datePubliRaa = datePubliRaa
        self.pages = pages
        self.statutTraitement = statutTraitement
        self.commentaire = commentaire

    def __str__(self):
        return f"Arrêté n°: {self.numArrete}, pages: {self.pages}"

if __name__ == "__main__":

#lecture d'un fichier 
    with open(path + '57_2025_04_RAA.csv', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')

        l = []
        for row in reader:
            print(row)
            #aa = Arrete("Alice", 30)
            #print(aa)

            #l.append(aa)
        #filtrer

