import hashlib
from typing import Any, Callable
from furet.processing.getKeyWords import getKeyWords
from furet.processing.correspondenceNameNumberDepartment import departementsLabelToCode
from furet.processing.ocr import mainOcr
from furet.processing.separation import mainSeparation
from furet.processing.getCharacteristics import extractDocumentCharacterisics
from furet import repository
from furet.types.decree import *
from furet import settings

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
        
        # Output folder where there are the outputs of each of the stages of the processing part, 
        self.outputProcessingSteps_path = outputProcessingSteps_path
    
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
        linkFile = os.path.join(settings.value("crawler.result"), "resultCrawler.json")
        
        if os.path.exists(linkFile):
            with open(linkFile, 'r') as f:
                data = json.load(f)
            return data["links"]
        else:
            return []
    
    # TODO move to crawler
    def startProcessing(self):
        """ 
            Function that is Input to the Processing Framework
            Retrieves information provided by the crawler for each RAA crawled : url, datePublication, departement (Creates a corresponding RAA object)
            Downloads the RAA from the URL
            Calls processing_RAA(...) -> Processes the RAA
        """
        # List of dictionaries representing RAAs (retrieved by the crawler)
        listeDictRAA = self.readLinkFile()

        for el in listeDictRAA:
            #rootDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
            #raaSavePath = os.path.join(rootDir, "src", "furet", "processing", "input_RAA",f"{os.path.basename(raaUrl)}")
            raaUrl = el["link"]
            raaSavePath = os.path.join(self.pdfDirectory_path,f"{os.path.basename(raaUrl)}")
            self.downloadPDF(raaUrl, raaSavePath)
            raa, decrees = self.processingRAA(raaSavePath)
            if raa.id != 0:
                continue
            
            raa.url = raaUrl
            raa.publicationDate = datetime.datetime.strptime(el["datePublication"], "%d/%m/%Y")
            raaDepartementLabel = el["department"]
            departementNumber = int(departementsLabelToCode[raaDepartementLabel])
            raa.department = repository.getDepartmentById(departementNumber)

            repository.addRaa(raa)
            repository.addDecree(decrees)

    def processingRAA(self, inputPath, reportProgress: Callable[[int, int, str], Any] | None = None) -> tuple[RAA, list[Decree]]:
        """ 
        Input : PDF corresponding to an RAA (RAA which was just downloaded from the links obtained by the crawler)

        Reduce PDF quality using magick → Generates a new PDF in -> "self.outputProcessingSteps_path/after_magick/"

        Perform OCR on the input PDF to generate a new "OCR-processed" PDF, meaning it's converted to text format → Generates a new OCR-processed PDF -> "self.outputProcessingSteps_path/after_ocr/"

        Split the RAA into decrees → Generates one PDF per decree from the RAA -> "self.outputProcessingSteps_path/after_split/{RAA_Name}/"

        Assign keywords to a decree

        Ouput → a csv file for each decree -> "database/prefectures/{code_department}/{code_department}_{month}.csv"
        """

        TOTAL_STEPS = 6
        if reportProgress is not None: reportProgress(1, TOTAL_STEPS, "Initialisation")
        with open(inputPath, "rb") as file:
            digest = hashlib.file_digest(file, "sha256")
        fileHash = digest.hexdigest()
        raa = repository.getRaaByHash(fileHash)
        if raa is not None:
            print("Skipping file")
            if reportProgress is not None: reportProgress(TOTAL_STEPS, TOTAL_STEPS, "Déja importé")
            return raa ,[]
        raa = RAA(0, fileHash)

        # We reduce the quality of the PDF to remove the error "BOMB DOS ATTACK SIZE LIMIT"
        print("Start magick execution")
        if reportProgress is not None: reportProgress(2, TOTAL_STEPS, "Minification...")
        directoryApresMagick = os.path.join(self.outputProcessingSteps_path, "after_magick")
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

        subprocess.run(commande, check=True)
        print("End magick execution")
        print("--------------------------------")
        print("Start ocr execution")
        if reportProgress is not None: reportProgress(3, TOTAL_STEPS, "OCR...")
        directoryApresOcr = os.path.join(self.outputProcessingSteps_path, "after_ocr")
        print(directoryApresOcr)
        os.makedirs(directoryApresOcr, exist_ok=True)
        pathApresOcr = os.path.join(directoryApresOcr, os.path.basename(inputPath))

        mainOcr(pathApresMagick,pathApresOcr)
        print("End ocr execution")
        print("--------------------------------")

        print("Start separation execution")
        if reportProgress is not None: reportProgress(4, TOTAL_STEPS, "Séparation...")
        basenameRAA = os.path.basename(inputPath).replace(".pdf","").replace(" ","")

        directoryApresSeparation = os.path.join(self.outputProcessingSteps_path, "after_separation", basenameRAA)
        os.makedirs(directoryApresSeparation, exist_ok=True)
        pathApresSeparation = os.path.join(directoryApresSeparation, os.path.basename(inputPath))

        pdfDecrees = mainSeparation(pathApresOcr, directoryApresSeparation, raa)
        raa.decreeCount = len(pdfDecrees)
        print("End separation execution")
        print("--------------------------------")

        print("Start execution of attribution keywords")
        if reportProgress is not None: reportProgress(5, TOTAL_STEPS, "Séparation...")
        directoryApresMotClef = os.path.join(self.outputProcessingSteps_path, "after_mot_cle", basenameRAA)
        os.makedirs(directoryApresMotClef, exist_ok=True)

        
        decrees = []
        for pathDecree, objectDecree in pdfDecrees:

            dic = self.getDictLabelToId() ; listeKeyWords = list(dic.keys())

            pathApresMotClef = os.path.join(directoryApresMotClef, f"{os.path.basename(pathDecree).replace('.pdf','')}.txt")
            dicKeyWords = getKeyWords(pathDecree, pathApresMotClef.replace(".txt",""), listeKeyWords) 
            
            # We create a list containing a list of DecreeTopics (KeyWords) that match the decree
            listeDecreeTopic = []

            for label, id in dicKeyWords.items():
                topic = Topic(id=dic[label], label=label)
                listeDecreeTopic.append(topic)

            objectDecree.topics = listeDecreeTopic

            # Check if the decree is really interesting
            # For example, if there is only "armes" the bylaw is VERY unlikely to be of interest.
            boolIsArreteProbablyFalsePositive = self.isArreteProbablyFalsePositive(listeDecreeTopic)

            # Saves decree information in CSV format if and only if it is of interest
            if(not boolIsArreteProbablyFalsePositive and listeDecreeTopic!=[]):
                
                # Retrieving data that can be extracted from the decree, if the extraction did not work then we will leave the default value : Title, Decree Number, Document Type (In reality there are 99% decrees but there are also other types)
                characteristics = extractDocumentCharacterisics(pathDecree)
                if characteristics is not None:
                    objectDecree.title = characteristics["Title"]
                    objectDecree.number = characteristics["Number"]

                    if characteristics["Type"] is not None:
                        objectDecree.docType = repository.getDocumentTypeById(characteristics["Type"])

                objectDecree.campaigns = self.getCampaignFromDecree(objectDecree) 
                
                decrees.append(objectDecree)
                
        print("End execution of attribution keywords")

        if reportProgress is not None: reportProgress(TOTAL_STEPS, TOTAL_STEPS, "Fini !")
        return raa, decrees

    def getDictLabelToId(self):
            """
            Returns a dictionary that associates each topic name with its id
            """
            listeDecreeTopics = repository.getTopics()
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
    
    def getCampaignFromDecree(self, decree):
        """
        Takes a decree as input and returns the list of objects campaigns that match the associated keywords
        """

        campaignsDecree = set()

        for currentDecreeTopic in decree.topics :
            listeCampaignCurrentTopic = repository.getCampaignFromTopic(currentDecreeTopic)
            campaignsDecree.update(listeCampaignCurrentTopic)

        return list(campaignsDecree)

            



    
