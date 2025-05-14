import threading
import time
from furet.crawler.crawler import Crawler
from furet import settings
import os
from furet.processing.processing import Processing


def setup():
    #settings.setDefaultValue("crawler.autorun", True) # Là on force à True si on veut le Crawler
    settings.setDefaultValue("crawler.autorun", False) # Là on force à True si on veut le Crawler
    
    # autorun is defined in a .config file, if it is False then no crawler (by default in the .config it is false)
    autorun = settings.value("crawler.autorun")
    if autorun:
        from furet.processing.processing import Processing
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

        os.makedirs(paramPdfStorageDirectory_path, exist_ok=True) # We create the folder if it does not exist
        os.makedirs(paramOutputProcessingSteps_path, exist_ok=True) # We create the folder if it does not exist

        processing = Processing(pdfDirectory_path=paramPdfStorageDirectory_path, outputProcessingSteps_path=paramOutputProcessingSteps_path)
        processing_thread = threading.Thread(target=processing.startProcessing)
        processing_thread.start()
        processing_thread.join()