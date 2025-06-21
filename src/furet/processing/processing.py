import logging
import shutil
from typing import Any, Callable
from furet.configs import ProcessingConfig
from furet.processing import utils
from furet.processing.getKeyWords import getKeyWords
from furet.processing.correspondenceNameNumberDepartment import departementsLabelToCode
from furet.processing.ocr import mainOcr
from furet.processing.separation import mainSeparation
from furet.processing.getCharacteristics import extractDocumentCharacterisics
from furet import repository
from furet.models.decree import Decree
from furet.models.campaign import Topic
from furet.models.raa import RAA
from furet import settings

import subprocess
import os
import json
import requests
import datetime

logger = logging.getLogger("processing")

class Processing:

    def downloadPDF(self, url, outputPath):
        """
            Download a PDF file from the given URL and put it in the output directory.

            :param url: URL of the PDF file.
        """

        logger.info(f"Downloading {url}...")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "fr-FR,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        }
        try:
            response = requests.get(url, stream=True, headers=headers)
            response.raise_for_status()
            
            fileName = os.path.join(outputPath)
            if not fileName.endswith('.pdf'):
                fileName += ".pdf"
            with open(fileName, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            logger.info(f"Downloaded: {fileName}")
        except requests.RequestException as e:
            logger.info(f"Failed to download {url}: {e}")

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

        pdfDir = os.path.join(settings.config(ProcessingConfig).pdfDir, ".crawler")

        for el in listeDictRAA:
            #rootDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
            #raaSavePath = os.path.join(rootDir, "src", "furet", "processing", "input_RAA",f"{os.path.basename(raaUrl)}")
            raaUrl = el["link"]
            raaSavePath = os.path.join(pdfDir, f"{os.path.basename(raaUrl)}")
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
        logger.info(f"Processing {inputPath}...")

        config = settings.config(ProcessingConfig)
        stepDirectory = os.path.join(config.pdfDir, ".steps")

        TOTAL_STEPS = 4+1
        if reportProgress is not None: reportProgress(0, 0, "Initialisation")
        fileHash = utils.getFileHash(inputPath)
        raa = repository.getRaaByHash(fileHash)
        if raa is not None:
            logger.info(f"{inputPath} was already imported")
            if reportProgress is not None: reportProgress(TOTAL_STEPS, TOTAL_STEPS, "Déja importé")
            return raa, []
        raa = RAA(0, fileHash)

        # We reduce the quality of the PDF to remove the error "BOMB DOS ATTACK SIZE LIMIT"
        logger.info("Executing magick...")
        if reportProgress is not None: reportProgress(1, TOTAL_STEPS, "Minification...")
        directoryApresMagick = os.path.join(stepDirectory, "1-magick")
        os.makedirs(directoryApresMagick, exist_ok=True)
        pathApresMagick = os.path.join(directoryApresMagick, f"{fileHash}.pdf")

        commande = [
            "magick",
            "-density", "300",
            f"{inputPath}",
            "-resize", "100%",
            "-quality", "85",
            pathApresMagick
        ]

        subprocess.run(commande, check=True)
        logger.debug("Finished magick execution")
        logger.info("Executing ocr...")
        if reportProgress is not None: reportProgress(2, TOTAL_STEPS, "OCR...")
        directoryApresOcr = os.path.join(stepDirectory, "2-ocr")
        os.makedirs(directoryApresOcr, exist_ok=True)
        pathApresOcr = os.path.join(directoryApresOcr, f"{fileHash}.pdf")

        mainOcr(pathApresMagick,pathApresOcr)
        logger.debug("Finished ocr execution")

        logger.info("Executing separation...")
        if reportProgress is not None: reportProgress(3, TOTAL_STEPS, "Séparation...")
        directoryApresSeparation = os.path.join(stepDirectory, "3-separation", fileHash)
        os.makedirs(directoryApresSeparation, exist_ok=True)

        pdfDecrees = mainSeparation(pathApresOcr, directoryApresSeparation, raa)
        raa.decreeCount = len(pdfDecrees)
        logger.debug("Finished separation execution")

        logger.info("Executing keywords separation...")
        if reportProgress is not None: reportProgress(4, TOTAL_STEPS, "Séparation...")
        directoryApresMotClef = os.path.join(stepDirectory, "4-keywords", fileHash)
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
                
        logger.debug("Finished attribution keywords")
        logger.info("Cleaning up...")
        os.makedirs(config.pdfDir, exist_ok=True)
        shutil.copy(pathApresOcr, os.path.join(config.pdfDir))
        if not config.debug:
            os.remove(pathApresMagick)
            os.remove(pathApresOcr)
            shutil.rmtree(directoryApresSeparation)
            shutil.rmtree(directoryApresMotClef)

        if reportProgress is not None: reportProgress(TOTAL_STEPS, TOTAL_STEPS, "Fini !")
        logger.info(f"Successfully processed {inputPath}: {raa.decreeCount} decrees")
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

            



    
