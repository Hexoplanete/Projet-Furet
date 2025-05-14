from PySide6.QtWidgets import QApplication
from . import settings, app
from furet import repository, crawler

import threading
from furet.processing.processing import Processing
import os

#from datetime import datetime

def main():
    QApplication.setApplicationName("Fouille Universelle de Recueils pour Entreposage et Traitement")
    QApplication.setOrganizationDomain("github.com/Hexoplanete/Projet-Furet/")
    QApplication.setOrganizationName("Hexoplanète")

    settings.setup()
    app.setup()
    crawler.init()
    repository.setup()  
    
    paramPdfStorageDirectory_path = os.path.join(os.getcwd(), "database", "pdfDirectory") # A recupérer dans le frontend ? Donc pas ici mais dans "importFileWindow.py"
    paramOutputProcessingSteps_path = os.path.join(os.getcwd(), "database", "debug", "processingSteps") # A recupérer dans le frontend ? Donc pas ici mais dans "importFileWindow.py"

    processing = Processing(pdfDirectory_path=paramPdfStorageDirectory_path, outputProcessingSteps_path=paramOutputProcessingSteps_path)
    processing_thread = threading.Thread(target=processing.startProcessing)
    processing_thread.start()
    processing_thread.join()

    repository.readAllArretesFromFiles()
    
    app.main()

if __name__ == '__main__':
    main()
    