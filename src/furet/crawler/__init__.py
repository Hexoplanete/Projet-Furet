import threading
import time
from furet.crawler.crawler import Crawler
from furet import settings
import os
from furet.processing.processing import Processing


def setup():
    settings.setDefaultValue("crawler.autorun", False)
    
    autorun = settings.value("crawler.autorun")
    if autorun:
        from furet.processing.processing import Traitement
        start_time = time.time()
        crawler = Crawler()
        crawler_thread = threading.Thread(target=crawler.startCrawler)

        crawler_thread.start()

        crawler_thread.join()
        end_time = time.time()
        print(f"Total execution time: {end_time - start_time:.2f} seconds")

        pathDatabase = settings.value("repository.csv-root")

        paramPdfStorageDirectory_path = os.path.join(os.getcwd(), pathDatabase, "pdfDirectory") # A recupérer dans le frontend ? Donc pas ici mais dans "importFileWindow.py"
        paramOutputProcessingSteps_path = os.path.join(os.getcwd(), pathDatabase, "debug", "processingSteps") # A recupérer dans le frontend ? Donc pas ici mais dans "importFileWindow.py"

        os.makedirs(paramPdfStorageDirectory_path, exist_ok=True) # Si on récupère ça du front alors logiquement, le dossier doit déjà existé 
        os.makedirs(paramOutputProcessingSteps_path, exist_ok=True) # Si on récupère ça du front alors logiquement, le dossier doit déjà existé 

        processing = Processing(pdfDirectory_path=paramPdfStorageDirectory_path, outputProcessingSteps_path=paramOutputProcessingSteps_path)
        processing_thread = threading.Thread(target=processing.startProcessing)
        processing_thread.start()
        processing_thread.join()