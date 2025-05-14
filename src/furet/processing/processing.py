from furet.processing.ocr import *
from furet.processing.separation  import *
from furet.processing.getKeyWords import *
from furet.processing.correspondenceNameNumberDepartment import *
from furet.types.raa import RAA
from furet.types.decree import *

import subprocess
import os
import json
import requests
import datetime

class Processing:

    def __init__(self, pdfDirectory_path, outputProcessingSteps_path):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "fr-FR,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        }

        # Folder where the RAW PDFs of the downloaded RAA will be stored (those whose links are obtained with the craxwler which are therefore the PDFs directly available on the prefecture websites)
        self.pdfDirectory_path = pdfDirectory_path
        
        # Output folder where there are the outputs of each of the stages of the processing part
        self.outputProcessingSteps_path = outputProcessingSteps_path

        # Folder of processing directory
        self.pathTraitement = os.path.join(os.getcwd(), "src", "furet", "processing")
    
    def downloadPDF(self, url, outputPath):
        """
            Download a PDF file from the given URL and put it in the output directory.

            :param url: URL of the PDF file.
        """
        try:
            response = requests.get(url, stream=True, headers=self.headers)
            response.raise_for_status()
            
            fileName = os.path.join(outputPath)
            if not fileName.endswith('.pdf'):
                fileName += ".pdf"
            with open(fileName, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"Downloaded: {fileName}")
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
        listeDictRAA = self.readLinkFile()

        for el in listeDictRAA:

            raaUrl = el["link"]
            raaDatePublication = datetime.datetime.strptime(el["datePublication"], "%d/%m/%Y")
            raaDepartementLabel = el["department"]

            departementNumber = int(departementsLabelToCode[raaDepartementLabel])
            departement = getDepartmentById(departementNumber)

            # Creates a RAA object containing information retrieved by the crawler
            raa = RAA(
                department=departement,
                publicationDate = raaDatePublication,
                link=raaUrl,
                number="Non déterminé", # It's going to be in the characteristic extraction section
            )

            rootDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
            raaSavePath = os.path.join(rootDir, "src", "furet", "processing", "input_RAA",f"{os.path.basename(raaUrl)}")
            self.downloadPDF(raaUrl, raaSavePath)
            self.processingRAA(raaSavePath, raa)

    def processingRAA(self, inputPath, raa):
        """ 
        Input : PDF corresponding to an RAA (RAA which was just downloaded from the links obtained by the crawler)

        Reduce PDF quality using magick → Generates a new PDF in -> "output/after_magick/"

        Perform OCR on the input PDF to generate a new "OCR-processed" PDF, meaning it's converted to text format → Generates a new OCR-processed PDF -> "output/after_ocr/"

        Split the RAA into decrees → Generates one PDF per decree from the RAA -> "output/after_split/{RAA_Name}/"

        Assign keywords to a decree

        Ouput → a csv file for each decree -> "database/prefectures/{code_department}/{code_department}_{month}.csv"
        """

        ## We reduce the quality of the PDF to remove the error "BOMB DOS ATTACK SIZE LIMIT"
        directoryApresMagick = os.path.join(self.pathTraitement, "output", "apres_magick")
        os.makedirs(directoryApresMagick, exist_ok=True)
        pathApresMagick = os.path.join(directoryApresMagick, os.path.basename(inputPath))

        commande = [
        "magick",
        "-density", "300",
        f"{inputPath}",
        "-resize", "100%",
        "-quality", "85",
        pathApresMagick
        ]

        print("Start magick execution")
        subprocess.run(commande, check=True)
        print("End magick execution")

        print("--------------------------------")

        directoryApresOcr = os.path.join(self.pathTraitement, "output", "apres_ocr")
        print(directoryApresOcr)
        os.makedirs(directoryApresOcr, exist_ok=True)
        pathApresOcr = os.path.join(directoryApresOcr, os.path.basename(inputPath))

        print("Start ocr execution")
        mainOcr(pathApresMagick,pathApresOcr)
        print("End ocr execution")
        
        print("--------------------------------")

        print("Start separation execution")
        basenameRAA = os.path.basename(inputPath).replace(".pdf","")

        directoryApresSeparation = os.path.join(self.pathTraitement, "output", "apres_separation", basenameRAA)
        os.makedirs(directoryApresSeparation, exist_ok=True)
        pathApresSeparation = os.path.join(directoryApresSeparation, os.path.basename(inputPath))

        print("Start separation execution")
        listeCheminObjetDecree = mainSeparation(pathApresOcr, directoryApresSeparation, raa)    
        print("End separation execution")

        print("--------------------------------")

        directoryApresMotClef = os.path.join(self.pathTraitement, "output", "apres_mot_cle", basenameRAA)
        os.makedirs(directoryApresMotClef, exist_ok=True)

        print("Start execution of attribution keywords")
        
        for i in range (len(listeCheminObjetDecree)):

            objectDecree = listeCheminObjetDecree[i][0]
            pathArrete = listeCheminObjetDecree[i][1]

            dic = self.getDictLabelToId() ; listeKeyWords = list(dic.keys())

            pathApresMotClef = os.path.join(directoryApresMotClef, f"{os.path.basename(pathArrete).replace('.pdf','')}.txt")
            dicKeyWords = getKeyWords(pathArrete, pathApresMotClef.replace(".txt",""), listeKeyWords) 
            
            # We create a list containing a list of DecreeTopics (KeyWords) that match the decree
            listeDecreeTopic = []

            for label, id in dicKeyWords.items():
                topic = DecreeTopic(id=dic[label], label=label)
                listeDecreeTopic.append(topic)

            objectDecree.topics = listeDecreeTopic

            # Check if the decree is really interesting
            # For example, if there is only "armes" the bylaw is VERY unlikely to be of interest.
            boolIsArreteProbablyFalsePositive = self.isArreteProbablyFalsePositive(listeDecreeTopic)
            
            # Saves decree information in CSV format if and only if it is of interest
            if(not boolIsArreteProbablyFalsePositive and listeDecreeTopic!=[]):
                csvdata.addArreteToFile(objectDecree) 
            
        print("End execution of attribution keywords")

    def getDictLabelToId(self):
            """
            Returns a dictionary that associates each topic name with its id
            """
            listeDecreeTopics = getTopics()
            return {topic.label: topic.id for topic in listeDecreeTopics}
    
    def isArreteProbablyFalsePositive(self, listeDecreeTopic):
        """
        Returns a boolean that indicates whether the decree is likely to be a false positive from the list of associated decreeTopics, 
        i.e. that some keys words have matched but are not relevant enough to say that it's an interesting decree.
        """
        
        listeLabel = []
        listeKeyWordsNotInterestingAlone = [] # ["armes", "destruction"]
        
        for decreeTopic in listeDecreeTopic:
            listeLabel.append(decreeTopic.label)

        for el in listeKeyWordsNotInterestingAlone:
            if(el==listeLabel):
                return True
            
        return False
