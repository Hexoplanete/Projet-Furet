from furet.traitement.ocr import *
from furet.traitement.separation_avec_sommaire  import *
from furet.traitement.getKeyWords import *
from furet.traitement.correspondance_nom_num_depart import *
from furet.types.raa import RAA
from furet.types.decree import *
from furet.repository import * 

from database.config import * # Contient les derniers IDs attribués

import subprocess
import os
import json
import requests
import datetime

class Traitement:

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "fr-FR,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        }

        self.path_traitement = os.path.join(os.getcwd(), "src", "furet", "traitement")
    
    def downloadPDF(self, url, output_path):
        """
            Download a PDF file from the given URL and put it in the output directory.

            :param url: URL of the PDF file.
        """
        try:
            response = requests.get(url, stream=True, headers=self.headers)
            response.raise_for_status()
            
            filename = os.path.join(output_path)
            if not filename.endswith('.pdf'):
                filename += ".pdf"
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"Downloaded: {filename}")
        except requests.RequestException as e:
            print(f"Failed to download {url}: {e}")

    def readLinkFile(self):
        """
        Reads the link file and returns the list of links.
        """
        rootDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
        linkFile = os.path.join(rootDir, "src", "furet", "crawler", "resultCrawler.json")
        
        if os.path.exists(linkFile):
            with open(linkFile, 'r') as f:
                data = json.load(f)
            return data["links"]
        else:
            return []
    
    def startTraitement(self):
        """ 
            Function that is Input to the Processing Framework
            Retrieves information provided by the crawler for each RAA crawled : url, datePublication, departement (Creates a corresponding RAA object)
            Downloads the RAA from the URL
            Calls processing_RAA(...) -> Processes the RAA
        """
        # List of dictionaries representing RAAs (retrieved by the crawler)
        liste_dict_RAA = self.readLinkFile()

        for el in liste_dict_RAA:

            raa_url = el["link"]
            raa_datePublication = datetime.datetime.strptime(el["datePublication"], "%d/%m/%Y")
            raa_departement_label = el["department"]

            departementNumber = int(departements_label_to_code[raa_departement_label])
            departement = getDepartmentById(departementNumber)

            # Creates a RAA object containing information retrieved by the crawler
            raa = RAA(
                department=departement,
                publicationDate = raa_datePublication,
                link=raa_url,
                number="Non déterminé", # It's going to be in the characteristic extraction section
            )

            rootDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
            raa_save_path = os.path.join(rootDir, "src", "furet", "traitement", "input_RAA",f"{os.path.basename(raa_url)}")
            self.downloadPDF(raa_url, raa_save_path)
            self.traitement_RAA(raa_save_path, raa)

    def traitement_RAA(self, input_path, raa):
        """ 
        Input : PDF corresponding to an RAA (RAA which was just downloaded from the links obtained by the crawler)

        Reduce PDF quality using magick → Generates a new PDF in -> "output/after_magick/"

        Perform OCR on the input PDF to generate a new "OCR-processed" PDF, meaning it's converted to text format → Generates a new OCR-processed PDF -> "output/after_ocr/"

        Split the RAA into decrees → Generates one PDF per decree from the RAA -> "output/after_split/{RAA_Name}/"

        Assign keywords to a decree

        Ouput → a csv file for each decree -> "database/prefectures/{code_department}/{code_department}_{month}.csv"
        """

        ## We reduce the quality of the PDF to remove the error "BOMB DOS ATTACK SIZE LIMIT"
        directory_apres_magick = os.path.join(self.path_traitement, "output", "apres_magick")
        os.makedirs(directory_apres_magick, exist_ok=True)
        path_apres_magick = os.path.join(directory_apres_magick, os.path.basename(input_path))

        commande = [
        "magick",
        "-density", "300",
        f"{input_path}",
        "-resize", "100%",
        "-quality", "85",
        path_apres_magick
        ]

        print("Start magick execution")
        subprocess.run(commande, check=True)
        print("End magick execution")

        print("--------------------------------")

        directory_apres_ocr = os.path.join(self.path_traitement, "output", "apres_ocr")
        print(directory_apres_ocr)
        os.makedirs(directory_apres_ocr, exist_ok=True)
        path_apres_ocr = os.path.join(directory_apres_ocr, os.path.basename(input_path))

        print("Start ocr execution")
        main_ocr(path_apres_magick,path_apres_ocr)
        print("End ocr execution")
        
        print("--------------------------------")

        print("Start separation execution")
        basename_RAA = os.path.basename(input_path).replace(".pdf","")

        directory_apres_separation = os.path.join(self.path_traitement, "output", "apres_separation", basename_RAA)
        os.makedirs(directory_apres_separation, exist_ok=True)
        path_apres_separation = os.path.join(directory_apres_separation, os.path.basename(input_path))

        liste_chemin_objetDecree = main_separation(path_apres_ocr, directory_apres_separation, raa)    

        print("End separation execution")

        # TO DO Extraction Caractéristique

        print("Start execution of attribution keywords")

        directory_apres_mot_clef = os.path.join(self.path_traitement, "output", "apres_mot_cle", basename_RAA)
        os.makedirs(directory_apres_mot_clef, exist_ok=True)
        
        for i in range (len(liste_chemin_objetDecree)):

            object_decree = liste_chemin_objetDecree[i][0]
            path_arrete = liste_chemin_objetDecree[i][1]

            dic = self.getDictLabelToId()
            listeKeyWords = list(dic.keys())

            path_apres_mot_clef = os.path.join(directory_apres_mot_clef, f"{os.path.basename(path_arrete).replace('.pdf','')}.txt")
            dic_key_words = getKeyWords(path_arrete, path_apres_mot_clef.replace(".txt",""), listeKeyWords) 
            
            liste_decree_topic = []

            for label, id in dic_key_words.items():
                topic = DecreeTopic(id=dic[label], label=label)
                liste_decree_topic.append(topic)

            object_decree.topic = liste_decree_topic

            # Check if the decree is really interesting
            # For example, if there is only "armes" the bylaw is VERY unlikely to be of interest.
            bool_isArreteProbablyFalsePositive = self.isArreteProbablyFalsePositive(liste_decree_topic)
            
            if(not bool_isArreteProbablyFalsePositive):
                addArreteToFile(object_decree) # Enregistre les informations de l'arreté sous format CSV
            
        print("End execution of attribution keywords")

    def getDictLabelToId(self):
            liste_decree_topics = getTopics()
            return {topic.label: topic.id for topic in liste_decree_topics}
    
    def isArreteProbablyFalsePositive(self, liste_decree_topic):
        
        liste_label = []
        liste_keyWords_not_interesting_alone = ["armes", "destruction"]
        
        for decreeTopic in liste_decree_topic:
            liste_label.append(decreeTopic.label)

        for el in liste_keyWords_not_interesting_alone:
            if(el==liste_label):
                return True
            
        return False


            