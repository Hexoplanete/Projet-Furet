from PySide6.QtWidgets import QApplication
from . import settings, app
from furet import repository, crawler

import threading
from furet.traitement.Traitement import Traitement

#from datetime import datetime

def main():
    QApplication.setApplicationName("Fouille Universelle de Recueils pour Entreposage et Traitement")
    QApplication.setOrganizationDomain("github.com/Hexoplanete/Projet-Furet/")
    QApplication.setOrganizationName("Hexoplanète")

    settings.setup()
    app.setup()
    crawler.init()
    
    traitement = Traitement()
    traitement_thread = threading.Thread(target=traitement.startTraitement)
    traitement_thread.start()
    traitement_thread.join()

    repository.setup()  
    
    app.main()

if __name__ == '__main__':
    main()
    