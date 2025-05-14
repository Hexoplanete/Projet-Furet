from PySide6.QtWidgets import QApplication
import os
from furet import repository, app, crawler, settings
from PySide6 import QtCore

def main():
    QApplication.setApplicationName("FURET")
    QApplication.setApplicationDisplayName("Fouille Universelle de Recueils pour Entreposage et Traitement")
    QApplication.setOrganizationDomain("github.com/Hexoplanete/Projet-Furet/")
    QApplication.setOrganizationName("Hexoplanete")

    os.makedirs(QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.AppDataLocation), exist_ok=True)
    settings.setup()
    app.setup()
    crawler.setup()
    repository.setup()
    repository.readAllArretesFromFiles()
    app.main()
    pass

if __name__ == '__main__':
    main()
    